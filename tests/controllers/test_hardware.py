# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.controllers.hardware.test_hardware.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_DESIGN_ELECTRIC, MOCK_DESIGN_MECHANIC, MOCK_HARDWARE
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amHardware, dmHardware
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKHardware
)


class MockDao:
    _all_hardware = []
    _all_design_electric = []
    _all_design_mechanic = []

    def _do_delete_hardware(self, record):
        for _idx, _record in enumerate(self._all_hardware):
            if _record.hardware_id == record.hardware_id:
                self._all_hardware.pop(_idx)

    def _do_delete_design_electric(self, record):
        for _idx, _record in enumerate(self._all_design_electric):
            if _record.hardware_id == record.hardware_id:
                self._all_design_electric.pop(_idx)

    def _do_delete_design_mechanic(self, record):
        for _idx, _record in enumerate(self._all_design_mechanic):
            if _record.hardware_id == record.hardware_id:
                self._all_design_mechanic.pop(_idx)

    def _do_delete_milhdbkf(self, record):
        for _idx, _record in enumerate(self._all_217f):
            if _record.hardware_id == record.hardware_id:
                self._all_217f.pop(_idx)

    def _do_delete_nswc(self, record):
        for _idx, _record in enumerate(self._all_nswc):
            if _record.hardware_id_id == record.hardware_id:
                self._all_nswc.pop(_idx)

    def do_delete(self, record):
        if record is None:
            raise DataAccessError('')
        elif record == RAMSTKHardware:
            self._do_delete_hardware(record)
        elif record == RAMSTKDesignElectric:
            self._do_delete_design_electric(record)
        elif record == RAMSTKDesignMechanic:
            self._do_delete_design_mechanic(record)

    def do_insert(self, record):
        if record.hardware_id == 30:
            raise DataAccessError('An error occurred with RAMSTK.')
        elif record == RAMSTKHardware:
            self._all_hardware.append(record)
        elif record == RAMSTKDesignElectric:
            self._all_design_electric.append(record)
        elif record == RAMSTKDesignMechanic:
            self._all_design_mechanic.append(record)

    def do_insert_many(self, records):
        for _record in records:
            self.do_insert(_record)

    def _do_select_all_hardware(self, table, value):
        self._all_hardware = []
        for _key in MOCK_HARDWARE:
            _record = table()
            _record.revision_id = value
            _record.hardware_id = _key
            _record.set_attributes(MOCK_HARDWARE[_key])
            self._all_hardware.append(_record)

        return self._all_hardware

    def _do_select_all_design_electric(self, table, value):
        self._all_design_electric = []
        _record = table()
        _record.hardware_id = value[0]
        _record.set_attributes(MOCK_DESIGN_ELECTRIC[value[0]])
        self._all_design_electric.append(_record)

        return self._all_design_electric[0]

    def _do_select_all_design_mechanic(self, table, value):
        self._all_design_mechanic = []
        _record = table()
        _record.hardware_id = value[0]
        _record.set_attributes(MOCK_DESIGN_MECHANIC[value[0]])
        self._all_design_mechanic.append(_record)

        return self._all_design_mechanic[0]

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        if table == RAMSTKHardware:
            _records = self._do_select_all_hardware(table, value)
        elif table == RAMSTKDesignElectric:
            _records = self._do_select_all_design_electric(table, value)
        elif table == RAMSTKDesignMechanic:
            _records = self._do_select_all_design_mechanic(table, value)

        return _records

    def do_update(self, record):
        if isinstance(record, RAMSTKHardware):
            for _key in MOCK_HARDWARE:
                if _key == record.hardware_id:
                    MOCK_HARDWARE[_key]['cost'] = record.cost
                    MOCK_HARDWARE[_key]['part'] = int(record.part)
        elif isinstance(record, RAMSTKDesignElectric):
            for _key in MOCK_DESIGN_ELECTRIC:
                if _key == record.hardware_id:
                    MOCK_DESIGN_ELECTRIC[_key]['area'] = record.area
        elif isinstance(record, RAMSTKDesignMechanic):
            for _key in MOCK_DESIGN_MECHANIC:
                if _key == record.hardware_id:
                    MOCK_DESIGN_MECHANIC[_key][
                        'altitude_operating'] = record.altitude_operating


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Hardware data manager."""
        DUT = dmHardware()

        assert isinstance(DUT, dmHardware)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'hardware'
        assert DUT._root == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_hardware_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_hardware_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes, 'wvw_editing_component')
        assert pub.isSubscribed(DUT.do_set_attributes, 'wvw_editing_hardware')
        assert pub.isSubscribed(DUT.do_set_tree, 'succeed_calculate_hardware')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_hardware')

        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_hardware_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_hardware')

        assert pub.isSubscribed(DUT._do_delete, 'request_delete_hardware')
        assert pub.isSubscribed(DUT._do_get_all_attributes,
                                'request_get_all_hardware_attributes')
        assert pub.isSubscribed(DUT._do_insert_hardware,
                                'request_insert_hardware')
        assert pub.isSubscribed(DUT._do_make_composite_ref_des,
                                'request_make_comp_ref_des')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the hardware analysis
        manager."""
        DUT = amHardware(test_toml_user_configuration)

        assert isinstance(DUT, amHardware)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_hardware_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_retrieve_hardware')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_hardware_tree')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_update_hardware')

        assert pub.isSubscribed(DUT._do_calculate_hardware,
                                'request_calculate_hardware')
        assert pub.isSubscribed(DUT._do_derating_analysis,
                                'request_derate_hardware')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['hardware'], RAMSTKHardware)
        assert isinstance(
            tree.get_node(1).data['design_electric'], RAMSTKDesignElectric)
        assert isinstance(
            tree.get_node(1).data['design_mechanic'], RAMSTKDesignMechanic)

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKHardware instances on success."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_hardware')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing Hardware
        tree."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_hardware')

    @pytest.mark.unit
    def test_do_select_design_electric(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKDesignElectric on
        success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='design_electric')

        assert isinstance(_hardware, RAMSTKDesignElectric)
        assert _hardware.application_id == 0
        assert _hardware.power_rated == 0.0

    @pytest.mark.unit
    def test_do_select_design_mechanic(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKDesignMechanic on
        success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='design_mechanic')

        assert isinstance(_hardware, RAMSTKDesignMechanic)
        assert _hardware.altitude_operating == 0.0
        assert _hardware.impact_id == 0.0

    @pytest.mark.unit
    def test_do_select_hardware(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKHardware on
        success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='hardware')

        assert isinstance(_hardware, RAMSTKHardware)
        assert _hardware.ref_des == 'S1'
        assert _hardware.cage_code == ''

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Hardware ID is
        requested."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='hardware') is None


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_hardware(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hardware topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_hardware,
                      'succeed_delete_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete_hardware,
                        'succeed_delete_hardware')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == (
                "_do_delete: Attempted to delete non-existent hardware ID 300."
            )

        pub.subscribe(on_message, 'fail_delete_hardware')

        pub.sendMessage('request_delete_hardware', node_id=300)

        pub.unsubscribe(on_message, 'fail_delete_hardware')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    @pytest.mark.unit
    def test_do_get_attributes_hardware(self, mock_program_dao):
        """do_get_attributes() should return a dict of hardware attributes on
        success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes['hardware_id'] == 2
            assert attributes['comp_ref_des'] == 'S1:SS1'
            assert attributes['parent_id'] == 1
            assert attributes['ref_des'] == 'SS1'

        pub.subscribe(on_message, 'succeed_get_hardware_attributes')

        pub.sendMessage('request_get_hardware_attributes',
                        node_id=2,
                        table='hardware')

    @pytest.mark.unit
    def test_get_all_attributes_data_manager(self, mock_program_dao):
        """get_all_attributes() should return a dict of all RAMSTK data tables'
        attributes on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes['hardware_id'] == 2
            assert attributes['application_id'] == 0
            assert attributes['comp_ref_des'] == 'S1:SS1'
            assert attributes['ref_des'] == 'SS1'

        pub.subscribe(on_message, 'succeed_get_all_hardware_attributes')

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)

    @pytest.mark.unit
    def test_get_all_attributes_analysis_manager(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)

        assert DUT._attributes['hardware_id'] == 2
        assert DUT._attributes['application_id'] == 0
        assert DUT._attributes['comp_ref_des'] == 'S1:SS1'
        assert DUT._attributes['ref_des'] == 'SS1'

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao, test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_hardware_tree message."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(tree):
            assert isinstance(tree, Tree)
            assert isinstance(DUT._tree, Tree)
            assert DUT._tree == tree
            assert isinstance(
                DUT._tree.get_node(1).data['hardware'], RAMSTKHardware)
            assert isinstance(
                DUT._tree.get_node(1).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                DUT._tree.get_node(1).data['design_mechanic'],
                RAMSTKDesignMechanic)

        pub.subscribe(on_message, 'succeed_get_hardware_tree')

        pub.sendMessage('request_get_hardware_tree')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_hardware_attributes',
                        node_id=[2, -1],
                        package={'name': 'Testing set name from moduleview.'})
        assert DUT.do_select(
            2, table='hardware').name == 'Testing set name from moduleview.'

        pub.sendMessage('request_set_hardware_attributes',
                        node_id=[1, -1],
                        package={'capacitance': 0.000047})
        assert DUT.do_select(1, table='design_electric').capacitance == \
               0.000047
        pub.sendMessage('request_set_hardware_attributes',
                        node_id=[1, -1],
                        package={'load_operating': 0.95})
        assert DUT.do_select(1, table='design_mechanic').load_operating == \
               0.95


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_fail_insert_hardware_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_hardware topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling_assembly(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new sibling hardware assembly."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 4
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 1
            assert tree.get_node(node_id).data['hardware'].part == 0

        pub.subscribe(on_message, 'succeed_insert_hardware')

        pub.sendMessage('request_insert_hardware', parent_id=1, part=0)

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.unit
    def test_do_insert_child_assembly(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new child hardware assembly."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 4
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 2
            assert tree.get_node(node_id).data['hardware'].part == 0

        pub.subscribe(on_message, 'succeed_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=2, part=0) is None

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.unit
    def test_do_insert_part(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new hardware part."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 4
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 2
            assert tree.get_node(node_id).data['hardware'].part == 1

        pub.subscribe(on_message, 'succeed_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=2, part=1) is None

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.integration
    def test_do_insert_part_to_part(self, test_program_dao):
        """do_insert() should send the fail message when attempting to add a
        child to a hardware part."""
        DUT = dmHardware()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == (
                'Attempting to insert a hardware assembly or '
                'component/piece part as a child of another '
                'component/piece part.')

        pub.subscribe(on_message, 'fail_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=8, part=1) is None

        pub.unsubscribe(on_message, 'fail_insert_hardware')

    @pytest.mark.unit
    def test_do_insert_hardware_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_hardware_db_error,
                      'fail_insert_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.last_id = 29
        DUT._do_insert_hardware(parent_id=0, part=0)

        pub.unsubscribe(self.on_fail_insert_hardware_db_error,
                        'fail_insert_hardware')

    @pytest.mark.unit
    def test_do_make_comp_ref_des(self, mock_program_dao):
        """do_make_comp_ref_des() should return a zero error code on
        success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='hardware')
        _hardware.ref_des = "SS8"
        _hardware = DUT.do_select(2, table='hardware')
        _hardware.ref_des = "A9"
        #_hardware = DUT.do_select(10, table='hardware')
        #_hardware.ref_des = "C1"

        pub.sendMessage('request_make_comp_ref_des', node_id=1)

        assert DUT.do_select(1, table='hardware').comp_ref_des == 'SS8'
        assert DUT.do_select(2, table='hardware').comp_ref_des == 'SS8:A9'
        #assert DUT.do_select(10, table='hardware').comp_ref_des == \
        #       'S1:SS1:A2:C1'


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_fail_update_hardware_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'hardware ID 1.')
        print("\033[35m\nfail_update_hardware topic was broadcast")

    def on_fail_update_hardware_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for hardware ID 1 was the wrong type.'
        )
        print("\033[35m\nfail_update_hardware topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(tree):
            DUT.do_select_all(attributes={'revision_id': 1})
            _hardware = DUT.do_select(2, table='hardware')
            assert isinstance(tree, Tree)
            assert _hardware.parent_id == 1
            assert _hardware.cost == 0.9832
            _hardware = DUT.do_select(2, table='design_electric')
            assert _hardware.parent_id == 1
            assert _hardware.area == 12000
            _hardware = DUT.do_select(2, table='design_mechanic')
            assert _hardware.parent_id == 1
            assert _hardware.altitude_operating == 12000

        pub.subscribe(on_message, 'succeed_update_hardware')

        _hardware = DUT.do_select(2, table='hardware')
        _hardware.cost = 0.9832
        _hardware = DUT.do_select(2, table='design_electric')
        _hardware.area = 12000
        _hardware = DUT.do_select(2, table='design_mechanic')
        _hardware.altitude_operating = 12000

        pub.sendMessage('request_update_hardware', node_id=2)

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Hardware ID that doesn't exist."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == (
                'do_update: Attempted to save non-existent hardware ID 100.')

        pub.subscribe(on_message, 'fail_update_hardware')

        DUT.do_update(100)

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_hardware_no_data,
                      'fail_update_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('hardware')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_hardware_no_data,
                        'fail_update_hardware')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_hardware_wrong_data_type,
                      'fail_update_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _hardware = DUT.do_select(1, table='hardware')
        _hardware.part = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_hardware_wrong_data_type,
                        'fail_update_hardware')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, table='hardware')
        _validation.part = {1: 2}

        DUT.do_update(0)

    @pytest.mark.unit
    def test_do_update_all(self, mock_program_dao):
        """do_update_all() should return a zero error code on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(tree):
            assert isinstance(tree, Tree)

        pub.subscribe(on_message, 'succeed_update_hardware')

        pub.sendMessage('request_update_all_hardware')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestStressCalculations():
    """Class for stress-related calculations test suite."""
    def on_fail_stress_analysis_zero_current(self, error_message):
        assert error_message == (
            '_do_calculate_current_ratio: Failed to calculate current ratio for hardware ID 3.  Rated current=0.0, operating current=0.05.'
        )
        print("\033[35m\nfail_stress_analysis topic was broadcast")

    def on_fail_stress_analysis_zero_power(self, error_message):
        assert error_message == (
            "_do_calculate_power_ratio: Failed to calculate power ratio for hardware ID 3.  Rated power=0.0, operating power=0.0125."
        )
        print("\033[35m\nfail_stress_analysis topic was broadcast")

    def on_fail_stress_analysis_zero_voltage(self, error_message):
        assert error_message == (
            "_do_calculate_voltage_ratio: Failed to "
            "calculate voltage ratio for hardware ID 3.  Rated voltage=0.0, operating ac voltage=0.002, operating DC voltage=0.25."
        )
        print("\033[35m\nfail_stress_analysis topic was broadcast")

    def on_succeed_derate_hardware_above_limit(self, attributes):
        assert attributes['overstress']
        assert attributes['reason'] == ('Operating voltage is greater than '
                                        'limit in a harsh environment.\n'
                                        'Operating voltage is greater than '
                                        'limit in a mild environment.\n')
        print("\033[35m\nsucceed_derate_hardware topic was broadcast")

    def on_succeed_derate_hardware_below_limit(self, attributes):
        assert attributes['overstress']
        assert attributes['reason'] == ('Operating voltage is less than '
                                        'limit in a harsh environment.\n'
                                        'Operating voltage is less than '
                                        'limit in a mild environment.\n')
        print("\033[35m\nsucceed_derate_hardware topic was broadcast")

    @pytest.mark.unit
    def test_do_calculate_current_ratio(self, mock_program_dao,
                                        test_toml_user_configuration):
        """_do_calculate_current() should return None and update the current
        ratio attribute."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        assert DUT._do_calculate_current_ratio(DUT._tree.get_node(3)) is None
        assert DUT._tree.get_node(3).data['design_electric'].current_ratio == \
               0.4

    @pytest.mark.unit
    def test_do_calculate_current_ratio_zero_rated(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message
        when rated current is zero."""
        pub.subscribe(self.on_fail_stress_analysis_zero_current,
                      'fail_stress_analysis')

        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(3).data['design_electric'].current_rated = 0.0
        DUT._request_do_stress_analysis(DUT._tree.get_node(3))

        pub.unsubscribe(self.on_fail_stress_analysis_zero_current,
                        'fail_stress_analysis')

    @pytest.mark.unit
    def test_do_calculate_power_ratio(self, mock_program_dao,
                                      test_toml_user_configuration):
        """_do_calculate_power() should return None and update the power ratio
        attribute."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        assert DUT._do_calculate_power_ratio(DUT._tree.get_node(3)) is None
        assert DUT._tree.get_node(
            3).data['design_electric'].power_ratio == 0.25

    @pytest.mark.unit
    def test_do_calculate_power_ratio_zero_rated(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_do_calculate_power() should raise the failure message when rated
        power is zero."""
        pub.subscribe(self.on_fail_stress_analysis_zero_power,
                      'fail_stress_analysis')

        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(3).data['hardware'].category_id = 3
        DUT._tree.get_node(3).data['design_electric'].power_rated = 0.0
        DUT._request_do_stress_analysis(DUT._tree.get_node(3))

        pub.unsubscribe(self.on_fail_stress_analysis_zero_power,
                        'fail_stress_analysis')

    @pytest.mark.unit
    def test_do_calculate_voltage_ratio(self, mock_program_dao,
                                        test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message
        when rated voltage is zero."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        assert DUT._do_calculate_voltage_ratio(DUT._tree.get_node(3)) is None
        assert DUT._tree.get_node(3).data[
            'design_electric'].voltage_ratio == pytest.approx(0.076363636)

    @pytest.mark.unit
    def test_do_calculate_part_zero_rated_voltage(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message
        when rated voltage is zero."""
        pub.subscribe(self.on_fail_stress_analysis_zero_voltage,
                      'fail_stress_analysis')

        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(3).data['design_electric'].voltage_rated = 0.0
        DUT._request_do_stress_analysis(DUT._tree.get_node(3))

        pub.unsubscribe(self.on_fail_stress_analysis_zero_voltage,
                        'fail_stress_analysis')

    @pytest.mark.unit
    def test_do_derating_analysis_current_stress(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and
        build reason message when a component is current overstressed."""
        test_toml_user_configuration.get_user_configuration()
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['overstress']
            assert attributes['reason'] == (
                'Operating current is greater than '
                'limit in a harsh environment.\n'
                'Operating current is greater than '
                'limit in a mild environment.\n')

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_type_id': 1})
        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_method_id': 2})
        DATAMGR.do_set_attributes([1, -1], {'category_id': 8})
        DATAMGR.do_set_attributes([1, -1], {'current_ratio': 0.95})
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_derating_analysis_power_stress(self, mock_program_dao,
                                               test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and
        build reason message when a component is power overstressed."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['overstress']
            assert attributes['reason'] == ('Operating power is greater than '
                                            'limit in a harsh environment.\n'
                                            'Operating power is greater than '
                                            'limit in a mild environment.\n')

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_type_id': 1})
        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_method_id': 2})
        DATAMGR.do_set_attributes([1, -1], {'category_id': 3})
        DATAMGR.do_set_attributes([1, -1], {'power_ratio': 0.95})
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_derating_analysis_voltage_stress_under(
            self, mock_program_dao, test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and
        build reason message when a component is voltage overstressed."""
        pub.subscribe(self.on_succeed_derate_hardware_below_limit,
                      'succeed_derate_hardware')

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_type_id': 1})
        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_method_id': 2})
        DATAMGR.do_set_attributes([1, -1], {'category_id': 4})
        DATAMGR.do_set_attributes([1, -1], {'voltage_ratio': -0.95})
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

        pub.unsubscribe(self.on_succeed_derate_hardware_below_limit,
                        'succeed_derate_hardware')

    @pytest.mark.unit
    def test_do_derating_analysis_voltage_stress_over(
            self, mock_program_dao, test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and
        build reason message when a component is voltage overstressed."""
        pub.subscribe(self.on_succeed_derate_hardware_above_limit,
                      'succeed_derate_hardware')

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_type_id': 1})
        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_method_id': 2})
        DATAMGR.do_set_attributes([1, -1], {'category_id': 4})
        DATAMGR.do_set_attributes([1, -1], {'voltage_ratio': 0.95})
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

        pub.unsubscribe(self.on_succeed_derate_hardware_above_limit,
                        'succeed_derate_hardware')

    @pytest.mark.unit
    def test_do_derating_analysis_no_overstress(self, mock_program_dao,
                                                test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute False and the
        reason message should='' when a component is not overstressed."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert not attributes['overstress']
            assert attributes['reason'] == ''

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_type_id': 1})
        DATAMGR.do_set_attributes([1, -1], {'hazard_rate_method_id': 2})
        DATAMGR.do_set_attributes([1, -1], {'category_id': 4})
        DATAMGR.do_set_attributes([1, -1], {'current_ratio': 0.45})
        DATAMGR.do_set_attributes([1, -1], {'power_ratio': 0.35})
        DATAMGR.do_set_attributes([1, -1], {'voltage_ratio': 0.5344})
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_cost_part(self, mock_program_dao,
                                    test_toml_user_configuration):
        """_do_calculate_part_count() should assign quantity to total part
        count for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_cost_metrics(DUT._tree.get_node(3))

        assert DUT._tree.get_node(3).data['hardware'].total_cost == \
               pytest.approx(2.35)

    @pytest.mark.unit
    def test_do_calculate_cost_assembly(self, mock_program_dao,
                                        test_toml_user_configuration):
        """_do_calculate_part_count() should assign quantity to total part
        count for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_cost_metrics(DUT._tree.get_node(2))

        assert DUT._tree.get_node(2).data['hardware'].total_cost == \
               pytest.approx(4.70)

    @pytest.mark.unit
    def test_do_calculate_cost_system(self, mock_program_dao,
                                      test_toml_user_configuration):
        """_do_calculate_part_count() should assign quantity to total part
        count for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_cost_metrics(DUT._tree.get_node(1))

        assert DUT._tree.get_node(1).data['hardware'].total_cost == \
               pytest.approx(4.70)

    @pytest.mark.unit
    def test_do_calculate_cost_specified(self, mock_program_dao,
                                         test_toml_user_configuration):
        """_do_calculate_part_count() should assign quantity to total part
        count for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(3).data['hardware'].cost_type_id = 1
        DUT._do_calculate_cost_metrics(DUT._tree.get_node(3))

        assert DUT._tree.get_node(3).data['hardware'].total_cost == \
               pytest.approx(1.98)

    @pytest.mark.unit
    def test_do_calculate_part_count_part(self, mock_program_dao,
                                          test_toml_user_configuration):
        """_do_calculate_part_count() should assign quantity to total part
        count for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_part_count(DUT._tree.get_node(3))

        assert DUT._tree.get_node(3).data['hardware'].total_part_count == 5

    @pytest.mark.unit
    def test_do_calculate_part_count_assembly(self, mock_program_dao,
                                              test_toml_user_configuration):
        """_do_calculate_part_count() should multiply total part count by
        quantity for an assembly."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_part_count(DUT._tree.get_node(2))

        assert DUT._tree.get_node(2).data['hardware'].total_part_count == 10

    @pytest.mark.unit
    def test_do_calculate_part_count_system(self, mock_program_dao,
                                            test_toml_user_configuration):
        """_do_calculate_part_count() should multiply total part count by
        quantity for an assembly."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_part_count(DUT._tree.get_node(1))

        assert DUT._tree.get_node(1).data['hardware'].total_part_count == 10

    @pytest.mark.unit
    def test_do_calculate_power_dissipation_part(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_do_calculate_power_dissipation() should assign the product of
        quantity and operating power to total power dissipation for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_power_dissipation(DUT._tree.get_node(3))

        assert DUT._tree.get_node(
            3).data['hardware'].total_power_dissipation == 0.0625

    @pytest.mark.unit
    def test_do_calculate_power_dissipation_assembly(
            self, mock_program_dao, test_toml_user_configuration):
        """_do_calculate_power_dissipation() should assign the product of
        quantity and operating power to total power dissipation for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_power_dissipation(DUT._tree.get_node(2))

        assert DUT._tree.get_node(
            2).data['hardware'].total_power_dissipation == 0.1250

    @pytest.mark.unit
    def test_do_calculate_power_dissipation_system(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_do_calculate_power_dissipation() should assign the product of
        quantity and operating power to total power dissipation for a part."""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_power_dissipation(DUT._tree.get_node(1))

        assert DUT._tree.get_node(
            1).data['hardware'].total_power_dissipation == 0.1250

    @pytest.mark.unit
    def test_do_calculate_hardware_part(self, mock_program_dao,
                                        test_toml_user_configuration):
        """_do_calculate_hardware()"""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_hardware(3)

        assert DUT._tree.get_node(3).data['hardware'].total_cost == \
               pytest.approx(2.35)
        assert DUT._tree.get_node(3).data['hardware'].total_part_count == 5
        assert DUT._tree.get_node(
            3).data['hardware'].total_power_dissipation == 0.0625

    @pytest.mark.unit
    def test_do_calculate_hardware_assembly(self, mock_program_dao,
                                            test_toml_user_configuration):
        """_do_calculate_hardware()"""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_hardware(2)

        assert DUT._tree.get_node(2).data['hardware'].total_cost == \
               pytest.approx(4.70)
        assert DUT._tree.get_node(2).data['hardware'].total_part_count == 10
        assert DUT._tree.get_node(
            2).data['hardware'].total_power_dissipation == 0.125

    @pytest.mark.unit
    def test_do_calculate_hardware_system(self, mock_program_dao,
                                          test_toml_user_configuration):
        """_do_calculate_hardware()"""
        DUT = amHardware(test_toml_user_configuration)

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._do_calculate_hardware(1)

        assert DUT._tree.get_node(1).data['hardware'].total_cost == \
               pytest.approx(4.70)
        assert DUT._tree.get_node(1).data['hardware'].total_part_count == 10
        assert DUT._tree.get_node(
            1).data['hardware'].total_power_dissipation == 0.1250
