# -*- coding: utf-8 -*-
#
#       ramstk.validation.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict
from treelib import Tree, tree

# RAMSTK Package Imports
from ramstk.dao import RAMSTKProgramStatus, RAMSTKValidation
from ramstk.modules import RAMSTKDataModel
from ramstk.statistics.Bounds import calculate_beta_bounds
from ramstk.Utilities import date_to_ordinal


class ValidationDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Validation.

    An RAMSTK Project will consist of one or more Validations.  The attributes
    of a Validation are:
    """

    _tag = 'Validations'

    def __init__(self, dao, **kwargs):
        """
        Initialize a Validation data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']

        # Initialize public dictionary attributes.
        self.dic_status = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.status_tree = Tree()

        # Add the root to the status Tree().  This is neccessary to allow
        # multiple entries at the top level as there can only be one root in a
        # treelib Tree().  Manipulation and viewing of a RAMSTK module tree needs
        # to ignore the root of the tree.
        try:
            self.status_tree.create_node(
                tag='Program Status', identifier=0, parent=None,
            )
        except (
                tree.MultipleRootError, tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError,
        ):
            pass

    def do_calculate(self, node_id, **kwargs):
        """
        Calculate task cost metrics.

        This method calculate mean, lower bound, upper bound, and standard
        error on task costs.

        :param int node_id: the PyPubSub Tree() ID of the Validation to
                            calculate.
        :return: None
        :rtype: None
        """
        _metric = kwargs['metric']
        _validation = self.tree.get_node(node_id).data

        if _metric == 'cost':
            _validation.calculate_task_cost()
        elif _metric == 'time':
            _validation.calculate_task_time()

        if not self._test:
            pub.sendMessage('calculated_validation', node_id=node_id)

    def do_calculate_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Calculate the overall cost and time of all validation tasks.

        :param int revision_id: the Revision ID to calculate program costs for.
        :return: _attributes; a dictionary of program status results.
        :rtype: dict
        """
        _attributes = {
            'cost_minimum':
            0.0,
            'cost_average':
            0.0,
            'cost_maximum':
            0.0,
            'time_minimum':
            0.0,
            'time_average':
            0.0,
            'time_maximum':
            0.0,
            'time_remaining':
            0.0,
            'status':
            self.status_tree.get_node(date_to_ordinal(date.today())).data,
            'cost_ll':
            0.0,
            'cost_mean':
            0.0,
            'cost_ul':
            0.0,
            'cost_variance':
            0.0,
            'time_ll':
            0.0,
            'time_mean':
            0.0,
            'time_ul':
            0.0,
            'time_variance':
            0.0,
            'y_minimum':
            None,
            'y_average':
            None,
            'y_maximum':
            None,
            'assessment_dates':
            None,
            'targets':
            None,
            'y_actual':
            None,
        }

        for _node in self.tree.children(0):
            self.do_calculate(_node.data.validation_id, metric='cost')
            _attributes['cost_minimum'] += _node.data.cost_minimum
            _attributes['cost_average'] += _node.data.cost_average
            _attributes['cost_maximum'] += _node.data.cost_maximum
            self.do_calculate(_node.data.validation_id, metric='time')
            _attributes['time_minimum'] += _node.data.time_minimum
            _attributes['time_average'] += _node.data.time_average
            _attributes['time_maximum'] += _node.data.time_maximum
            _attributes['time_remaining'] += _node.data.time_average * (
                1.0 - _node.data.status / 100.0
            )

        _attributes['status'].time_remaining = _attributes['time_remaining']

        (
            _attributes['cost_ll'], _attributes['cost_mean'],
            _attributes['cost_ul'],
            _attributes['time_variance'],
        ) = calculate_beta_bounds(
            _attributes['cost_minimum'], _attributes['cost_average'],
            _attributes['cost_maximum'], 0.95,
        )
        (
            _attributes['time_ll'], _attributes['time_mean'],
            _attributes['time_ul'], __,
        ) = calculate_beta_bounds(
            _attributes['time_minimum'], _attributes['time_average'],
            _attributes['time_maximum'], 0.95,
        )

        _attributes['time_variance'] = _attributes['time_variance']**2
        _attributes['cost_variance'] = _attributes['cost_variance']**2

        (
            _attributes['y_minimum'], _attributes['y_average'],
            _attributes['y_maximum'],
        ) = self.get_planned_burndown()
        (
            _attributes['assessment_dates'],
            _attributes['targets'],
        ) = self.get_assessment_points()
        _attributes['y_actual'] = self.get_actual_burndown()

        if not self._test:
            pub.sendMessage('calculated_validation', attributes=_attributes)

        return _attributes

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKValidation table.

        :param int node_id entity: the ID of the RAMSTKValidation record to be
                                   removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Validation ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

            # If we're not running a test, let anyone who cares know a
            # Validation Task was deleted.
            if not self._test:
                pub.sendMessage('deleted_validation', tree=self.tree)

        return _error_code, _msg

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKValidation table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _validation = RAMSTKValidation()
        _validation.revision_id = kwargs['revision_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _validation,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _validation.description,
                _validation.validation_id,
                parent=0,
                data=_validation,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _validation.validation_id

            # If we're not running a test, let anyone who cares know a new
            # Function was inserted.
            if not self._test:
                pub.sendMessage('inserted_validation', tree=self.tree)

        return _error_code, _msg

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Validations from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKValidation table in
        the connected RAMSTK Program database.  It then add each to the Validation
        data model treelib.Tree().

        :return: tree; the Tree() of RAMSTKValidation data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _validation in _session.query(RAMSTKValidation).filter(
                RAMSTKValidation.revision_id == _revision_id,
        ).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _validation.get_attributes()
            _validation.set_attributes(_attributes)
            self.tree.create_node(
                _validation.description,
                _validation.validation_id,
                parent=0,
                data=_validation,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _validation.validation_id)
            except TypeError:
                self.last_id = _validation.validation_id

        # Now select all the status updates.
        _today = False
        for _status in _session.query(RAMSTKProgramStatus).filter(
                RAMSTKProgramStatus.revision_id == _revision_id,
        ).all():
            _attributes = _status.get_attributes()
            _status.set_attributes(_attributes)
            try:
                self.status_tree.create_node(
                    _status.date_status,
                    date_to_ordinal(_status.date_status),
                    parent=0,
                    data=_status,
                )
            except tree.DuplicatedNodeIdError:
                pass
            if _status.date_status == date.today():
                _today = True

        if not _today:
            _status = RAMSTKProgramStatus()
            _status.revision_id = _revision_id
            _status.date_status = date.today()
            _error_code, _msg = RAMSTKDataModel.do_insert(
                self, entities=[
                    _status,
                ],
            )

            if _error_code == 0:
                self.status_tree.create_node(
                    _status.date_status,
                    date_to_ordinal(_status.date_status),
                    parent=0,
                    data=_status,
                )

        _session.close()

        # If we're not running a test and there were validation tasks returned,
        # let anyone who cares know the Validation tasks have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_validations', tree=self.tree)

    def do_update(self, node_id):
        """
        Update record associated with Node ID in the RAMSTK Program database.

        :param int node_id: the Validation ID of the Validation to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        # If there was no error and we're not running a test, let anyone
        # who cares know a Function was updated.
        if _error_code == 0:
            if not self._test:
                _attributes = self.do_select(node_id).get_attributes()
                pub.sendMessage('updated_validation', attributes=_attributes)
        else:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to save non-existent "
                "Validation ID {0:d}."
            ).format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKValidation table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the validation "
                "table."
            )

        return _error_code, _msg

    def do_update_status(self):
        """
        Update the overall program Validation status.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _node_id = date_to_ordinal(date.today())

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        try:
            _entity = self.status_tree.get_node(_node_id).data
            if _entity is not None:
                _session.add(_entity)
                _error_code, _msg = self.dao.db_update(_session)
        except AttributeError:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Program ' \
                   'Status for date {0:s}.'.format(str(_node_id))

        _session.close()

        return _error_code, _msg

    def get_actual_burndown(self):
        """
        Get the actual burndown curve dates and task times.

        This method creates and returns a SortedDict with remaining task times
        for each date.  The key is the ordinal date and the value is the sum of
        the remaining time for tasks due on that date.  The remaining times are
        calculated using the average expected time to complete the task.

        :return: _time_remaining; dictionary of remaining program time by date.
        :rtype: dict
        """
        _time_remaining = {}

        _dates = list(SortedDict(self.status_tree.nodes).keys())
        _dates.pop(0)

        for _key in _dates:
            _entity = self.status_tree.get_node(_key).data
            _time_remaining[
                date_to_ordinal(
                    _entity.date_status,
                )
            ] = _entity.time_remaining

        return _time_remaining

    def get_assessment_points(self):
        """
        Get the dates, minimum, and maximum values for reliability assessments.

        :return: (_assessed_dates, _targets)
        :rtype: tuple
        """
        _assessment_dates = []
        _targets = []

        for _node in self.tree.children(0):
            if _node.data.task_type == 'Reliability, Assessment':
                _assessment_dates.append(date_to_ordinal(_node.data.date_end))
                _targets.append([
                    _node.data.acceptable_minimum,
                    _node.data.acceptable_maximum,
                ])

        return _assessment_dates, _targets

    def get_planned_burndown(self):
        """
        Get the planned burndown curve dates and task times.

        This method creates and returns three SortedDicts; one with minimum
        expected task times, one with average expected task times, and one with
        maximum expected task times.  The key for each dict is the ordinal date
        and the value for each dict is the sum of times for tasks due on that
        date.

        :return: (_y_minimum, _y_average, _y_maximum)
        :rtype: tuple
        """
        _y_minimum = {}
        _y_average = {}
        _y_maximum = {}
        _date_minimum = 999999
        _time_minimum = 999999
        _time_average = 999999
        _time_maximum = 999999

        for _node in self.tree.children(0):
            _date_minimum = min(
                date_to_ordinal(_node.data.date_start), _date_minimum,
            )
            _time_minimum = min(_node.data.time_minimum, _time_minimum)
            _time_average = min(_node.data.time_average, _time_average)
            _time_maximum = min(_node.data.time_maximum, _time_maximum)
            _y_minimum[_date_minimum] = _time_minimum
            _y_average[_date_minimum] = _time_average
            _y_maximum[_date_minimum] = _time_maximum
            try:
                _y_minimum[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] += _node.data.time_minimum
            except KeyError:
                _y_minimum[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] = _node.data.time_minimum

            try:
                _y_average[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] += _node.data.time_average
            except KeyError:
                _y_average[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] = _node.data.time_average

            try:
                _y_maximum[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] += _node.data.time_maximum
            except KeyError:
                _y_maximum[
                    date_to_ordinal(
                        _node.data.date_end,
                    )
                ] = _node.data.time_maximum

        return SortedDict(_y_minimum), SortedDict(_y_average), SortedDict(
            _y_maximum,
        )
