# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Third Party Imports
from pubsub import pub

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

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Hardware data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'succeed_select_revision')
        pub.subscribe(self.do_set_tree, 'succeed_calculate_all_hardware')
        pub.subscribe(self._do_delete, 'request_delete_hardware')
        pub.subscribe(self.do_insert, 'request_insert_hardware')
        pub.subscribe(self.do_update, 'request_update_hardware')
        pub.subscribe(self.do_update_all, 'request_update_all_hardware')
        pub.subscribe(self.do_make_composite_ref_des,
                      'request_make_comp_ref_des')
        pub.subscribe(self.do_get_attributes,
                      'request_get_hardware_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_hardware_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_hardware_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_hardware_attributes')
        pub.subscribe(self.do_set_all_attributes, 'succeed_calculate_hardware')

    def _do_delete(self, node_id):
        """
        Remove a Hardware item.

        :param int node_id: the node (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            RAMSTKDataManager.do_delete(self, node_id, 'hardware')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_hardware', node_id=node_id)
        except(AttributeError, DataAccessError):
            _error_msg = ("Attempted to delete non-existent hardware ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_hardware', error_msg=_error_msg)

    def do_get_all_attributes(self, node_id):
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
        _attributes = {}
        for _table in [
                'hardware', 'design_electric', 'design_mechanic',
                'mil_hdbk_217f', 'nswc', 'reliability', 'allocation',
                'similar_item'
        ]:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_hardware_attributes',
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the hardware treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_hardware_tree', dmtree=self.tree)

    def do_insert(self, parent_id, part):  # pylint: disable=arguments-differ
        """
        Add a new hardware item.

        :param int parent_id: the parent hardware item'd ID.
        :param int part: whether to insert a part (1) or assembly (0).
        :return: None
        :rtype: None
        """
        _parent = self.do_select(parent_id, table='hardware')
        if parent_id != 0 and _parent.part == 1:
            pub.sendMessage('fail_insert_hardware',
                            error_msg=("Attempting to insert a hardware "
                                       "assembly or component/piece part as a "
                                       "child of another component/piece "
                                       "part."))
        else:
            try:
                _hardware = RAMSTKHardware(revision_id=self._revision_id,
                                           parent_id=parent_id,
                                           part=part)

                self.dao.do_insert(_hardware)

                self.last_id = _hardware.hardware_id

                _design_e = RAMSTKDesignElectric(hardware_id=self.last_id)
                _design_m = RAMSTKDesignMechanic(hardware_id=self.last_id)
                _milhdbkf = RAMSTKMilHdbkF(hardware_id=self.last_id)
                _nswc = RAMSTKNSWC(hardware_id=self.last_id)
                _reliability = RAMSTKReliability(hardware_id=self.last_id)
                _allocation = RAMSTKAllocation(revision_id=self._revision_id,
                                               hardware_id=self.last_id,
                                               parent_id=parent_id)
                _similaritem = RAMSTKSimilarItem(revision_id=self._revision_id,
                                                 hardware_id=self.last_id,
                                                 parent_id=parent_id)

                self.dao.do_insert_many(
                    [_design_e, _design_m, _milhdbkf, _nswc, _reliability,
                     _allocation, _similaritem])

                _data_package = {
                    'hardware': _hardware,
                    'design_electric': _design_e,
                    'design_mechanic': _design_m,
                    'mil_hdbk_217f': _milhdbkf,
                    'nswc': _nswc,
                    'reliability': _reliability,
                    'allocation': _allocation,
                    'similar_item': _similaritem
                }
                self.tree.create_node(tag=_hardware.comp_ref_des,
                                      identifier=_hardware.hardware_id,
                                      parent=parent_id,
                                      data=_data_package)

                pub.sendMessage('inserted_hardware', tree=self.tree)
                pub.sendMessage('succeed_insert_hardware',
                                node_id=self.last_id)
            except DataAccessError as _error:
                print(_error)
                pub.sendMessage("fail_insert_hardware", error_message=_error)

    def do_make_composite_ref_des(self, node_id=1):
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
            _node.tag = _p_comp_ref_des + ':' + _node.data[
                'hardware'].ref_des
        else:
            _node.data['hardware'].comp_ref_des = _node.data[
                'hardware'].ref_des
            _node.tag = _node.data['hardware'].ref_des

        # Now make the composite reference designator for all the child nodes.
        for _child_node in self.tree.children(node_id):
            self.do_make_composite_ref_des(node_id=_child_node.identifier)

    def do_select_all(self, revision_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Hardware BoM for.
        :return: None
        :rtype: None
        """
        self._revision_id = revision_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hardware in self.dao.session.query(RAMSTKHardware).filter(
                RAMSTKHardware.revision_id == self._revision_id).all():

            _design_e = self.dao.session.query(RAMSTKDesignElectric).filter(
                RAMSTKDesignElectric.hardware_id ==
                _hardware.hardware_id).first()

            _design_m = self.dao.session.query(RAMSTKDesignMechanic).filter(
                RAMSTKDesignMechanic.hardware_id ==
                _hardware.hardware_id).first()

            _milhdbkf = self.dao.session.query(RAMSTKMilHdbkF).filter(
                RAMSTKMilHdbkF.hardware_id == _hardware.hardware_id).first()

            _nswc = self.dao.session.query(RAMSTKNSWC).filter(
                RAMSTKNSWC.hardware_id == _hardware.hardware_id).first()

            _reliability = self.dao.session.query(RAMSTKReliability).filter(
                RAMSTKReliability.hardware_id ==
                _hardware.hardware_id).first()

            _allocation = self.dao.session.query(RAMSTKAllocation).filter(
                RAMSTKAllocation.hardware_id ==
                _hardware.hardware_id).first()

            _similaritem = self.dao.session.query(RAMSTKSimilarItem).filter(
                RAMSTKSimilarItem.hardware_id ==
                _hardware.hardware_id).first()

            _data_package = {
                'hardware': _hardware,
                'design_electric': _design_e,
                'design_mechanic': _design_m,
                'mil_hdbk_217f': _milhdbkf,
                'nswc': _nswc,
                'reliability': _reliability,
                'allocation': _allocation,
                'similar_item': _similaritem
            }

            self.tree.create_node(tag=_hardware.comp_ref_des,
                                  identifier=_hardware.hardware_id,
                                  parent=_hardware.parent_id,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_hardware', tree=self.tree)

    def do_set_all_attributes(self, attributes):
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
            self.do_set_attributes(attributes['hardware_id'], _key,
                                   attributes[_key])

    def do_set_attributes(self, node_id, key, value):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :return: None
        :rtype: None
        """
        for _table in [
                'hardware', 'design_electric', 'design_mechanic',
                'mil_hdbk_217f', 'nswc', 'reliability', 'allocation',
                'similar_item'
        ]:
            _attributes = self.do_select(node_id,
                                         table=_table).get_attributes()
            if key in _attributes:
                _attributes[key] = value

                try:
                    _attributes.pop('revision_id')
                except KeyError:
                    pass
                _attributes.pop('hardware_id')

                self.do_select(node_id,
                               table=_table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the hardware ID of the hardware item to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.session.add(self.tree.get_node(node_id).data['hardware'])
            self.dao.session.add(
                self.tree.get_node(node_id).data['design_electric'])
            self.dao.session.add(
                self.tree.get_node(node_id).data['design_mechanic'])
            self.dao.session.add(
                self.tree.get_node(node_id).data['mil_hdbk_217f'])
            self.dao.session.add(self.tree.get_node(node_id).data['nswc'])
            self.dao.session.add(
                self.tree.get_node(node_id).data['reliability'])
            self.dao.session.add(
                self.tree.get_node(node_id).data['allocation'])
            self.dao.do_update()

            pub.sendMessage('succeed_update_hardware', node_id=node_id)
        except(AttributeError, DataAccessError):
            pub.sendMessage('fail_update_hardware',
                            error_msg=('Attempted to save non-existent '
                                       'hardware item with hardware ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_hardware',
                                error_msg=('No data package found for '
                                           'hardware ID {0:s}.').format(
                                               str(node_id)))
