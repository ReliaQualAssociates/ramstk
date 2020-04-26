# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.controllers.hardware.test_hardware.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models. """
# TODO: un-skip matrix tests in test_hardware.py.
#
# The Hardware work flow module currently has no other modules it
# cross-references with and, thus, does not need to create matrices.  Future
# RAMSTK work flow modules will be cross-referenced with the Hardware
# module.  When these new modules exist, the matrix-related tests in
# test_hardware.py should be un-skipped.

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import (
    MOCK_217F, MOCK_ALLOCATION, MOCK_DESIGN_ELECTRIC,
    MOCK_DESIGN_MECHANIC, MOCK_HARDWARE, MOCK_NSWC,
    MOCK_RELIABILITY, MOCK_RQRMNT_TREE, MOCK_SIMILAR_ITEM
)
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amHardware, dmHardware, mmHardware
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAllocation, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability, RAMSTKSimilarItem
)


class MockDao:
    _all_hardware = []
    _all_design_electric = []
    _all_design_mechanic = []
    _all_217f = []
    _all_nswc = []
    _all_reliability = []
    _all_allocation = []
    _all_similar_item = []

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
        try:
            if record == RAMSTKHardware:
                self._do_delete_hardware(record)
            elif record == RAMSTKDesignElectric:
                self._do_delete_design_electric(record)
            elif record == RAMSTKDesignMechanic:
                self._do_delete_design_mechanic(record)
            elif record == RAMSTKMilHdbkF:
                self._do_delete_milhdbkf(record)
            elif record == RAMSTKNSWC:
                self._do_delete_nswc(record)
        except AttributeError:
            raise DataAccessError('')

    def do_insert(self, record):
        if record == RAMSTKHardware:
            self._all_hardware.append(record)
        elif record == RAMSTKDesignElectric:
            self._all_design_electric.append(record)
        elif record == RAMSTKDesignMechanic:
            self._all_design_mechanic.append(record)
        elif record == RAMSTKMilHdbkF:
            self._all_217f.append(record)
        elif record == RAMSTKNSWC:
            self._all_nswc.append(record)
        elif record == RAMSTKReliability:
            self._all_reliability.append(record)
        elif record == RAMSTKAllocation:
            self._all_allocation.append(record)
        elif record == RAMSTKSimilarItem:
            self._all_similar_item.append(record)

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
        _record.hardware_id = value
        _record.set_attributes(MOCK_DESIGN_ELECTRIC[value])
        self._all_design_electric.append(_record)

        return self._all_design_electric[0]

    def _do_select_all_design_mechanic(self, table, value):
        self._all_design_mechanic = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_DESIGN_MECHANIC[value])
        self._all_design_mechanic.append(_record)

        return self._all_design_mechanic[0]

    def _do_select_all_217f(self, table, value):
        self._all_217f = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_217F[value])
        self._all_217f.append(_record)

        return self._all_217f[0]

    def _do_select_all_nswc(self, table, value):
        self._all_nswc = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_NSWC[value])
        self._all_nswc.append(_record)

        return self._all_nswc[0]

    def _do_select_all_reliability(self, table, value):
        self._all_reliability = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_RELIABILITY[value])
        self._all_reliability.append(_record)

        return self._all_reliability[0]

    def _do_select_all_allocation(self, table, value):
        self._all_allocation = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_ALLOCATION[value])
        self._all_allocation.append(_record)

        return self._all_allocation[0]

    def _do_select_all_similar_item(self, table, value):
        self._all_similar_item = []
        _record = table()
        _record.hardware_id = value
        _record.set_attributes(MOCK_SIMILAR_ITEM[value])
        self._all_similar_item.append(_record)

        return self._all_similar_item[0]

    def do_select_all(self, table, key=None, value=None, order=None,
                      _all=False):
        if table == RAMSTKHardware:
            _records = self._do_select_all_hardware(table, value)
        elif table == RAMSTKDesignElectric:
            _records = self._do_select_all_design_electric(table, value)
        elif table == RAMSTKDesignMechanic:
            _records = self._do_select_all_design_mechanic(table, value)
        elif table == RAMSTKMilHdbkF:
            _records = self._do_select_all_217f(table, value)
        elif table == RAMSTKNSWC:
            _records = self._do_select_all_nswc(table, value)
        elif table == RAMSTKReliability:
            _records = self._do_select_all_reliability(table, value)
        elif table == RAMSTKAllocation:
            _records = self._do_select_all_allocation(table, value)
        elif table == RAMSTKSimilarItem:
            _records = self._do_select_all_similar_item(table, value)

        return _records

    def do_update(self, record):
        for _key in MOCK_HARDWARE:
            if _key == record.cost:
                MOCK_HARDWARE[_key]['cost'] = record.cost
        for _key in MOCK_ALLOCATION:
            if _key == record.mtbf_goal:
                MOCK_ALLOCATION[_key]['mtbf_goal'] = record.mtbf_goal


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
        assert pub.isSubscribed(DUT._do_select_all_hardware,
                        'succeed_select_revision')
        assert pub.isSubscribed(DUT.do_set_tree, 'succeed_calculate_all_hardware')
        assert pub.isSubscribed(DUT._do_delete_hardware, 'request_delete_hardware')
        assert pub.isSubscribed(DUT._do_insert_hardware, 'request_insert_hardware')
        assert pub.isSubscribed(DUT.do_update, 'request_update_hardware')
        assert pub.isSubscribed(DUT.do_update_all, 'request_update_all_hardware')
        assert pub.isSubscribed(DUT._do_make_composite_ref_des,
                      'request_make_comp_ref_des')
        assert pub.isSubscribed(DUT.do_get_attributes,
                      'request_get_hardware_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                      'request_get_all_hardware_attributes')
        assert pub.isSubscribed(DUT._do_get_hardware_tree, 'request_get_hardware_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                      'request_set_hardware_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes, 'succeed_calculate_hardware')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the hardware analysis manager."""
        DUT = amHardware(test_toml_user_configuration)

        assert isinstance(DUT, amHardware)
        assert isinstance(DUT.RAMSTK_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}

    @pytest.mark.unit
    def test_matrix_manager_create(self):
        """__init__() should create an instance of the hardware matrix manager."""
        DUT = mmHardware()

        assert isinstance(DUT, mmHardware)
        assert isinstance(DUT._column_tables, dict)
        assert isinstance(DUT._col_tree, dict)
        assert isinstance(DUT._row_tree, Tree)
        assert DUT.dic_matrices == {}
        assert DUT.n_row == 1
        assert DUT.n_col == 1
        assert pub.isSubscribed(DUT.do_create_rows, 'succeed_retrieve_hardware')
        assert pub.isSubscribed(DUT._on_delete_hardware, 'succeed_delete_hardware')
        assert pub.isSubscribed(DUT._on_insert_hardware, 'succeed_insert_hardware')


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
        assert isinstance(
            tree.get_node(1).data['mil_hdbk_217f'], RAMSTKMilHdbkF)
        assert isinstance(tree.get_node(1).data['nswc'], RAMSTKNSWC)
        assert isinstance(
            tree.get_node(1).data['reliability'], RAMSTKReliability)
        assert isinstance(
            tree.get_node(1).data['allocation'], RAMSTKAllocation)
        assert isinstance(
            tree.get_node(1).data['similar_item'], RAMSTKSimilarItem)

    @pytest.mark.unit
    def test__do_select_all_hardware(self, mock_program_dao):
        """_do_select_all_hardware() should return a Tree() object populated with RAMSTKHardware instances on success."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_hardware')

    @pytest.mark.unit
    def test_do_select_design_electric(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKDesignElectric on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='design_electric')

        assert isinstance(_hardware, RAMSTKDesignElectric)
        assert _hardware.application_id == 0
        assert _hardware.power_rated == 0.0

    @pytest.mark.unit
    def test_do_select_design_mechanic(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKDesignMechanic on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='design_mechanic')

        assert isinstance(_hardware, RAMSTKDesignMechanic)
        assert _hardware.altitude_operating == 0.0
        assert _hardware.impact_id == 0.0

    @pytest.mark.unit
    def test_do_select_hardware(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKHardware on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='hardware')

        assert isinstance(_hardware, RAMSTKHardware)
        assert _hardware.ref_des == 'S1'
        assert _hardware.cage_code == ''

    @pytest.mark.unit
    def test_do_select_mil_hdbk_f(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKMilHdbkF on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='mil_hdbk_217f')

        assert isinstance(_hardware, RAMSTKMilHdbkF)
        assert _hardware.piE == 0.0
        assert _hardware.lambdaBD == 0.0

    @pytest.mark.unit
    def test_do_select_nswc(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKNSWC on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='nswc')

        assert isinstance(_hardware, RAMSTKNSWC)
        assert _hardware.Cac == 0.0
        assert _hardware.Ci == 0.0

    @pytest.mark.unit
    def test_do_select_reliability(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKReliability on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='reliability')

        assert isinstance(_hardware, RAMSTKReliability)
        assert _hardware.lambda_b == 0.0
        assert _hardware.reliability_goal == 1.0

    @pytest.mark.unit
    def test__do_select_all_hardwareocation(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKAllocation on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='allocation')

        assert isinstance(_hardware, RAMSTKAllocation)
        assert _hardware.goal_measure_id == 1
        assert _hardware.mtbf_alloc == 0.0

    @pytest.mark.unit
    def test_do_select_similar_item(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKSimilarItem on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        _hardware = DUT.do_select(1, table='similar_item')

        assert isinstance(_hardware, RAMSTKSimilarItem)
        assert _hardware.change_description_1 == ''
        assert _hardware.temperature_from == 30.0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Hardware ID is requested."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='hardware') is None

    @pytest.mark.skip
    def test_do_create_matrix(self, test_program_dao):
        """_do_create() should create an instance of the hardware matrix manager."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = mmHardware()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('hrdwr_rqrmnt', 1, 0) == 'REL-0001'
        assert DUT.do_select('hrdwr_rqrmnt', 2, 0) == 'FUNC-0001'
        assert DUT.do_select('hrdwr_rqrmnt', 3, 0) == 'REL-0002'
        assert DUT.do_select('hrdwr_rqrmnt', 1, 1) == 0


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_hardware(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hardware topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_hardware,
                      'succeed_delete_hardware')

        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_hardware,
                        'succeed_delete_hardware')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == ("Hardware ID 300 was not found as a "
                                     "node in the tree.")

        pub.subscribe(on_message, 'fail_delete_hardware')

        pub.sendMessage('request_delete_hardware', node_id=300)

        pub.unsubscribe(on_message, 'fail_delete_hardware')

    @pytest.mark.skip
    def test_do_delete_matrix_row(self, mock_program_dao):
        """do_delete_row() should remove the appropriate row from the hardware matrices."""
        DUT = mmHardware()

        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_requirements', tree=MOCK_RQRMNT_TREE)
        print(DUT.dic_matrices)
        assert DUT.do_select('hrdwr_rqrmnt', 1, 'S1:SS4') == 0

        DATAMGR.tree.remove_node(1)
        pub.sendMessage('succeed_delete_hardware', node_id=1,
                        tree=DATAMGR.tree)

        with pytest.raises(KeyError):
            DUT.do_select('hrdwr_rqrmnt', 1, 'S1:SS4')

    @pytest.mark.skip
    def test_do_delete_matrix_column(self, test_program_dao):
        """do_delete_column() should remove the appropriate column from the requested hardware matrix."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = mmHardware()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('hrdwr_rqrmnt', 1, 1) == 0

        # pub.sendMessage('succeed_delete_requirement', node_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('hrdwr_rqrmnt', 1, 1)


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    @pytest.mark.unit
    def test_do_get_attributes_hardware(self, mock_program_dao):
        """do_get_attributes() should return a dict of hardware attributes on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

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
        """get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes['hardware_id'] == 2
            assert attributes['application_id'] == 0
            assert attributes['comp_ref_des'] == 'S1:SS1'
            assert attributes['hazard_rate_active'] == 0.0
            assert attributes['mtbf_alloc'] == 0.0
            assert attributes['piE'] == 0.0
            assert attributes['ref_des'] == 'SS1'

        pub.subscribe(on_message, 'succeed_get_all_hardware_attributes')

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)

    @pytest.mark.unit
    def test_get_all_attributes_analysis_manager(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on success."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)

        assert DUT._attributes['hardware_id'] == 2
        assert DUT._attributes['application_id'] == 0
        assert DUT._attributes['comp_ref_des'] == 'S1:SS1'
        assert DUT._attributes['hazard_rate_active'] == 0.0
        assert DUT._attributes['mtbf_alloc'] == 0.0
        assert DUT._attributes['piE'] == 0.0
        assert DUT._attributes['ref_des'] == 'SS1'

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao, test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree attribute in response to the succeed_get_hardware_tree message."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(dmtree):
            assert isinstance(dmtree, Tree)
            assert isinstance(DUT._tree, Tree)
            assert DUT._tree == dmtree
            assert isinstance(DUT._tree.get_node(1).data['nswc'], RAMSTKNSWC)

        pub.subscribe(on_message, 'succeed_get_hardware_tree')

        pub.sendMessage('request_get_hardware_tree')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        pub.sendMessage('request_set_hardware_attributes',
                        node_id=2,
                        key='name',
                        value='Testing set name from moduleview.')
        assert DUT.do_select(
            2, table='hardware').name == 'Testing set name from moduleview.'

        pub.sendMessage('request_set_hardware_attributes',
                        node_id=2,
                        key='lambdaBD',
                        value=0.003862)
        assert DUT.do_select(2, table='mil_hdbk_217f').lambdaBD == 0.003862

        pub.sendMessage('request_set_hardware_attributes',
                        node_id=1,
                        key='reliability_goal',
                        value=0.9995)
        assert DUT.do_select(1, table='reliability').reliability_goal == 0.9995
        assert DUT.do_select(1, table='allocation').reliability_goal == 0.9995
        pub.sendMessage('request_set_hardware_attributes',
                        node_id=1,
                        key='change_factor_5',
                        value=0.95)
        assert DUT.do_select(1, table='similar_item').change_factor_5 == 0.95

    @pytest.mark.unit
    @pytest.mark.parametrize("method_id", [1, 2, 3, 4])
    def test_do_get_allocation_goal(self, mock_program_dao,
                                    test_toml_user_configuration, method_id):
        """do_calculate_goal() should return the proper allocation goal measure."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_hardware_tree')
        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)

        DUT._attributes['allocation_method_id'] = method_id
        DUT._attributes['hazard_rate_goal'] = 0.00002681
        DUT._attributes['reliability_goal'] = 0.9995

        _goal = DUT.do_get_allocation_goal()

        if method_id in [2, 4]:
            assert _goal == 0.00002681
        else:
            assert _goal == 0.9995


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    @pytest.mark.unit
    def test_do_insert_sibling_assembly(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new sibling hardware assembly."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 3
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert isinstance(
                tree.get_node(node_id).data['mil_hdbk_217f'],
                RAMSTKMilHdbkF)
            assert isinstance(
                tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
            assert isinstance(
                tree.get_node(node_id).data['reliability'],
                RAMSTKReliability)
            assert isinstance(
                tree.get_node(node_id).data['allocation'],
                RAMSTKAllocation)
            assert isinstance(
                tree.get_node(node_id).data['similar_item'],
                RAMSTKSimilarItem)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 1
            assert tree.get_node(node_id).data['hardware'].part == 0

        pub.subscribe(on_message, 'succeed_insert_hardware')

        pub.sendMessage('request_insert_hardware', parent_id=1, part=0)

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.unit
    def test_do_insert_child_assembly(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new child hardware assembly."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 3
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert isinstance(
                tree.get_node(node_id).data['mil_hdbk_217f'],
                RAMSTKMilHdbkF)
            assert isinstance(
                tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
            assert isinstance(
                tree.get_node(node_id).data['reliability'],
                RAMSTKReliability)
            assert isinstance(
                tree.get_node(node_id).data['allocation'],
                RAMSTKAllocation)
            assert isinstance(
                tree.get_node(node_id).data['similar_item'],
                RAMSTKSimilarItem)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 2
            assert tree.get_node(node_id).data['hardware'].part == 0

        pub.subscribe(on_message, 'succeed_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=2, part=0) is None

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.unit
    def test_do_insert_part(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new hardware part."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(node_id, tree):
            assert node_id == 3
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(node_id).data['hardware'], RAMSTKHardware)
            assert isinstance(
                tree.get_node(node_id).data['design_electric'],
                RAMSTKDesignElectric)
            assert isinstance(
                tree.get_node(node_id).data['design_mechanic'],
                RAMSTKDesignMechanic)
            assert isinstance(
                tree.get_node(node_id).data['mil_hdbk_217f'],
                RAMSTKMilHdbkF)
            assert isinstance(
                tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
            assert isinstance(
                tree.get_node(node_id).data['reliability'],
                RAMSTKReliability)
            assert isinstance(
                tree.get_node(node_id).data['allocation'],
                RAMSTKAllocation)
            assert isinstance(
                tree.get_node(node_id).data['similar_item'],
                RAMSTKSimilarItem)
            assert tree.get_node(node_id).data['hardware'].revision_id == 1
            assert tree.get_node(node_id).data['hardware'].parent_id == 2
            assert tree.get_node(node_id).data['hardware'].part == 1

        pub.subscribe(on_message, 'succeed_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=2, part=1) is None

        pub.unsubscribe(on_message, 'succeed_insert_hardware')

    @pytest.mark.integration
    def test_do_insert_part_to_part(self, test_program_dao):
        """do_insert() should send the fail message when attempting to add a child to a hardware part."""
        DUT = dmHardware()
        DUT.do_connect(test_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == (
                'Attempting to insert a hardware assembly or '
                'component/piece part as a child of another '
                'component/piece part.')

        pub.subscribe(on_message, 'fail_insert_hardware')

        assert DUT._do_insert_hardware(parent_id=8, part=1) is None

        pub.unsubscribe(on_message, 'fail_insert_hardware')

    @pytest.mark.skip
    def test_do_insert_matrix_row(self, test_program_dao):
        """do_insert_row() should add a row to the end of each hardware matrix."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = mmHardware()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('hrdwr_rqrmnt', 1, 12)

        pub.sendMessage('succeed_insert_hardware', node_id=12)

        assert DUT.do_select('hrdwr_rqrmnt', 1, 12) == 0

    @pytest.mark.skip
    def test_do_insert_matrix_column(self, test_program_dao):
        """do_insert_column() should add a column to the right of the requested hardware matrix."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = mmHardware()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('hrdwr_rqrmnt', 4, 8)

        # pub.sendMessage('succeed_insert_requirement', node_id=6)

        assert DUT.do_select('hrdwr_rqrmnt', 6, 8) == 0

    @pytest.mark.unit
    def test_do_make_comp_ref_des(self, mock_program_dao):
        """do_make_comp_ref_des() should return a zero error code on success."""
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

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
    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """ do_update() should return a zero error code on success. """
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(node_id):
            DUT._do_select_all_hardware(attributes={'revision_id': 1})
            _hardware = DUT.do_select(node_id, table='hardware')
            assert node_id == 2
            assert _hardware.parent_id == 1
            assert _hardware.cost == 0.9832
            _hardware = DUT.do_select(node_id, table='allocation')
            assert _hardware.parent_id == 1
            assert _hardware.mtbf_goal == 12000

        pub.subscribe(on_message, 'succeed_update_hardware')

        _hardware = DUT.do_select(2, table='hardware')
        _hardware.cost = 0.9832
        _hardware = DUT.do_select(2, table='allocation')
        _hardware.mtbf_goal = 12000

        pub.sendMessage('request_update_hardware', node_id=2)

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Hardware ID that doesn't exist. """
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(error_message):
            assert error_message == (
                'Attempted to save non-existent hardware item '
                'with hardware ID 100.')

        pub.subscribe(on_message, 'fail_update_hardware')

        DUT.do_update(100)

    @pytest.mark.unit
    def test_do_update_all(self, mock_program_dao):
        """ do_update_all() should return a zero error code on success. """
        DUT = dmHardware()
        DUT.do_connect(mock_program_dao)
        DUT._do_select_all_hardware(attributes={'revision_id': 1})

        def on_message(node_id):
            assert DUT.do_select(node_id,
                                 table='hardware').hardware_id == node_id

        pub.subscribe(on_message, 'succeed_update_hardware')

        pub.sendMessage('request_update_all_hardware')

    @pytest.mark.skip
    def test_do_update_matrix_manager(self, test_program_dao):
        """do_update() should ."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = mmHardware()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        def on_message():
            assert True

        pub.subscribe(on_message, 'succeed_update_matrix')

        pub.sendMessage('succeed_select_revision', revision_id=1)

        DUT.dic_matrices['hrdwr_rqrmnt'][1][2] = 1
        DUT.dic_matrices['hrdwr_rqrmnt'][1][3] = 2
        DUT.dic_matrices['hrdwr_rqrmnt'][2][2] = 2
        DUT.dic_matrices['hrdwr_rqrmnt'][3][5] = 1

        pub.sendMessage('request_update_hardware_matrix',
                        revision_id=1,
                        matrix_type='hrdwr_rqrmnt')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_assembly_specified_hazard_rate(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should calculate reliability metrics and update the _attributes dict with results when specifying the h(t)."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert float(
                DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER) == 1000000.0
            assert attributes['hazard_rate_type_id'] == 2
            assert attributes['hazard_rate_active'] == pytest.approx(
                3.1095e-06)
            assert attributes['hazard_rate_dormant'] == 2.3876e-08
            assert attributes['hazard_rate_software'] == 3.876e-07
            assert attributes['hazard_rate_logistics'] == pytest.approx(
                3.520976e-06)
            assert attributes['mtbf_logistics'] == pytest.approx(
                284012.16026465)
            assert attributes['reliability_logistics'] == pytest.approx(
                0.02957056)
            assert attributes['hazard_rate_mission'] == pytest.approx(
                3.4971e-06)
            assert attributes['mtbf_mission'] == pytest.approx(285951.21672243)
            assert attributes['reliability_mission'] == pytest.approx(
                0.99996479)
            assert attributes['hr_specified_variance'] == pytest.approx(
                5.70063376e-12)
            assert attributes['hr_logistics_variance'] == pytest.approx(
                1.2397272e-11)
            assert attributes['hr_mission_variance'] == pytest.approx(
                1.22297084e-11)
            assert attributes['mtbf_logistics_variance'] == 80662907178.19547
            assert attributes['mtbf_mission_variance'] == 81768098345.03651
            assert attributes['total_part_count'] == 10
            assert attributes['total_power_dissipation'] == 0.0
            assert attributes['cost_type_id'] == 2
            assert attributes['total_cost'] == 5.28
            assert attributes['cost_hour'] == pytest.approx(1.8464688e-05)

        pub.subscribe(on_message, 'succeed_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 2)
        DATAMGR.do_set_attributes(1, 'hazard_rate_specified', 2.3876)
        DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.023876)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.3876)
        DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.1)
        DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.25)
        DATAMGR.do_set_attributes(1, 'mission_time', 10.0)
        DATAMGR.do_set_attributes(1, 'quantity', 1)
        DATAMGR.do_set_attributes(1, 'cost_type_id', 2)
        DATAMGR.do_set_attributes(1, 'cost', 5.28)
        DATAMGR.do_set_attributes(1, 'total_part_count', 10)

        pub.sendMessage('request_calculate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_calculate_assembly_specified_mtbf(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should calculate reliability metrics and update the _attributes dict with results when specifying the MTBF."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert float(
                DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER) == 1000000.0
            assert attributes['hazard_rate_type_id'] == 3
            assert attributes['hazard_rate_active'] == pytest.approx(
                3.50877193e-06)
            assert attributes['hazard_rate_dormant'] == 0.0
            assert attributes['hazard_rate_software'] == 0.0
            assert attributes['hazard_rate_logistics'] == pytest.approx(
                3.50877193e-06)
            assert attributes['mtbf_logistics'] == 285000.0
            assert attributes['reliability_logistics'] == pytest.approx(
                0.029933652)
            assert attributes['hazard_rate_mission'] == pytest.approx(
                3.50877193e-06)
            assert attributes['mtbf_mission'] == 285000.0
            assert attributes['reliability_mission'] == pytest.approx(
                0.99996479)
            assert attributes['mtbf_specified_variance'] == 81225000000.0

        pub.subscribe(on_message, 'succeed_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 3)
        DATAMGR.do_set_attributes(1, 'mtbf_specified', 285000.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)
        DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.0)
        DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.0)
        DATAMGR.do_set_attributes(1, 'mission_time', 10.0)

        pub.sendMessage('request_calculate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_calculate_assembly_zero_hazard_rates(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the fail message when all hazard rates=0.0."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == (
                "Failed to calculate hazard rate and/or MTBF "
                "metrics for hardware ID 1; too many inputs "
                "equal to zero.  Specified MTBF=285000.000000, "
                "active h(t)=0.000000, dormant h(t)=0.000000, "
                "and software h(t)=0.000000.")

        pub.subscribe(on_message, 'fail_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 2)
        DATAMGR.do_set_attributes(1, 'hazard_rate_specified', 0.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)

        pub.sendMessage('request_calculate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_calculate_assembly_zero_specified_mtbf(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the fail message when the specified MTBF=0.0."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == (
                "Failed to calculate hazard rate and/or MTBF "
                "metrics for hardware ID 1; too many inputs "
                "equal to zero.  Specified MTBF=0.000000, active "
                "h(t)=0.000000, dormant h(t)=0.000000, and "
                "software h(t)=0.000000.")

        pub.subscribe(on_message, 'fail_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 3)
        DATAMGR.do_set_attributes(1, 'mtbf_specified', 0.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)

        pub.sendMessage('request_calculate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_calculate_all_hardware(self, mock_program_dao,
                                       test_toml_user_configuration):
        """do_calculate_all_hardware() should calculate the entire system and roll-up results from child to parent hardware items."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(module_tree):
            assert isinstance(module_tree, Tree)
            assert DUT._attributes['hazard_rate_active'] == pytest.approx(
                2.6265115e-05)
            assert DUT._attributes['hazard_rate_dormant'] == pytest.approx(
                3.5e-09)
            assert DUT._attributes['hazard_rate_software'] == 4.5e-08
            assert DUT._attributes['total_cost'] == pytest.approx(1721.14)
            assert DUT._attributes['total_part_count'] == 144
            assert DUT._attributes['total_power_dissipation'] == pytest.approx(
                50.56)

        pub.subscribe(on_message, 'succeed_calculate_all_hardware')

        # Do a couple of assemblies with a specified h(t)
        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 2)
        DATAMGR.do_set_attributes(1, 'hazard_rate_specified', 0.15)
        DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0035)
        DATAMGR.do_set_attributes(1, 'total_part_count', 89)
        DATAMGR.do_set_attributes(1, 'total_power_dissipation', 45.89)
        DATAMGR.do_set_attributes(1, 'cost', 438.19)
        DATAMGR.do_set_attributes(1, 'mission_time', 10.0)
        DATAMGR.do_update(1)

        # Do a couple of assemblies with a specified MTBF
        DATAMGR.do_set_attributes(2, 'hazard_rate_type_id', 3)
        DATAMGR.do_set_attributes(2, 'mtbf_specified', 38292)
        DATAMGR.do_set_attributes(2, 'hazard_rate_software', 0.045)
        DATAMGR.do_set_attributes(2, 'total_part_count', 55)
        DATAMGR.do_set_attributes(2, 'total_power_dissipation', 4.67)
        DATAMGR.do_set_attributes(2, 'cost', 1282.95)
        DATAMGR.do_set_attributes(2, 'mission_time', 10.0)
        DATAMGR.do_update(2)

        pub.sendMessage('request_calculate_all_hardware')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestMilHdbk217FPredictions():
    """Class for prediction methods using MIL-HDBK-217F test suite."""
    @pytest.mark.unit
    def test_do_calculate_part_mil_hdbk_217f_parts_count(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should calculate reliability metrics and update the _attributes dict with results when performing a MIL-HDBK-217F parts count prediction."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert float(
                DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER) == 1000000.0
            assert attributes['hazard_rate_type_id'] == 1
            assert attributes['hazard_rate_method_id'] == 1
            assert attributes['hazard_rate_active'] == pytest.approx(9.75e-09)
            assert attributes['hazard_rate_dormant'] == 7.8e-10
            assert attributes['hazard_rate_software'] == 3.876e-07
            assert attributes['hazard_rate_logistics'] == pytest.approx(
                3.9813e-07)
            assert attributes['mtbf_logistics'] == pytest.approx(
                2511742.3956999)
            assert attributes['reliability_logistics'] == pytest.approx(
                0.67157472)
            assert attributes['hazard_rate_mission'] == pytest.approx(
                3.9735e-07)
            assert attributes['mtbf_mission'] == pytest.approx(
                2516672.95834906)
            assert attributes['reliability_mission'] == pytest.approx(
                0.99999603)
            assert attributes['hr_specified_variance'] == 0.0
            assert attributes['hr_logistics_variance'] == pytest.approx(
                1.77431343e-13)
            assert attributes['hr_mission_variance'] == pytest.approx(
                1.57887023e-13)
            assert attributes['mtbf_logistics_variance'] == 6308849862356.259
            assert attributes['mtbf_mission_variance'] == 6333642779285.422
            assert attributes['total_part_count'] == 1
            assert attributes['total_power_dissipation'] == 0.05
            assert attributes['cost_type_id'] == 2
            assert attributes['total_cost'] == 5.28
            assert attributes['cost_hour'] == pytest.approx(2.098008e-06)

        pub.subscribe(on_message, 'succeed_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 1)
        DATAMGR.do_set_attributes(1, 'category_id', 1)
        DATAMGR.do_set_attributes(1, 'subcategory_id', 1)
        DATAMGR.do_set_attributes(1, 'quality_id', 1)
        DATAMGR.do_set_attributes(1, 'environment_active_id', 3)
        DATAMGR.do_set_attributes(1, 'environment_dormant_id', 2)
        DATAMGR.do_set_attributes(1, 'n_elements', 100)
        DATAMGR.do_set_attributes(1, 'power_operating', 0.05)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.3876)
        DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.0)
        DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.0)
        DATAMGR.do_set_attributes(1, 'mission_time', 10.0)
        DATAMGR.do_set_attributes(1, 'quantity', 1)
        DATAMGR.do_set_attributes(1, 'cost_type_id', 2)
        DATAMGR.do_set_attributes(1, 'cost', 5.28)
        DATAMGR.do_set_attributes(1, 'part', 1)
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_calculate_part_mil_hdbk_217f_parts_stress(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should calculate reliability metrics and update the _attributes dict with results when performing a MIL-HDBK-217F part stress prediction."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert float(
                DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER) == 1000000.0
            assert attributes['hazard_rate_type_id'] == 1
            assert attributes['hazard_rate_method_id'] == 2
            assert attributes['voltage_ratio'] == 0.5344
            assert attributes['hazard_rate_active'] == pytest.approx(
                2.75691476e-07)
            assert attributes['hazard_rate_dormant'] == pytest.approx(
                2.75691476e-08)
            assert attributes['hazard_rate_software'] == 0.0
            assert attributes['hazard_rate_logistics'] == pytest.approx(
                3.03260624e-07)
            assert attributes['mtbf_logistics'] == pytest.approx(
                3297493.71115455)
            assert attributes['reliability_logistics'] == pytest.approx(
                0.73840662)
            assert attributes['hazard_rate_mission'] == pytest.approx(
                2.75691476e-07)
            assert attributes['mtbf_mission'] == pytest.approx(
                3627243.08227001)
            assert attributes['reliability_mission'] == pytest.approx(
                0.99999712)
            assert attributes['hr_specified_variance'] == 0.0
            assert attributes['hr_logistics_variance'] == pytest.approx(
                1.77431343e-13)
            assert attributes['hr_mission_variance'] == pytest.approx(
                1.57887023e-13)
            assert attributes['mtbf_logistics_variance'] == 10873464775103.824
            assert attributes['mtbf_mission_variance'] == 13156892377875.629
            assert attributes['total_part_count'] == 1
            assert attributes['total_power_dissipation'] == 0.05
            assert attributes['cost_type_id'] == 2
            assert attributes['total_cost'] == 1.35
            assert attributes['cost_hour'] == pytest.approx(3.7218349e-07)

        pub.subscribe(on_message, 'succeed_calculate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(1, 'category_id', 4)
        DATAMGR.do_set_attributes(1, 'subcategory_id', 1)
        DATAMGR.do_set_attributes(1, 'quality_id', 1)
        DATAMGR.do_set_attributes(1, 'environment_active_id', 3)
        DATAMGR.do_set_attributes(1, 'environment_dormant_id', 2)
        DATAMGR.do_set_attributes(1, 'capacitance', 0.0000033)
        DATAMGR.do_set_attributes(1, 'construction_id', 1)
        DATAMGR.do_set_attributes(1, 'configuration_id', 1)
        DATAMGR.do_set_attributes(1, 'resistance', 0.05)
        DATAMGR.do_set_attributes(1, 'voltage_dc_operating', 3.3)
        DATAMGR.do_set_attributes(1, 'voltage_ac_operating', 0.04)
        DATAMGR.do_set_attributes(1, 'voltage_rated', 6.25)
        DATAMGR.do_set_attributes(1, 'temperature_rated_max', 105.0)
        DATAMGR.do_set_attributes(1, 'temperature_active', 45.0)
        DATAMGR.do_set_attributes(1, 'power_operating', 0.05)
        DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)
        DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.0)
        DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.0)
        DATAMGR.do_set_attributes(1, 'mission_time', 10.0)
        DATAMGR.do_set_attributes(1, 'quantity', 1)
        DATAMGR.do_set_attributes(1, 'cost_type_id', 2)
        DATAMGR.do_set_attributes(1, 'cost', 1.35)
        DATAMGR.do_set_attributes(1, 'part', 1)
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_hardware', node_id=1)


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestStressCalculations():
    """Class for stress-related calculations test suite."""
    @pytest.mark.unit
    def test_do_calculate_part_zero_rated_current(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message when rated current is zero."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == (
                'Failed to calculate current ratio for hardware '
                'ID 10; rated current is zero.')

        pub.subscribe(on_message, 'fail_stress_analysis')

        DATAMGR.do_set_attributes(2, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(2, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(2, 'category_id', 1)
        DATAMGR.do_set_attributes(2, 'current_operating', 0.005)
        DATAMGR.do_set_attributes(2, 'current_rated', 0.0)

    @pytest.mark.unit
    def test_do_calculate_part_zero_rated_power(self, mock_program_dao,
                                                test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message when rated power is zero."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == (
                'Failed to calculate power ratio for hardware '
                'ID 10; rated power is zero.')

        pub.subscribe(on_message, 'fail_stress_analysis')

        DATAMGR.do_set_attributes(2, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(2, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(2, 'category_id', 3)
        DATAMGR.do_set_attributes(2, 'power_operating', 0.05)
        DATAMGR.do_set_attributes(2, 'power_rated', 0.0)

        pub.sendMessage('request_calculate_hardware', node_id=8)

        pub.sendMessage('request_calculate_hardware', node_id=10)

    @pytest.mark.unit
    def test_do_calculate_part_zero_rated_voltage(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate() should send the stress ratio calculation fail message when rated voltage is zero."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == (
                'Failed to calculate voltage ratio for hardware '
                'ID 10; rated voltage is zero.')

        pub.subscribe(on_message, 'fail_stress_analysis')

        DATAMGR.do_set_attributes(2, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(2, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(2, 'category_id', 4)
        DATAMGR.do_set_attributes(2, 'voltage_dc_operating', 3.3)
        DATAMGR.do_set_attributes(2, 'voltage_ac_operating', 0.04)
        DATAMGR.do_set_attributes(2, 'voltage_rated', 0.0)

        pub.sendMessage('request_calculate_hardware', node_id=2)

    @pytest.mark.unit
    def test_do_derating_analysis_current_stress(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and build reason message when a component is current overstressed."""
        test_toml_user_configuration.get_user_configuration()
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['overstress']
            assert attributes['reason'] == (
                'Operating current is greater than '
                'limit in a harsh environment.\n'
                'Operating current is greater than '
                'limit in a mild environment.\n')

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(1, 'category_id', 8)
        DATAMGR.do_set_attributes(1, 'current_ratio', 0.95)
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_derating_analysis_power_stress(self, mock_program_dao,
                                               test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and build reason message when a component is power overstressed."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['overstress']
            assert attributes['reason'] == ('Operating power is greater than '
                                            'limit in a harsh environment.\n'
                                            'Operating power is greater than '
                                            'limit in a mild environment.\n')

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(1, 'category_id', 3)
        DATAMGR.do_set_attributes(1, 'power_ratio', 0.95)
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_derating_analysis_voltage_stress(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute True and build reason message when a component is voltage overstressed."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['overstress']
            assert attributes['reason'] == (
                'Operating voltage is greater than '
                'limit in a harsh environment.\n'
                'Operating voltage is greater than '
                'limit in a mild environment.\n')

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(1, 'category_id', 4)
        DATAMGR.do_set_attributes(1, 'voltage_ratio', 0.95)
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)

    @pytest.mark.unit
    def test_do_derating_analysis_no_overstress(self, mock_program_dao,
                                                test_toml_user_configuration):
        """do_derating_analysis() should set overstress attribute False and the reason message should='' when a component is not overstressed."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert not attributes['overstress']
            assert attributes['reason'] == ''

        pub.subscribe(on_message, 'succeed_derate_hardware')

        DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 1)
        DATAMGR.do_set_attributes(1, 'hazard_rate_method_id', 2)
        DATAMGR.do_set_attributes(1, 'category_id', 4)
        DATAMGR.do_set_attributes(1, 'current_ratio', 0.45)
        DATAMGR.do_set_attributes(1, 'power_ratio', 0.35)
        DATAMGR.do_set_attributes(1, 'voltage_ratio', 0.5344)
        DATAMGR.do_update(1)

        pub.sendMessage('request_derate_hardware', node_id=1)


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestAllocation():
    """Class for allocation methods test suite."""
    @pytest.mark.unit
    def test_do_calculate_goals_reliability_specified(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent h(t) and MTBF goals from a specified reliability goal."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hardware_attributes', node_id=1)
        DUT._attributes['goal_measure_id'] = 1
        DUT._attributes['mission_time'] = 100.0
        DUT._attributes['reliability_goal'] = 0.99732259

        pub.sendMessage('request_calculate_goals')

        assert DUT._attributes['hazard_rate_goal'] == pytest.approx(0.00002681)
        assert DUT._attributes['mtbf_goal'] == pytest.approx(37299.5151063)

    @pytest.mark.unit
    def test_do_calculate_goals_hazard_rate_specified(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent MTBF and R(t) goals from a specified hazard rate goal."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)
        DUT._attributes['goal_measure_id'] = 2
        DUT._attributes['mission_time'] = 100.0
        DUT._attributes['hazard_rate_goal'] = 0.00002681

        pub.sendMessage('request_calculate_goals')

        assert DUT._attributes['mtbf_goal'] == pytest.approx(37299.5151063)
        assert DUT._attributes['reliability_goal'] == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_goals_mtbf_specified(self, mock_program_dao,
                                               test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent h(t) and R(t) goals from a specified MTBF goal."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_all_hardware_attributes', node_id=2)
        DUT._attributes['goal_measure_id'] = 3
        DUT._attributes['mission_time'] = 100.0
        DUT._attributes['mtbf_goal'] = 37300.0

        pub.sendMessage('request_calculate_goals')

        assert DUT._attributes['hazard_rate_goal'] == pytest.approx(
            2.68096515e-05)
        assert DUT._attributes['reliability_goal'] == pytest.approx(0.99732259)

    @pytest.mark.integration
    def test_do_calculate_agree_allocation(self, test_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability goal using the AGREE method."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert isinstance(attributes, dict)
            if attributes['hardware_id'] == 6:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    0.001386164)
                assert attributes['mtbf_alloc'] == pytest.approx(721.4151892)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.8950344)
            elif attributes['hardware_id'] == 7:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    0.002464292)
                assert attributes['mtbf_alloc'] == pytest.approx(405.796044)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.8010865)

        pub.subscribe(on_message, 'succeed_allocate_reliability')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(6, 'allocation')
        _assembly.n_sub_elements = 2
        _assembly.duty_cycle = 80.0
        _assembly.weight_factor = 0.8
        DATAMGR.do_update(6)

        _assembly = DATAMGR.do_select(7, 'allocation')
        _assembly.n_sub_elements = 4
        _assembly.duty_cycle = 90.0
        _assembly.weight_factor = 0.95
        DATAMGR.do_update(7)

        _assembly = DATAMGR.do_select(2, 'allocation')
        _assembly.allocation_method_id = 1
        _assembly.reliability_goal = 0.717
        DATAMGR.do_update(2)

        pub.sendMessage('request_allocate_reliability', node_id=2)

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation(self, test_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability goal using the ARINC method."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert isinstance(attributes, dict)
            if attributes['hardware_id'] == 6:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    2.89e-07)
                assert attributes['mtbf_alloc'] == pytest.approx(
                    3460207.61245675)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.99997110)
            elif attributes['hardware_id'] == 7:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    1.132e-08)
                assert attributes['mtbf_alloc'] == pytest.approx(
                    88339222.61484098)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.99999887)

        pub.subscribe(on_message, 'succeed_allocate_reliability')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(6, 'reliability')
        _assembly.hazard_rate_active = 2.89e-6
        DATAMGR.do_update(6)

        _assembly = DATAMGR.do_select(7, 'reliability')
        _assembly.hazard_rate_active = 1.132e-07
        DATAMGR.do_update(7)

        _assembly = DATAMGR.do_select(2, 'allocation')
        _assembly.allocation_method_id = 2
        _assembly.hazard_rate_goal = 0.000617
        DATAMGR.do_update(2)

        pub.sendMessage('request_allocate_reliability', node_id=2)

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation_zero_parent_hazard_rate(
            self, test_program_dao, test_toml_user_configuration):
        """do_calculate_allocation() should send an error message when attempting to allocate an assembly with a zero hazard rate using the ARINC method."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(error_message):
            assert error_message == ('Failed to allocate the reliability for '
                                     'hardware ID 2; zero hazard rate.')

        pub.subscribe(on_message, 'fail_calculate_arinc_weight_factor')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(2, 'allocation')
        _assembly.allocation_method_id = 2
        _assembly.hazard_rate_goal = 0.0
        DATAMGR.do_update(2)

        DUT.do_calculate_allocation(2)

    @pytest.mark.integration
    def test_do_calculate_equal_allocation(self, test_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability goal using the equal apportionment method."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes['hazard_rate_alloc'] == pytest.approx(
                2.50627091e-05)
            assert attributes['mtbf_alloc'] == pytest.approx(39899.91645767)
            assert attributes['reliability_alloc'] == pytest.approx(0.99749687)

        pub.subscribe(on_message, 'succeed_allocate_reliability')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(2, 'allocation')
        _assembly.allocation_method_id = 3
        _assembly.reliability_goal = 0.995
        DATAMGR.do_update(2)

        pub.sendMessage('request_allocate_reliability', node_id=2)

    @pytest.mark.integration
    def test_do_calculate_foo_allocation(self, test_program_dao,
                                         test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability goal using the feasibility of objectives method."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert isinstance(attributes, dict)
            if attributes['hardware_id'] == 6:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    0.00015753191)
                assert attributes['mtbf_alloc'] == pytest.approx(6347.92004322)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.98437024)
            elif attributes['hardware_id'] == 7:
                assert attributes['hazard_rate_alloc'] == pytest.approx(
                    0.00045946809)
                assert attributes['mtbf_alloc'] == pytest.approx(2176.42972910)
                assert attributes['reliability_alloc'] == pytest.approx(
                    0.95509276)

        pub.subscribe(on_message, 'succeed_allocate_reliability')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(6, 'allocation')
        _assembly.env_factor = 6
        _assembly.soa_factor = 2
        _assembly.op_time_factor = 9
        _assembly.int_factor = 3
        DATAMGR.do_update(6)

        _assembly = DATAMGR.do_select(7, 'allocation')
        _assembly.env_factor = 3
        _assembly.soa_factor = 7
        _assembly.op_time_factor = 9
        _assembly.int_factor = 5
        DATAMGR.do_update(7)

        _assembly = DATAMGR.do_select(2, 'allocation')
        _assembly.allocation_method_id = 4
        _assembly.hazard_rate_goal = 0.000617
        DATAMGR.do_update(2)

        pub.sendMessage('request_allocate_reliability', node_id=2)


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestSimilarItem():
    """Class for similar item methods test suite."""
    @pytest.mark.unit
    def test_do_calculate_topic_633(self, mock_program_dao,
                                    test_toml_user_configuration):
        """do_calculate_goal() should calculate the Topic 6.3.3 similar item."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(2, 'reliability')
        _assembly.hazard_rate_active = 0.00617
        _assembly = DATAMGR.do_select(2, 'similar_item')
        _assembly.similar_item_method_id = 1
        _assembly.change_description_1 = ('Test change description for '
                                          'factor #1.')
        _assembly.environment_from_id = 2
        _assembly.environment_to_id = 3
        _assembly.quality_from_id = 1
        _assembly.quality_to_id = 2
        _assembly.temperature_from = 55.0
        _assembly.temperature_to = 65.0
        DATAMGR.do_update(2)

        pub.sendMessage('request_calculate_similar_item', node_id=2)

        assert DUT._attributes['change_factor_1'] == 0.8
        assert DUT._attributes['change_factor_2'] == 1.4
        assert DUT._attributes['change_factor_3'] == 1.0
        assert DUT._attributes['result_1'] == pytest.approx(0.0055089286)

    @pytest.mark.integration
    def test_do_calculate_user_defined(self, test_program_dao,
                                       test_toml_user_configuration):
        """do_calculate_goal() should calculate the Topic 644 similar item."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(2, 'similar_item')
        _assembly.similar_item_method_id = 2
        _assembly.change_description_1 = ('Test change description for '
                                          'factor #1.')
        _assembly.change_factor_1 = 0.85
        _assembly.change_factor_2 = 1.2
        _assembly.function_1 = 'pi1*pi2*hr'
        _assembly.function_2 = '0'
        _assembly.function_3 = '0'
        _assembly.function_4 = '0'
        _assembly.function_5 = '0'
        _assembly.hazard_rate_active = 0.00617
        DATAMGR.do_update(2)

        pub.sendMessage('request_calculate_similar_item', node_id=2)

        assert DUT._attributes['change_description_1'] == (
            'Test change description for factor #1.')
        assert DUT._attributes['change_factor_1'] == 0.85
        assert DUT._attributes['change_factor_2'] == 1.2
        assert DUT._attributes['result_1'] == pytest.approx(0.0062934)

    @pytest.mark.integration
    def test_do_roll_up_change_descriptions(self, test_program_dao,
                                            test_toml_user_configuration):
        """do_roll_up_change_descriptions() should combine all child change descriptions into a single change description for the parent."""
        DATAMGR = dmHardware()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR._do_select_all_hardware(attributes={'revision_id': 1})
        DUT = amHardware(test_toml_user_configuration)

        def on_message(attributes):
            assert attributes['change_description_1'] == (
                'Test Assembly 6:\nThis is change decription 1 for assembly '
                '6\n\nTest Assembly 7:\nThis is change decription 1 for '
                'assembly 7\n\n')
            assert attributes['change_description_2'] == (
                'Test Assembly 6:\nThis is change decription 2 for assembly '
                '6\n\nTest Assembly 7:\nThis is change decription 2 for '
                'assembly 7\n\n')
            assert attributes['change_description_3'] == (
                'Test Assembly 6:\nThis is change decription 3 for assembly '
                '6\n\nTest Assembly 7:\nThis is change decription 3 for '
                'assembly 7\n\n')

        pub.subscribe(on_message, 'succeed_roll_up_change_descriptions')

        pub.sendMessage('request_get_hardware_tree')

        _assembly = DATAMGR.do_select(6, 'hardware')
        _assembly.name = 'Test Assembly 6'
        _assembly = DATAMGR.do_select(6, 'similar_item')
        _assembly.change_description_1 = ('This is change decription 1 for '
                                          'assembly 6')
        _assembly.change_description_2 = ('This is change decription 2 for '
                                          'assembly 6')
        _assembly.change_description_3 = ('This is change decription 3 for '
                                          'assembly 6')
        DATAMGR.do_update(6)

        _assembly = DATAMGR.do_select(7, 'hardware')
        _assembly.name = 'Test Assembly 7'
        _assembly = DATAMGR.do_select(7, 'similar_item')
        _assembly.change_description_1 = ('This is change decription 1 for '
                                          'assembly 7')
        _assembly.change_description_2 = ('This is change decription 2 for '
                                          'assembly 7')
        _assembly.change_description_3 = ('This is change decription 3 for '
                                          'assembly 7')
        DATAMGR.do_update(7)

        pub.sendMessage('request_roll_up_change_descriptions', node_id=2)
