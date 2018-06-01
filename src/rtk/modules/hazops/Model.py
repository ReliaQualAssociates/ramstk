# -*- coding: utf-8 -*-
#
#       rtk.modules.hazard_analysis.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hazard Analysis Data Model."""

from treelib import tree

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

    def select_all(self, revision_id):
        """
        Retrieve all the Hazard Analysis from the RTK Program database.

        This method retrieves all the records from the RTKHazardAnalysis table
        in the connected RTK Program database.  It then adds each to the
        HazardAnalysis data model treelib.Tree().

        :param int revision_id: the Revision ID the Hazard Analysis are
                                associated with.
        :return: tree; the Tree() of RTKHazardAnalysis data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _hazard_analysis in _session.query(RTKHazardAnalysis).filter(
                RTKHazardAnalysis.revision_id == revision_id).all():
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

    def select_children(self, node_id):
        """
        Select a list containing the immediate child nodes.

        :param int node_id: the Node (Hardware) ID to select the subtree for.
        :return: a list of the immediate child nodes of the passed Node
                 (Hardware) ID.
        :rtype: list
        """
        return self.tree.children(node_id)

    def insert(self, **kwargs):
        """
        Add a record to the RTKHazardAnalysis table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _hazard_analysis = RTKHazardAnalysis()
        _hazard_analysis.revision_id = kwargs['revision_id']
        _hazard_analysis.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(
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

    def delete(self, node_id):
        """
        Remove a record from the RTKHazardAnalysis table.

        :param int node_id: the ID of the Hazard Analysis to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Hazard Analysis ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the selected HazOps in the RTKHazardAnalysis table.

        :param int node_id: the HazOps ID to save to the RTK Program
                            database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2207
            _msg = 'RTK ERROR: Attempted to save non-existent Hazard ' \
                   'Analysis ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self, module_id):
        """
        Update all RTKHazardAnalysis records for the selected Hardware item.

        :param int module_id: the ID of the Hardware item to save the HazOps for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating the RTK Program database."

        for _node in self.select_children(module_id):
            try:
                _id = '{0:d}.{1:d}'.format(_node.data.hardware_id,
                                           _node.data.hazard_id)
                _error_code, _err_msg = self.update(_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.hazard_analysis.Model.update_all().'

            except AttributeError:
                if _node.data is None:
                    _msg = _msg + ('RTK ERROR: No data package for Node ID: '
                                   '{0:d}.\n').format(_node.identifier)
                else:
                    _msg = _msg + ('RTK ERROR: Attempt to save Node ID: '
                                   '{0:d}.{1:d} failed.\n').format(
                                       _node.data.hardware_id,
                                       _node.data.hazard_id)

        return _error_code, _msg

    def calculate(self, node_id):
        """
        Calculate the HRIs for the selected hazard.

        :param int node_id: the Node (Hazard) ID of the hardware item whose
                            goal is to be allocated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hazard = self.select(node_id)

        return _hazard.calculate()
