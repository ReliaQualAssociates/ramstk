# -*- coding: utf-8 -*-
#
#       tests.models.programdb.function.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Function module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFunctionRecord
from ramstk.models.dbtables import RAMSTKFunctionTable
from tests import MockDAO


@pytest.fixture(scope="function")
def unit_test_table_model(mock_program_dao):
    """Get a data manager instance for each unit test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFunctionTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_function")
    pub.unsubscribe(dut.do_update, "request_update_function")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_function_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_function")
    pub.unsubscribe(dut.do_insert, "request_insert_function")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_program_dao):
    """Get a data manager instance for each system test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFunctionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_function")
    pub.unsubscribe(dut.do_update, "request_update_function")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_function_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_function")
    pub.unsubscribe(dut.do_insert, "request_insert_function")

    # Delete the device under test.
    del dut


@pytest.fixture
def mock_program_dao(monkeypatch):
    """Create a mock database table."""
    _function_1 = RAMSTKFunctionRecord()
    _function_1.revision_id = 1
    _function_1.function_id = 1
    _function_1.availability_logistics = 1.0
    _function_1.availability_mission = 1.0
    _function_1.cost = 0.0
    _function_1.function_code = "PRESS-001"
    _function_1.hazard_rate_logistics = 0.0
    _function_1.hazard_rate_mission = 0.0
    _function_1.level = 0
    _function_1.mcmt = 0.0
    _function_1.mmt = 0.0
    _function_1.mpmt = 0.0
    _function_1.mtbf_logistics = 0.0
    _function_1.mtbf_mission = 0.0
    _function_1.mttr = 0.0
    _function_1.name = "Function Name"
    _function_1.parent_id = 0
    _function_1.remarks = ""
    _function_1.safety_critical = 0
    _function_1.total_mode_count = 0
    _function_1.total_part_count = 0
    _function_1.type_id = 0

    _function_2 = RAMSTKFunctionRecord()
    _function_2.revision_id = 1
    _function_2.function_id = 2
    _function_2.availability_logistics = 1.0
    _function_2.availability_mission = 1.0
    _function_2.cost = 0.0
    _function_2.function_code = "PRESS-001"
    _function_2.hazard_rate_logistics = 0.0
    _function_2.hazard_rate_mission = 0.0
    _function_2.level = 0
    _function_2.mcmt = 0.0
    _function_2.mmt = 0.0
    _function_2.mpmt = 0.0
    _function_2.mtbf_logistics = 0.0
    _function_2.mtbf_mission = 0.0
    _function_2.mttr = 0.0
    _function_2.name = "Function Name"
    _function_2.parent_id = 1
    _function_2.remarks = ""
    _function_2.safety_critical = 0
    _function_2.total_mode_count = 0
    _function_2.total_part_count = 0
    _function_2.type_id = 0

    DAO = MockDAO()
    DAO.table = [
        _function_1,
        _function_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Function attributes."""
    yield {
        "revision_id": 1,
        "function_id": 1,
        "availability_logistics": 1.0,
        "availability_mission": 1.0,
        "cost": 0.0,
        "function_code": "Function Code",
        "hazard_rate_logistics": 0.0,
        "hazard_rate_mission": 0.0,
        "level": 0,
        "mmt": 0.0,
        "mcmt": 0.0,
        "mpmt": 0.0,
        "mtbf_logistics": 0.0,
        "mtbf_mission": 0.0,
        "mttr": 0.0,
        "name": "New Function",
        "parent_id": 0,
        "remarks": "",
        "safety_critical": 0,
        "total_mode_count": 0,
        "total_part_count": 0,
        "type_id": 0,
    }


@pytest.fixture(scope="function")
def test_record_model(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
