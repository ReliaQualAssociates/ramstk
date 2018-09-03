# -*- coding: utf-8 -*-
#
#       rtk.modules.stakeholder.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model Module."""

# Import other RAMSTK modules.
from rtk.modules import RAMSTKDataModel
from rtk.dao import RAMSTKStakeholder


class StakeholderDataModel(RAMSTKDataModel):
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

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Stakeholders from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKStakeholder
        table in the connected RAMSTK Program database.  It then add each to the
        Stakeholder data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKStakeholder data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self, **kwargs)

        for _stakeholder in _session.query(RAMSTKStakeholder).filter(
                RAMSTKStakeholder.revision_id == _revision_id).all():
            self.tree.create_node(
                _stakeholder.description,
                _stakeholder.stakeholder_id,
                parent=0,
                data=_stakeholder)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _stakeholder.stakeholder_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKStakeholder table.

        :param int revision_id: the Revision ID to add the Failure
                                Definition against.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _stakeholder = RAMSTKStakeholder()
        _stakeholder.revision_id = _revision_id
        _error_code, _msg = RAMSTKDataModel.do_insert(
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
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _stakeholder.stakeholder_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKStakeholder table.

        :param int node_id: the ID of the Stakeholder to be
                                  removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Stakeholder ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record in the RAMSTKStakeholder table.

        :param int node_id: the Stakeholder ID to save to the RAMSTK
                                  Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Stakeholder ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKStakeholder records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more records in the stakeholder "
                        "table did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all records in the stakeholder "
                    "table.")

        return _error_code, _msg

    def do_calculate(self, node_id, **kwargs):  # pylint: disable=unused-argument
        """
        Calculate the improvement factor and overall weighting.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _stakeholder = self.tree.get_node(node_id).data

        _stakeholder.improvement = 1.0 + 0.2 * (
            _stakeholder.planned_rank - _stakeholder.customer_rank)
        _stakeholder.overall_weight = float(_stakeholder.priority) * \
            _stakeholder.improvement * _stakeholder.user_float_1 * \
            _stakeholder.user_float_2 * _stakeholder.user_float_3 * \
            _stakeholder.user_float_4 * _stakeholder.user_float_5

        return _return

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all Stakeholder inputs.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Calculate all Stakeholder inputs, skipping the top node in the tree.
        for _node in self.tree.all_nodes():
            if _node.identifier != 0:
                self.do_calculate(_node.identifier, **kwargs)

        return _return
