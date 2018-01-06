# -*- coding: utf-8 -*-
#
#       rtk.validation.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

from datetime import date

from statistics.Bounds import calculate_beta_bounds  # pylint: disable=E0401
from sortedcontainers import SortedDict  # pylint: disable=E0401
from treelib import tree, Tree  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import date_to_ordinal  # pylint: disable=E0401
from datamodels import RTKDataModel  # pylint: disable=E0401
from dao import RTKProgramStatus, RTKValidation  # pylint: disable=E0401


class ValidationDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Validation.

    An RTK Project will consist of one or more Validations.  The attributes of a
    Validation are:
    """

    _tag = 'Validations'

    def __init__(self, dao):
        """
        Initialize a Validation data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_status = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.status_tree = Tree()

        # Add the root to the status Tree().  This is neccessary to allow
        # multiple entries at the top level as there can only be one root in a
        # treelib Tree().  Manipulation and viewing of a RTK module tree needs
        # to ignore the root of the tree.
        try:
            self.status_tree.create_node(
                tag='Program Status', identifier=0, parent=None)
        except (tree.MultipleRootError, tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError):
            pass

    def select_all(self, revision_id):  # pragma: no cover
        """
        Retrieve all the Validations from the RTK Program database.

        This method retrieves all the records from the RTKValidation table in
        the connected RTK Program database.  It then add each to the Validation
        data model treelib.Tree().

        :param int revision_id: the Revision ID to select the Validation tasks
                                for.
        :return: tree; the Tree() of RTKValidation data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _validation in _session.query(RTKValidation).filter(
                RTKValidation.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _validation.get_attributes()
            _validation.set_attributes(_attributes)
            self.tree.create_node(
                _validation.description,
                _validation.validation_id,
                parent=0,
                data=_validation)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _validation.validation_id)

        # Now select all the status updates.
        _today = False
        for _status in _session.query(RTKProgramStatus).filter(
                RTKProgramStatus.revision_id == revision_id).all():
            _attributes = _status.get_attributes()
            _status.set_attributes(_attributes)
            try:
                self.status_tree.create_node(
                    _status.date_status,
                    date_to_ordinal(_status.date_status),
                    parent=0,
                    data=_status)
            except tree.DuplicatedNodeIdError:
                pass
            if _status.date_status == date.today():
                _today = True

        if not _today:
            _status = RTKProgramStatus()
            _status.revision_id = revision_id
            _status.date_status = date.today()
            _error_code, _msg = RTKDataModel.insert(
                self, entities=[
                    _status,
                ])

            if _error_code == 0:
                self.status_tree.create_node(
                    _status.date_status,
                    date_to_ordinal(_status.date_status),
                    parent=0,
                    data=_status)

        _session.close()

        return self.tree

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKValidation table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _validation = RTKValidation()
        _validation.revision_id = kwargs['revision_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _validation,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _validation.description,
                _validation.validation_id,
                parent=0,
                data=_validation)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _validation.validation_id

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKValidation table.

        :param int node_id entity: the ID of the RTKValidation record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Validation ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Validation ID of the Validation to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Validation ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKValidation table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.validation_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.validation.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.validation.Model.update_all().'

        return _error_code, _msg

    def update_status(self):
        """
        Update the overall program Validation status.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _node_id = date_to_ordinal(date.today())

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        try:
            _entity = self.status_tree.get_node(_node_id).data
            if _entity is not None:
                _session.add(_entity)
                _error_code, _msg = self.dao.db_update(_session)
        except AttributeError:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to save non-existent Program ' \
                   'Status for date {0:s}.'.format(str(_node_id))

        _session.close()

        return _error_code, _msg

    def calculate_costs(self, validation_id):
        """
        Calculate task cost metrics.

        This method calculate mean, lower bound, upper bound, and standard
        error on task costs.

        :param int validation_id: the Validation ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _validation = self.tree.get_node(validation_id).data

        return _validation.calculate_task_cost()

    def calculate_time(self, validation_id):
        """
        Calculate task time metrics.

        This method calculate mean, lower bound, upper bound, and standard
        error on task time.

        :param int validation_id: the Validation ID to calculate.
        :param float mission_time: the time over which to calculate costs.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _validation = self.tree.get_node(validation_id).data

        return _validation.calculate_task_time()

    def calculate_program(self):
        """
        Calculate the overall cost and time of all validation tasks.

        :param int revision_id: the Revision ID to calculate program costs for.
        :return: (_cost_ll, _cost_mean, _cost_ul,
                  _time_ll, _time_mean, _time_ul); the lower bound, mean,
                 and upper bound for program cost and time.
        :rtype: tuple
        """
        _cost_minimum = 0.0
        _cost_average = 0.0
        _cost_maximum = 0.0
        _time_minimum = 0.0
        _time_average = 0.0
        _time_maximum = 0.0
        _time_remaining = 0.0
        _status = self.status_tree.get_node(date_to_ordinal(date.today())).data

        for _node in self.tree.children(0):
            self.calculate_costs(_node.data.validation_id)
            _cost_minimum += _node.data.cost_minimum
            _cost_average += _node.data.cost_average
            _cost_maximum += _node.data.cost_maximum
            self.calculate_time(_node.data.validation_id)
            _time_minimum += _node.data.time_minimum
            _time_average += _node.data.time_average
            _time_maximum += _node.data.time_maximum
            _time_remaining += _node.data.time_average * (
                1.0 - _node.data.status / 100.0)

        _status.time_remaining = _time_remaining

        (_cost_ll, _cost_mean, _cost_ul, __) = calculate_beta_bounds(
            _cost_minimum, _cost_average, _cost_maximum, 0.95)
        (_time_ll, _time_mean, _time_ul, __) = calculate_beta_bounds(
            _time_minimum, _time_average, _time_maximum, 0.95)

        return (_cost_ll, _cost_mean, _cost_ul, _time_ll, _time_mean, _time_ul)

    def assessments(self):
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
                    _node.data.acceptable_maximum
                ])

        return _assessment_dates, _targets

    def planned_burndown(self):
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
                date_to_ordinal(_node.data.date_start), _date_minimum)
            _time_minimum = min(_node.data.time_minimum, _time_minimum)
            _time_average = min(_node.data.time_average, _time_average)
            _time_maximum = min(_node.data.time_maximum, _time_maximum)
            _y_minimum[_date_minimum] = _time_minimum
            _y_average[_date_minimum] = _time_average
            _y_maximum[_date_minimum] = _time_maximum
            try:
                _y_minimum[date_to_ordinal(
                    _node.data.date_end)] += _node.data.time_minimum
            except KeyError:
                _y_minimum[date_to_ordinal(
                    _node.data.date_end)] = _node.data.time_minimum

            try:
                _y_average[date_to_ordinal(
                    _node.data.date_end)] += _node.data.time_average
            except KeyError:
                _y_average[date_to_ordinal(
                    _node.data.date_end)] = _node.data.time_average

            try:
                _y_maximum[date_to_ordinal(
                    _node.data.date_end)] += _node.data.time_maximum
            except KeyError:
                _y_maximum[date_to_ordinal(
                    _node.data.date_end)] = _node.data.time_maximum

        return SortedDict(_y_minimum), SortedDict(_y_average), SortedDict(
            _y_maximum)

    def actual_burndown(self):
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

        _dates = SortedDict(self.status_tree.nodes).keys()
        _dates.pop(0)

        for _key in _dates:
            _entity = self.status_tree.get_node(_key).data
            _time_remaining[date_to_ordinal(
                _entity.date_status)] = _entity.time_remaining

        return _time_remaining
