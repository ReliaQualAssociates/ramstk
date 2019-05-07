# -*- coding: utf-8 -*-
#
#       ramstk.modules.hazops.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hazard Analysis Data Model."""

# Import third party packages.
from pubsub import pub
from treelib import tree
from treelib.exceptions import NodeIDAbsentError

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataModel
from ramstk.dao import RAMSTKHazardAnalysis


class HazardAnalysisDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a Hazard Analysis."""

    _tag = 'HazardAnalysis'

    def __init__(self, dao, **kwargs):
        """
        Initialize a Hazard Analysis data model instance.

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

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Hazard Analysis from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKHazardAnalysis
        table in the connected RAMSTK Program database.  It then adds each to
        the HazardAnalysis data model treelib.Tree().

        :param int hardware_id: the Hardware ID the Hazards are associated
                                with.
        :return: tree; the Tree() of RAMSTKHazardAnalysis data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _hazard_analysis in _session.query(RAMSTKHazardAnalysis).filter(
                RAMSTKHazardAnalysis.revision_id == _revision_id).all():
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
                parent=_hazard_analysis.hardware_id,
                data=_hazard_analysis)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _hazard_analysis.hazard_id)

        _session.close()

        # If we're not running a test and there were hazards returned,
        # let anyone who cares know the Hazards have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_hazards', tree=self.tree)

        return None

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
        Add a record to the RAMSTKHazardAnalysis table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _hazard_analysis = RAMSTKHazardAnalysis()
        _hazard_analysis.revision_id = kwargs['revision_id']
        _hazard_analysis.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _hazard_analysis,
            ])

        _id = '{0:d}.{1:d}'.format(_hazard_analysis.hardware_id,
                                   _hazard_analysis.hazard_id)
        try:
            self.tree.create_node(
                _hazard_analysis.potential_hazard,
                _id,
                parent=_hazard_analysis.hardware_id,
                data=_hazard_analysis)
        except tree.NodeIDAbsentError:
            self.tree.create_node(
                _hazard_analysis.potential_hazard,
                _hazard_analysis.hardware_id,
                parent=0,
                data=None)
            self.tree.create_node(
                _hazard_analysis.potential_hazard,
                _id,
                parent=_hazard_analysis.hardware_id,
                data=_hazard_analysis)

        self.last_id = max(self.last_id, _hazard_analysis.hazard_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKHazardAnalysis table.

        :param int node_id: the ID of the Hazard Analysis to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Hazard Analysis ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the selected HazOps in the RAMSTKHazardAnalysis table.

        :param str node_id: the HazOps ID to save to the RAMSTK Program
                            database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)
        print(_error_code, _msg)
        if _error_code != 0:
            _error_code = 2207
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Hazard ' \
                   'Analysis ID {0:s}.'.format(str(node_id))

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKHazardAnalysis records for the selected Hardware item.

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
                _msg = (
                    "RAMSTK ERROR: One or more records in the HazOps table "
                    "for Hardware ID {0:d} did not "
                    "update.").format(_hardware_id)
            except NodeIDAbsentError:
                pass

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all records in the HazOps table "
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
