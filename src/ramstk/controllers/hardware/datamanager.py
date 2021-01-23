# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.hardware.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability
)


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Hardware data manager.

    This class manages the hardware data from the RAMSTKHardware,
    RAMSTKDesignElectric, and RAMSTKDesignMechanic data models.
    """

    _tag: str = 'hardwares'
    _root: int = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            'hardware': ['revision_id', 'hardware_id'],
            'design_electric': ['revision_id', 'hardware_id'],
            'design_mechanic': ['revision_id', 'hardware_id'],
            'mil_hdbk_217f': ['revision_id', 'hardware_id'],
            'nswc': ['revision_id', 'hardware_id'],
            'reliability': ['revision_id', 'hardware_id'],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_hardware_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_hardware_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_component')
        pub.subscribe(super().do_set_attributes, 'mvw_editing_hardware')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_hardware')
        pub.subscribe(super().do_update_all, 'request_update_all_hardwares')

        pub.subscribe(self.do_get_tree, 'request_get_hardwares_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_set_all_attributes,
                      'succeed_predict_reliability')
        pub.subscribe(self.do_update, 'request_update_hardware')

        pub.subscribe(self._do_delete, 'request_delete_hardware')
        pub.subscribe(self._do_get_all_attributes,
                      'request_get_all_hardware_attributes')
        pub.subscribe(self._do_insert_hardware, 'request_insert_hardware')
        pub.subscribe(self._do_make_composite_ref_des,
                      'request_make_comp_ref_des')

    def do_get_tree(self) -> None:
        """Retrieve the hardware treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_hardwares_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hardware in self.dao.do_select_all(
                RAMSTKHardware,
                key=['revision_id'],
                value=[self._revision_id],
                order=[RAMSTKHardware.parent_id, RAMSTKHardware.ref_des]):

            _design_e = self._do_select_electrical(_hardware.hardware_id)
            _design_m = self._do_select_mechanical(_hardware.hardware_id)
            _milhdbkf = self._do_select_milhdbk217f(_hardware.hardware_id)
            _nswc = self._do_select_nswc(_hardware.hardware_id)
            _reliability = self._do_select_reliability(_hardware.hardware_id)

            self.tree.create_node(tag='hardware',
                                  identifier=_hardware.hardware_id,
                                  parent=_hardware.parent_id,
                                  data={
                                      'hardware': _hardware,
                                      'design_electric': _design_e,
                                      'design_mechanic': _design_m,
                                      'mil_hdbk_217f': _milhdbkf,
                                      'nswc': _nswc,
                                      'reliability': _reliability
                                  })

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_hardware',
            tree=self.tree,
        )

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the selected hardware item.

        This is a helper method to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the hardware item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(node_id=[attributes['hardware_id'], ''],
                                      package={_key: attributes[_key]})

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the hardware ID of the hardware item to save.
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

            pub.sendMessage(
                'succeed_update_hardware',
                tree=self.tree,
            )
        except AttributeError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: Attempted to save non-existent hardware '
                          'ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_hardware',
                error_message=_error_msg,
            )
        except KeyError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: No data package found for hardware ID '
                          '{0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_hardware',
                error_message=_error_msg,
            )
        except TypeError:
            if node_id != 0:
                _method_name: str = inspect.currentframe(  # type: ignore
                ).f_code.co_name
                _error_msg = ('{1}: The value for one or more attributes for '
                              'hardware ID {0} was the wrong type.').format(
                                  str(node_id), _method_name)
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_hardware',
                    error_message=_error_msg,
                )

    def _do_select_electrical(self, hardware_id: int) -> RAMSTKDesignElectric:
        """Select the electrical attributes for hardware ID.

        :param hardware_id: the ID of the hardware item whose electrical
            attributes are needed.
        :return: the RAMSTKDesignElectric() record for the hardware ID.
        :rtype: RAMSTKDesignElectric
        """
        return self.dao.do_select_all(RAMSTKDesignElectric,
                                      key=['hardware_id'],
                                      value=[hardware_id],
                                      order=None,
                                      _all=False)

    def _do_select_mechanical(self, hardware_id: int) -> RAMSTKDesignMechanic:
        """Select the mechanical attributes for hardware ID.

        :param hardware_id: the ID of the hardware item whose mechanical
            attributes are needed.
        :return: the RAMSTKDesignMechanic() record for the hardware ID.
        :rtype: RAMSTKDesignMechanic
        """
        return self.dao.do_select_all(RAMSTKDesignMechanic,
                                      key=['hardware_id'],
                                      value=[hardware_id],
                                      order=None,
                                      _all=False)

    def _do_select_milhdbk217f(self, hardware_id: int) -> RAMSTKMilHdbkF:
        """Select the MIL-HDBK-217F attributes for hardware ID.

        :param hardware_id: the ID of the hardware item whose MIL-HDBK-217F
            attributes are needed.
        :return: the RAMSTKMilHdbkF() record for the hardware ID.
        :rtype: RAMSTKDesignMilHdbkF
        """
        return self.dao.do_select_all(RAMSTKMilHdbkF,
                                      key=['hardware_id'],
                                      value=[hardware_id],
                                      order=None,
                                      _all=False)

    def _do_select_nswc(self, hardware_id: int) -> RAMSTKNSWC:
        """Select the NSWC attributes for hardware ID.

        :param hardware_id: the ID of the hardware item whose NSWC
            attributes are needed.
        :return: the RAMSTKNSWC() record for the hardware ID.
        :rtype: RAMSTKSWC
        """
        return self.dao.do_select_all(RAMSTKNSWC,
                                      key=['hardware_id'],
                                      value=[hardware_id],
                                      order=None,
                                      _all=False)

    def _do_select_reliability(self, hardware_id: int) -> RAMSTKReliability:
        """Select the reliability attributes for hardware ID.

        :param hardware_id: the ID of the hardware item whose reliability
            attributes are needed.
        :return: the RAMSTKReliability() record for the hardware ID.
        :rtype: RAMSTKReliability
        """
        return self.dao.do_select_all(RAMSTKReliability,
                                      key=['hardware_id'],
                                      value=[hardware_id],
                                      order=None,
                                      _all=False)

    def _do_delete(self, node_id: int) -> None:
        """Remove a Hardware item.

        :param node_id: the node (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            # Delete the children (if any), then the parent node that was
            # passed.
            for _child in self.tree.children(node_id):
                super().do_delete(_child.identifier, 'hardware')
            super().do_delete(node_id, 'hardware')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_hardware',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent hardware ID {0}.'
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_hardware',
                error_message=_error_msg,
            )

    def _do_get_all_attributes(self, node_id: int) -> None:
        """Retrieve all RAMSTK data tables' attributes for the hardware item.

        This is a helper method to be able to retrieve all the hardware item's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param node_id: the node (hardware) ID of the hardware item to get the
            attributes for.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = {}
        for _table in [
                'hardware', 'design_electric', 'design_mechanic',
                'mil_hdbk_217f', 'nswc', 'reliability'
        ]:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage(
            'succeed_get_all_hardware_attributes',
            attributes=_attributes,
        )

    def _do_insert_hardware(self, parent_id: int, part: int) -> None:
        """Add a new hardware item.

        :param parent_id: the parent hardware item ID.
        :param part: whether to insert a part (1) or assembly (0).
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

                self.dao.do_insert_many(
                    [_design_e, _design_m, _milhdbkf, _nswc, _reliability])

                self.tree.create_node(tag='hardware',
                                      identifier=_hardware.hardware_id,
                                      parent=parent_id,
                                      data={
                                          'hardware': _hardware,
                                          'design_electric': _design_e,
                                          'design_mechanic': _design_m,
                                          'mil_hdbk_217f': _milhdbkf,
                                          'nswc': _nswc,
                                          'reliability': _reliability
                                      })

                pub.sendMessage(
                    'succeed_insert_hardware',
                    node_id=self.last_id,
                    tree=self.tree,
                )
                pub.sendMessage(
                    'request_insert_allocation',
                    hardware_id=self.last_id,
                    parent_id=parent_id,
                )
                pub.sendMessage(
                    'request_insert_similar_item',
                    hardware_id=self.last_id,
                    parent_id=parent_id,
                )
            except DataAccessError as _error:
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error.msg,
                )
                pub.sendMessage(
                    "fail_insert_hardware",
                    error_message=_error.msg,
                )

    def _do_make_composite_ref_des(self, node_id: int = 1) -> None:
        """Make the composite reference designators.

        :param node_id: the ID of the node to start making the composite
            reference designators.
        :return: None
        :rtype: None
        """
        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)

        if _node.predecessor(self.tree.identifier) != 0:
            _p_comp_ref_des = self.do_select(_node.predecessor(
                self.tree.identifier),
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

        _attributes = _node.data['hardware'].get_attributes()
        pub.sendMessage('succeed_create_comp_ref_des', attributes=_attributes)
