# -*- coding: utf-8 -*-
#
#       rtk.modules.hazops.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hazard Analysis Data Model."""

from treelib import tree
from treelib.exceptions import NodeIDAbsentError

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKHazardAnalysis


class HazardAnalysisDataModel(RTKDataModel):
    """Contain the attributes and methods of a Hazard Analysis."""

    _tag = 'HazardAnalysis'

    def __init__(self, dao):
        """
        Initialize a Hazard Analysis data model instance.

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
        Retrieve all the Hazard Analysis from the RTK Program database.

        This method retrieves all the records from the RTKHazardAnalysis table
        in the connected RTK Program database.  It then adds each to the
        HazardAnalysis data model treelib.Tree().

        :param int hardware_id: the Hardware ID the Hazards are associated
                                with.
        :return: tree; the Tree() of RTKHazardAnalysis data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RTKDataModel.do_select_all(self)

        for _hazard_analysis in _session.query(RTKHazardAnalysis).filter(
                RTKHazardAnalysis.revision_id == _revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _hazard_analysis.get_attributes()
            _hazard_analysis.set_attributes(_attributes)
            try:
                self.tree.create_node(
                    'Hardware ID: {0:d}'.format(_hazard_analysis.hardware_id),
                    _hazard_analysis.hardware_id,
                    0,
                    data=None)
            except tree.DuplicatedNodeIdError:
                pass
            _id = '{0:d}.{1:d}'.format(_hazard_analysis.hardware_id,
                                       _hazard_analysis.hazard_id)
            self.tree.create_node(
                _hazard_analysis.potential_hazard,
                _id,
                _hazard_analysis.hardware_id,
                data=_hazard_analysis)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _hazard_analysis.hazard_id)

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
        try:
            _children = self.tree.subtree(node_id)
        except NodeIDAbsentError:
            _children = None

        return _children

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKHazardAnalysis table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _hazard_analysis = RTKHazardAnalysis()
        _hazard_analysis.revision_id = kwargs['revision_id']
        _hazard_analysis.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _hazard_analysis,
            ])

        _id = '{0:d}.{1:d}'.format(_hazard_analysis.hardware_id,
                                   _hazard_analysis.hazard_id)
        self.tree.create_node(
            _hazard_analysis.potential_hazard,
            _id,
            parent=_hazard_analysis.hardware_id,
            data=_hazard_analysis)

        self.last_id = max(self.last_id, _hazard_analysis.hazard_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RTKHazardAnalysis table.

        :param int node_id: the ID of the Hazard Analysis to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Hazard Analysis ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the selected HazOps in the RTKHazardAnalysis table.

        :param str node_id: the HazOps ID to save to the RTK Program
                            database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)
        print _error_code, _msg
        if _error_code != 0:
            _error_code = 2207
            _msg = 'RTK ERROR: Attempted to save non-existent Hazard ' \
                   'Analysis ID {0:s}.'.format(str(node_id))

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RTKHazardAnalysis records for the selected Hardware item.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hardware_id = kwargs['hardware_id']
        _error_code = 0
        _msg = ''

        for _node in self.do_select_children(_hardware_id).all_nodes()[1:]:
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)
                _msg = _msg + _debug_msg + '\n'
            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more records in the HazOps table "
                        "for Hardware ID {0:d} did not "
                        "update.").format(_hardware_id)
            except NodeIDAbsentError:
                pass

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all records in the HazOps table "
                    "for Hardware ID {0:d}.").format(_hardware_id)

        return _error_code, _msg

    def do_calculate(self, node_id, **kwargs):  # pylint: disable=unused-argument
        """
        Calculate the HRIs for the selected hazard.

        :param int node_id: the Node (Hazard) ID of the hardware item whose
                            goal is to be allocated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hazard = self.do_select(node_id)

        return _hazard.calculate()

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all Similar Item analysis.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Calculate all Similar Items, skipping the top node in the tree.
        for _node in self.tree.all_nodes():
            if _node.identifier != 0:
                self.do_calculate(_node.identifier, **kwargs)

        return _return
