# -*- coding: utf-8 -*-
#
#       ramstk.modules.allocation.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Models."""

# Third Party Imports
from pubsub import pub
from treelib.exceptions import DuplicatedNodeIdError, NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.data.storage.programdb import RAMSTKAllocation
from ramstk.modules import RAMSTKDataModel


class AllocationDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a reliability allocation."""

    _tag = 'Allocations'
    _root = 0

    def __init__(self, dao, **kwargs):
        """
        Initialize an Allocation data model instance.

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

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_calculate(self, node_id, **kwargs):
        """
        Calculate and allocate the goals for the selected hardware item.

        :param int node_id: the PyPubSub Tree() ID of the Hardware item whose
                            goal is to be allocated.
        :param list hazard_rates: the hazard rates of the parent hardware item
                                  to be allocated and each of the child items
                                  (only needed for ARINC apportionment).  Index
                                  0 is the parent hazard rate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        try:
            _hazard_rates = kwargs['hazard_rates']
        except KeyError:
            _hazard_rates = None
        _return = False

        _parent = self.do_select(node_id)
        _children = self.do_select_children(node_id)
        _parent.n_sub_systems = 0
        for _child in _children:
            if _child.data.included:
                _parent.n_sub_systems += 1

        # Calculate the parent goals.
        if not _parent.calculate_goals():
            # Allocate the goal to the children.
            _idx = 1
            _parent.weight_factor = sum([
                _child.data.int_factor * _child.data.soa_factor *
                _child.data.op_time_factor * _child.data.env_factor
                for _child in _children
            ])
            for _child in _children:
                if _parent.method_id == 1:
                    _return = (
                        _return or _child.data.equal_apportionment(
                            _parent.n_sub_systems,
                            _parent.reliability_goal,
                        )
                    )
                elif _parent.method_id == 2:
                    _return = (
                        _return or _child.data.agree_apportionment(
                            _parent.n_sub_systems,
                            _parent.reliability_goal,
                        )
                    )
                elif _parent.method_id == 3:
                    _return = (
                        _return or _child.data.arinc_apportionment(
                            _hazard_rates[0],
                            _parent.hazard_rate_goal,
                            _hazard_rates[_idx],
                        )
                    )
                    _idx += 1
                elif _parent.method_id == 4:
                    _return = (
                        _return or _child.data.foo_apportionment(
                            _parent.weight_factor,
                            _parent.hazard_rate_goal,
                        )
                    )
        else:
            _return = True

        if not self._test and not _return:
            _attributes = {
                'revision_id': _parent.revision_id,
                'hardware_id': _parent.hardware_id,
                'method_id': _parent.method_id,
                'goal_measure_id': _parent.goal_measure_id,
                'hazard_rate_goal': _parent.hazard_rate_goal,
                'mtbf_goal': _parent.mtbf_goal,
                'reliability_goal': _parent.reliability_goal,
            }
            pub.sendMessage('calculated_allocation', attributes=_attributes)

        return _return

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all Allocations.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Calculate all Allocations, skipping the top node in the tree.
        for _node in self.tree.all_nodes()[1:]:
            if _node.identifier != 0:
                self.do_calculate(_node.identifier, **kwargs)

        return _return

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKFailureDefinition table.

        :param int node_id: the PyPubSub Tree() ID of the Allocation to be
                            removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 1
            _msg = _msg + (
                '\n  RAMSTK ERROR: Attempted to delete non-existent '
                'Allocation ID {0:d}.'
            ).format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

            # If we're not running a test, let anyone who cares know an
            # Allocation was deleted.
            if not self._test:
                pub.sendMessage('deleted_allocation', tree=self.tree)

        return _error_code, _msg

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKAllocation table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _allocation = RAMSTKAllocation()
        _allocation.revision_id = kwargs['revision_id']
        _allocation.hardware_id = kwargs['hardware_id']
        _allocation.parent_id = kwargs['parent_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _allocation,
            ],
        )

        if _error_code == 0:
            try:
                self.tree.create_node(
                    'Allocation ID: {0:d}'.format(_allocation.hardware_id, ),
                    _allocation.hardware_id,
                    parent=_allocation.parent_id,
                    data=_allocation,
                )
                self.last_id = max(self.last_id, _allocation.hardware_id)
            except DuplicatedNodeIdError:
                _error_code = 1
                _msg = (
                    'RAMSTK ERROR: Node ID {0:s} already exists in the '
                    'Allocation tree for Hardware ID {1:s}'
                ).format(
                    str(_allocation.hardware_id),
                    str(_allocation.parent_id),
                )

            # If we're not running a test, let anyone who cares know a new
            # Allocation was inserted.
            if not self._test:
                pub.sendMessage('inserted_allocation', tree=self.tree)

        return _error_code, _msg

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Allocations from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKAllocation table in
        the connected RAMSTK Program database.  It then adds each to the
        Allocation data model treelib.Tree().

        :return: None
        :rtype: None
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _allocation in _session.query(RAMSTKAllocation).filter(
                RAMSTKAllocation.revision_id == _revision_id, ).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _allocation.get_attributes()
            _allocation.set_attributes(_attributes)
            self.tree.create_node(
                'Allocation ID: {0:d}'.format(_allocation.hardware_id, ),
                _allocation.hardware_id,
                parent=_allocation.parent_id,
                data=_allocation,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _allocation.hardware_id)
            except TypeError:
                self.last_id = _allocation.hardware_id

        _session.close()

        # If we're not running a test and there were allocations returned,
        # let anyone who cares know the Allocations have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_allocations', tree=self.tree)

    def do_select_children(self, node_id):
        """
        Select a list containing the immediate child nodes.

        :param int node_id: the Node (Hardware) ID to select the subtree for.
        :return: a list of the immediate child nodes of the passed Node
                 (Hardware) ID.
        :rtype: list
        """
        try:
            _children = self.tree.children(node_id)
        except NodeIDAbsentError:
            _children = None

        return _children

    def do_update(self, node_id):
        """
        Update the record in the RAMSTKAllocation table.

        :param int node_id: the PyPubSub Tree() ID of the Allocation to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code == 0:
            if not self._test:
                _attributes = self.do_select(node_id).get_attributes()
                pub.sendMessage('updated_allocation', attributes=_attributes)
        else:
            _error_code = 2207
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Allocation ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKAllocation records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all line items in the reliability "
                "allocation analysis worksheet."
            )

        return _error_code, _msg
