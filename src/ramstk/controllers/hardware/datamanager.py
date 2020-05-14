# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAllocation, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability, RAMSTKSimilarItem
)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Hardware data manager.

    This class manages the hardware data from the RAMSTKHardware,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKMilHdbkF, RAMSTKNSWC, and
    RAMSKTReliability data models.
    """

    _tag = 'hardware'
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_tree, 'succeed_calculate_all_hardware')
        pub.subscribe(self.do_update, 'request_update_hardware')
        pub.subscribe(self.do_update_all, 'request_update_all_hardware')
        pub.subscribe(self.do_get_attributes,
                      'request_get_hardware_attributes')

        pub.subscribe(self._do_select_all_hardware, 'selected_revision')
        pub.subscribe(self._do_delete_hardware, 'request_delete_hardware')
        pub.subscribe(self._do_insert_hardware, 'request_insert_hardware')
        pub.subscribe(self._do_set_hardware_attributes,
                      'request_set_hardware_attributes')
        pub.subscribe(self._do_set_hardware_attributes,
                      'wvw_editing_component')
        pub.subscribe(self._do_set_hardware_attributes, 'wvw_editing_hardware')
        pub.subscribe(self._do_set_all_hardware_attributes,
                      'succeed_calculate_hardware')
        pub.subscribe(self._do_get_all_hardware_attributes,
                      'request_get_all_hardware_attributes')
        pub.subscribe(self._do_get_hardware_tree, 'request_get_hardware_tree')
        pub.subscribe(self._do_make_composite_ref_des,
                      'request_make_comp_ref_des')

    def _do_delete_hardware(self, node_id: int) -> None:
        """
        Remove a Hardware item.

        :param int node_id: the node (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'hardware')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_hardware',
                            node_id=node_id,
                            tree=self.tree)
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_msg = ("Attempted to delete non-existent hardware ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_hardware', error_message=_error_msg)

    def _do_get_all_hardware_attributes(self, node_id: int) -> None:
        """
        Retrieve all RAMSTK data tables' attributes for the hardware item.

        This is a helper method to be able to retrieve all the hardware item's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (hardware) ID of the hardware item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = {}
        for _table in [
                'hardware', 'design_electric', 'design_mechanic',
                'mil_hdbk_217f', 'nswc', 'reliability', 'allocation',
                'similar_item'
        ]:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_hardware_attributes',
                        attributes=_attributes)

    def _do_get_hardware_tree(self) -> None:
        """
        Retrieve the hardware treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_hardware_tree', dmtree=self.tree)

    def _do_insert_hardware(self, parent_id: int, part: int) -> None:
        """
        Add a new hardware item.

        :param int parent_id: the parent hardware item'd ID.
        :param int part: whether to insert a part (1) or assembly (0).
        :return: None
        :rtype: None
        """
        _parent = self.do_select(parent_id, table='hardware')
        if parent_id != 0 and _parent.part == 1:
            pub.sendMessage(
                'fail_insert_hardware',
                error_message=("Attempting to insert a hardware "
                               "assembly or component/piece part as a "
                               "child of another component/piece "
                               "part."))
        else:
            try:
                _hardware = RAMSTKHardware()
                _hardware.revision_id = self._revision_id
                _hardware.hardware_id = self.last_id + 1
                _hardware.parent_id = parent_id
                _hardware.part = part

                self.dao.do_insert(_hardware)

                self.last_id = _hardware.hardware_id

                _design_e = RAMSTKDesignElectric()
                _design_e.hardware_id = self.last_id
                _design_m = RAMSTKDesignMechanic()
                _design_m.hardware_id = self.last_id
                _milhdbkf = RAMSTKMilHdbkF()
                _milhdbkf.hardware_id = self.last_id
                _nswc = RAMSTKNSWC()
                _nswc.hardware_id = self.last_id
                _reliability = RAMSTKReliability()
                _reliability.hardware_id = self.last_id
                _allocation = RAMSTKAllocation()
                _allocation.revision_id = self._revision_id
                _allocation.hardware_id = self.last_id
                _allocation.parent_id = parent_id
                _similaritem = RAMSTKSimilarItem()
                _similaritem.revision_id = self._revision_id
                _similaritem.hardware_id = self.last_id
                _similaritem.parent_id = parent_id

                self.dao.do_insert_many([
                    _design_e, _design_m, _milhdbkf, _nswc, _reliability,
                    _allocation, _similaritem
                ])

                self.tree.create_node(tag=_hardware.comp_ref_des,
                                      identifier=_hardware.hardware_id,
                                      parent=parent_id,
                                      data={
                                          'hardware': _hardware,
                                          'design_electric': _design_e,
                                          'design_mechanic': _design_m,
                                          'mil_hdbk_217f': _milhdbkf,
                                          'nswc': _nswc,
                                          'reliability': _reliability,
                                          'allocation': _allocation,
                                          'similar_item': _similaritem
                                      })

                pub.sendMessage('inserted_hardware', tree=self.tree)
                pub.sendMessage('succeed_insert_hardware',
                                node_id=self.last_id,
                                tree=self.tree)
            except DataAccessError as _error:
                pub.sendMessage("fail_insert_hardware", error_message=_error)

    def _do_make_composite_ref_des(self, node_id: int = 1) -> None:
        """
        Make the composite reference designators.

        :keyword int node_id: the ID of the node to start making the composite
            reference designators.
        :return: None
        :rtype: None
        """
        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)
        if _node.bpointer != 0:
            _p_comp_ref_des = self.do_select(_node.bpointer,
                                             table='hardware').comp_ref_des
        else:
            _p_comp_ref_des = ''

        if _p_comp_ref_des != '':
            _node.data[
                'hardware'].comp_ref_des = _p_comp_ref_des + ':' + _node.data[
                    'hardware'].ref_des
            _node.tag = _p_comp_ref_des + ':' + _node.data['hardware'].ref_des
        else:
            _node.data['hardware'].comp_ref_des = _node.data[
                'hardware'].ref_des
            _node.tag = _node.data['hardware'].ref_des

        # Now make the composite reference designator for all the child nodes.
        for _child_node in self.tree.children(node_id):
            self._do_make_composite_ref_des(node_id=_child_node.identifier)

    def _do_select_all_hardware(self, attributes: Dict[str, Any]) -> None:
        """
        Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param dict revision_id: the Revision ID to select the Hardware BoM
            for.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hardware in self.dao.do_select_all(
                RAMSTKHardware,
                key=RAMSTKHardware.revision_id,
                value=self._revision_id,
                order=RAMSTKHardware.parent_id):

            _design_e = self.dao.do_select_all(
                RAMSTKDesignElectric,
                key=RAMSTKDesignElectric.hardware_id,
                value=_hardware.hardware_id,
                order=None,
                _all=False)

            _design_m = self.dao.do_select_all(
                RAMSTKDesignMechanic,
                key=RAMSTKDesignMechanic.hardware_id,
                value=_hardware.hardware_id,
                order=None,
                _all=False)

            _milhdbkf = self.dao.do_select_all(RAMSTKMilHdbkF,
                                               key=RAMSTKMilHdbkF.hardware_id,
                                               value=_hardware.hardware_id,
                                               order=None,
                                               _all=False)

            _nswc = self.dao.do_select_all(RAMSTKNSWC,
                                           key=RAMSTKNSWC.hardware_id,
                                           value=_hardware.hardware_id,
                                           order=None,
                                           _all=False)

            _reliability = self.dao.do_select_all(
                RAMSTKReliability,
                key=RAMSTKReliability.hardware_id,
                value=_hardware.hardware_id,
                order=None,
                _all=False)

            _allocation = self.dao.do_select_all(
                RAMSTKAllocation,
                key=RAMSTKAllocation.hardware_id,
                value=_hardware.hardware_id,
                order=None,
                _all=False)

            _similaritem = self.dao.do_select_all(
                RAMSTKSimilarItem,
                key=RAMSTKSimilarItem.hardware_id,
                value=_hardware.hardware_id,
                order=None,
                _all=False)

            self.tree.create_node(tag=_hardware.comp_ref_des,
                                  identifier=_hardware.hardware_id,
                                  parent=_hardware.parent_id,
                                  data={
                                      'hardware': _hardware,
                                      'design_electric': _design_e,
                                      'design_mechanic': _design_m,
                                      'mil_hdbk_217f': _milhdbkf,
                                      'nswc': _nswc,
                                      'reliability': _reliability,
                                      'allocation': _allocation,
                                      'similar_item': _similaritem
                                  })

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_hardware', tree=self.tree)

    def _do_set_all_hardware_attributes(self,
                                        attributes: Dict[str, Any]) -> None:
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the hardware
            item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self._do_set_hardware_attributes(
                node_id=[attributes['hardware_id'], -1],
                package={_key: attributes[_key]})

    def _do_set_hardware_attributes(self,
                                    node_id: List[int],
                                    package: Dict[str, Any]) -> None:
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        for _table in [
                'hardware', 'design_electric', 'design_mechanic',
                'mil_hdbk_217f', 'nswc', 'reliability', 'allocation',
                'similar_item'
        ]:
            _attributes = self.do_select(node_id[0],
                                         table=_table).get_attributes()

            if _key in _attributes:
                _attributes[_key] = _value

                # Only the ramstk_hardware table contains the revision_id
                # column.
                try:
                    _attributes.pop('revision_id')
                except KeyError:
                    pass
                _attributes.pop('hardware_id')

                self.do_select(node_id[0],
                               table=_table).set_attributes(_attributes)

    def do_update(self, node_id: int) -> None:
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the hardware ID of the hardware item to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['hardware'])
            self.dao.do_update(
                self.tree.get_node(node_id).data['design_electric'])
            self.dao.do_update(
                self.tree.get_node(node_id).data['design_mechanic'])
            self.dao.do_update(
                self.tree.get_node(node_id).data['mil_hdbk_217f'])
            self.dao.do_update(self.tree.get_node(node_id).data['nswc'])
            self.dao.do_update(self.tree.get_node(node_id).data['reliability'])
            self.dao.do_update(self.tree.get_node(node_id).data['allocation'])

            pub.sendMessage('succeed_update_hardware', node_id=node_id)
        except (AttributeError, DataAccessError):
            pub.sendMessage('fail_update_hardware',
                            error_message=('Attempted to save non-existent '
                                           'hardware item with hardware ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_hardware',
                                error_message=('No data package found for '
                                               'hardware ID {0:s}.').format(
                                                   str(node_id)))
