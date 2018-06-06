# -*- coding: utf-8 -*-
#
#       rtk.analyses.allocation.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Models."""

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKAllocation


class AllocationDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a reliability allocation.

    An RTK Project will consist of one or more Modes.  The attributes of a
    Mode are:
    """

    _tag = 'Allocations'

    def __init__(self, dao):
        """
        Initialize a Allocation data model instance.

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

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Allocations from the RTK Program database.

        This method retrieves all the records from the RTKAllocation table in
        the connected RTK Program database.  It then adds each to the
        Allocation data model treelib.Tree().

        :return: tree; the Tree() of RTKAllocation data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RTKDataModel.do_select_all(self)

        for _allocation in _session.query(RTKAllocation).filter(
                RTKAllocation.revision_id == _revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _allocation.get_attributes()
            _allocation.set_attributes(_attributes)
            self.tree.create_node(
                'Allocation ID: {0:d}'.format(_allocation.hardware_id),
                _allocation.hardware_id,
                parent=_allocation.parent_id,
                data=_allocation)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _allocation.hardware_id)

        _session.close()

        return self.tree

    def do_select_children(self, node_id):
        """
        Select a list containing the immediate child nodes.

        :param int node_id: the Node (Hardware) ID to select the subtree for.
        :return: a list of the immediate child nodes of the passed Node
                 (Hardware) ID.
        :rtype: list
        """
        return self.tree.children(node_id)

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKAllocation table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _allocation = RTKAllocation()
        _allocation.revision_id = kwargs['revision_id']
        _allocation.hardware_id = kwargs['hardware_id']
        _allocation.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _allocation,
            ])

        self.tree.create_node(
            'Allocation ID: {0:d}'.format(_allocation.hardware_id),
            _allocation.hardware_id,
            parent=_allocation.parent_id,
            data=_allocation)

        self.last_id = max(self.last_id, _allocation.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RTKFailureDefinition table.

        :param int node_id: the PyPubSub Tree() ID of the Allocation to be
                            removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Allocation ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record in the RTKAllocation table.

        :param int node_id: the PyPubSub Tree() ID of the Allocation to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2207
            _msg = 'RTK ERROR: Attempted to save non-existent Allocation ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKAllocation records.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.do_update(_node.data.hardware_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.allocation.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.analyses.allocation.Model.update_all().'

        return _error_code, _msg

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
                    _return = (_return or _child.data.equal_apportionment(
                        _parent.n_sub_systems, _parent.reliability_goal))
                elif _parent.method_id == 2:
                    _return = (_return or _child.data.agree_apportionment(
                        _parent.n_sub_systems, _parent.reliability_goal))
                elif _parent.method_id == 3:
                    _return = (_return or _child.data.arinc_apportionment(
                        _hazard_rates[0], _parent.hazard_rate_goal,
                        _hazard_rates[_idx]))
                    _idx += 1
                elif _parent.method_id == 4:
                    _return = (_return or _child.data.foo_apportionment(
                        _parent.weight_factor, _parent.hazard_rate_goal))
        else:
            _return = True

        return _return

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all Allocations.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Calculate all Allocations, skipping the top node in the tree.
        for _node in self.tree.all_nodes():
            if _node.identifier != 0:
                self.do_calculate(_node.identifier, **kwargs)

        return _return
