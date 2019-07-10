# -*- coding: utf-8 -*-
#
#       ramstk.modules.hardware.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.Exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability
)
from ramstk.modules import RAMSTKDataModel


class DataManager(RAMSTKDataModel):
    """
    Contain the attributes and methods of the Hardware data manager.

    This class manages the hardware data from the RAMSTKHardware,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKMilHdbkF, RAMSTKNSWC, and
    RAMSKTReliability data models.
    """

    _tag = 'HardwareBoM'
    _root = 0

    def __init__(self, dao, configuration, **kwargs):   # pylint: disable=unused-argument
        """
        Initialize a Hardware data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_CONFIGURATION = configuration

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'succeed_select_revision')
        pub.subscribe(self.do_delete, 'request_delete_hardware')
        pub.subscribe(self.do_insert, 'request_insert_hardware')
        pub.subscribe(self.do_update, 'request_update_hardware')
        pub.subscribe(self.do_update_all, 'request_update_all_hardware')
        pub.subscribe(self.do_make_composite_ref_des,
                      'request_make_comp_ref_des')
        pub.subscribe(self.do_get_attributes, 'request_get_attributes')
        pub.subscribe(self.do_get_all_attributes, 'request_get_all_attributes')
        pub.subscribe(self.do_set_attributes, 'request_set_attributes')
        pub.subscribe(self.do_set_all_attributes, 'succeed_calculate_hardware')

    def do_calculate_all(self, **kwargs):
        """
        Calculate all items in the system.

        :param float hr_multiplier: the hazard rate multiplier.  This is used
            to allow the hazard rates to be entered and displayed in more human
            readable numbers, but have the calculations work out.  Default
            value is 1E6 so hazard rates will be entered and displayed as
            failures/million hours.
        :param int node_id: the ID of the treelib Tree() node to start the
            calculation at.
        :return: _cum_results; the list of cumulative results.  The list order
            is:

                    * 0 - active hazard rate
                    * 1 - dormant hazard rate
                    * 2 - software hazard rate
                    * 3 - total cost
                    * 4 - part count
                    * 5 - power dissipation

        :rtype: list
        """
        _node_id = kwargs['node_id']
        _limits = kwargs['limits']
        _hr_multiplier = kwargs['hr_multiplier']
        _cum_results = [0.0, 0.0, 0.0, 0.0, 0, 0.0]

        # Check if there are children nodes of the node passed.
        if self.tree.get_node(_node_id).fpointer:
            _attributes = self.tree.get_node(_node_id).data

            # If there are children, calculate each of them first.
            for _subnode_id in self.tree.get_node(_node_id).fpointer:
                _results = self.do_calculate_all(
                    node_id=_subnode_id,
                    limits=_limits,
                    hr_multiplier=_hr_multiplier,
                )
                _cum_results[0] += _results[0]
                _cum_results[1] += _results[1]
                _cum_results[2] += _results[2]
                _cum_results[3] += _results[3]
                _cum_results[4] += int(_results[4])
                _cum_results[5] += _results[5]
            # Then calculate the parent node.
            _attributes = self.do_calculate(
                _node_id,
                limits=_limits,
                hr_multiplier=_hr_multiplier,
            )
            if _attributes is not None:
                _cum_results[0] += _attributes['hazard_rate_active']
                _cum_results[1] += _attributes['hazard_rate_dormant']
                _cum_results[2] += _attributes['hazard_rate_software']
                _cum_results[3] += _attributes['total_cost']
                _cum_results[4] += int(_attributes['total_part_count'])
                _cum_results[5] += _attributes['total_power_dissipation']
        else:
            if self.tree.get_node(_node_id).data is not None:
                _attributes = self.do_calculate(
                    _node_id,
                    limits=_limits,
                    hr_multiplier=_hr_multiplier,
                )
                _cum_results[0] += _attributes['hazard_rate_active']
                _cum_results[1] += _attributes['hazard_rate_dormant']
                _cum_results[2] += _attributes['hazard_rate_software']
                _cum_results[3] += _attributes['total_cost']
                _cum_results[4] += int(_attributes['total_part_count'])
                _cum_results[5] += _attributes['total_power_dissipation']

        if self.tree.get_node(
                _node_id, ).data is not None and _attributes['part'] == 0:
            _attributes['hazard_rate_active'] = _cum_results[0]
            _attributes['hazard_rate_dormant'] = _cum_results[1]
            _attributes['hazard_rate_software'] = _cum_results[2]
            _attributes['total_cost'] = _cum_results[3]
            _attributes['total_part_count'] = int(_cum_results[4])
            _attributes['total_power_dissipation'] = _cum_results[5]

            _attributes = self._do_calculate_reliability_metrics(_attributes)
            _attributes = self._do_calculate_cost_metrics(_attributes)
            _attributes = self._do_calculate_metric_variances(_attributes)

        return _cum_results

    def do_delete(self, node_id):
        """
        Remove a Hardware item.

        :param int node_id: the node (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        _error_code = 0
        _error_msg = ''

        # Delete the RAMSTKHardware entry.  Other RAMSTK Program database
        # tables will delete their entries based on CASCADE behavior.
        try:
            _hardware = self.tree.get_node(node_id).data['hardware']
            (_error_code,
             _error_msg) = self.dao.db_delete(_hardware, self.dao.session)
        except AttributeError:
            _error_code = 1
            _error_msg = ("Attempted to delete non-existent hardware ID "
                          "{0:s}.").format(str(node_id))

        # pylint: disable=attribute-defined-outside-init
        # self.last_id is defined in RAMSTKDataModel.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_hardware', node_id=node_id)
        else:
            pub.sendMessage('fail_delete_hardware', error_msg=_error_msg)

    def do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for the hardware item.

        :param int node_id: the node (hardware) ID of the hardware item to
            get the attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_attributes',
                        attributes=self.do_select(
                            node_id, table=table).get_attributes())

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
                'mil_hdbk_217f', 'nswc', 'reliability'
        ]:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_attributes', attributes=_attributes)

    def do_insert(self, revision_id, parent_id, part):  # pytest: disable=arguments-differ
        """
        Add a new hardware item.

        :param int revision_id: the revision ID to add the hardware item.
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
                _hardware = RAMSTKHardware(revision_id=revision_id,
                                           parent_id=parent_id,
                                           part=part)

                _error_code, _msg = self.dao.db_add([_hardware], None)

                self.last_id = _hardware.hardware_id

                _design_e = RAMSTKDesignElectric(hardware_id=self.last_id)
                _design_m = RAMSTKDesignMechanic(hardware_id=self.last_id)
                _milhdbkf = RAMSTKMilHdbkF(hardware_id=self.last_id)
                _nswc = RAMSTKNSWC(hardware_id=self.last_id)
                _reliability = RAMSTKReliability(hardware_id=self.last_id)

                _error_code, _msg = self.dao.db_add(
                    [_design_e, _design_m, _milhdbkf, _nswc, _reliability],
                    None)

                _data_package = {
                    'hardware': _hardware,
                    'design_electric': _design_e,
                    'design_mechanic': _design_m,
                    'mil_hdbk_217f': _milhdbkf,
                    'nswc': _nswc,
                    'reliability': _reliability
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
        else:
            _node.data['hardware'].comp_ref_des = _node.data[
                'hardware'].ref_des

        # Now make the composite reference designator for all the child nodes.
        for _child_node in self.tree.children(node_id):
            self.do_make_composite_ref_des(node_id=_child_node.identifier)

    def do_select(self, node_id, **kwargs):
        """
        Retrieve the data package for the requested table.

        :param int node_id: the ID of the node in the treelib Tree() to select.
            This is the Hardware ID.
        :return: the requested table record for the node ID.  This will be a
            record from the RAMSTKDesignElectric, RAMSTKDesignMechanic,
            RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKNSWC, or RAMSTKReliability
            table.
        :rtype: :class:`ramstk.data.models.RAMSTKDesignElectric`
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        :raise: TypeError if passed a node (hardware) ID that doesn't exist in
            the tree.
        """
        _table = kwargs['table']

        return RAMSTKDataModel.do_select(self, node_id)[_table]

    def do_select_all(self, revision_id):   # pytest: disable=arguments-differ
        """
        Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Hardware BoM for.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hardware in self.dao.session.query(RAMSTKHardware).filter(
                RAMSTKHardware.revision_id == revision_id).all():

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

            _data_package = {
                'hardware': _hardware,
                'design_electric': _design_e,
                'design_mechanic': _design_m,
                'mil_hdbk_217f': _milhdbkf,
                'nswc': _nswc,
                'reliability': _reliability
            }

            self.tree.create_node(tag=_hardware.comp_ref_des,
                                  identifier=_hardware.hardware_id,
                                  parent=_hardware.parent_id,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_hardware', tree=self.tree)

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
                'mil_hdbk_217f', 'nswc', 'reliability'
        ]:
            _attributes = self.do_select(node_id,
                                         table=_table).get_attributes()
            if key in _attributes:
                _attributes[key] = value

                if _table == 'hardware':
                    _attributes.pop('revision_id')
                _attributes.pop('hardware_id')

                self.do_select(node_id,
                               table=_table).set_attributes(_attributes)

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
            _error_code, _error_msg = self.dao.db_update(None)

            if _error_code == 0:
                pub.sendMessage('succeed_update_hardware', node_id=node_id)
            else:
                pub.sendMessage('fail_update_hardware', error_msg=_error_msg)
        except AttributeError:
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

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKHardware table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_update(_node.identifier)
