# -*- coding: utf-8 -*-
#
#       rtk.stakeholder.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model Module."""

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from dao import RTKStakeholder  # pylint: disable=E0401


class StakeholderDataModel(RTKDataModel):
    """
    Contain the attributes and methods of Stakeholder.

    The Stakeholder data model contains the attributes and methods of a
    stakeholder.  A Revision will contain zero or more definitions.  The
    attributes of a Stakeholder are:
    """

    _tag = 'Stakeholders'

    def __init__(self, dao):
        """
        Initialize a Stakeholder data model instance.

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

    def select_all(self, revision_id):
        """
        Retrieve all the Stakeholders from the RTK Program database.

        This method retrieves all the records from the RTKStakeholder
        table in the connected RTK Program database.  It then add each to the
        Stakeholder data model treelib.Tree().

        :param int revision_id: the Revision ID to select the Failure
                                Definition records.
        :return: tree; the treelib Tree() of RTKStakeholder data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _stakeholder in _session.query(RTKStakeholder).filter(
                RTKStakeholder.revision_id == revision_id).all():
            self.tree.create_node(
                _stakeholder.description,
                _stakeholder.stakeholder_id,
                parent=0,
                data=_stakeholder)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _stakeholder.stakeholder_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Add a record to the RTKStakeholder table.

        :param int revision_id: the Revision ID to add the Failure
                                Definition against.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _stakeholder = RTKStakeholder()
        _stakeholder.revision_id = _revision_id
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _stakeholder,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _stakeholder.description,
                _stakeholder.stakeholder_id,
                parent=0,
                data=_stakeholder)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _stakeholder.stakeholder_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKStakeholder table.

        :param int node_id: the ID of the Stakeholder to be
                                  removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Stakeholder ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record in the RTKStakeholder table.

        :param int node_id: the Stakeholder ID to save to the RTK
                                  Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Stakeholder ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKStakeholder records.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Updating the RTK Program database.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.stakeholder_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.stakeholder.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.stakeholder.Model.update_all().'

        return _error_code, _msg

    def calculate_weight(self, stakeholder_id):
        """
        Calculate the improvement factor and overall weighting.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _stakeholder = self.tree.get_node(stakeholder_id).data

        _stakeholder.improvement = 1.0 + 0.2 * (
            _stakeholder.planned_rank - _stakeholder.customer_rank)
        _stakeholder.overall_weight = float(_stakeholder.priority) * \
            _stakeholder.improvement * _stakeholder.user_float_1 * \
            _stakeholder.user_float_2 * _stakeholder.user_float_3 * \
            _stakeholder.user_float_4 * _stakeholder.user_float_5

        return _return
