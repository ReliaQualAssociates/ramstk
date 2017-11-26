# -*- coding: utf-8 -*-
#
#       rtk.validation.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from dao import RTKValidation  # pylint: disable=E0401


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

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, validation_id):  # pylint: disable=unused-argument
        """
        Retrieve all the Validations from the RTK Program database.

        This method retrieves all the records from the RTKValidation table in the
        connected RTK Program database.  It then add each to the Validation data
        model treelib.Tree().

        :param int validation_id: unused, only required for compatibility with
                                underlying RTKDataModel.
        :return: tree; the Tree() of RTKValidation data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _validation in _session.query(RTKValidation).all():
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
        _error_code, _msg = RTKDataModel.insert(self, entities=[
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
