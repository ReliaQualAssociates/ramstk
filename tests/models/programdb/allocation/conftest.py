# -*- coding: utf-8 -*-
#
#       tests.models.programdb.allocation.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Allocation module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKAllocationRecord
from ramstk.models.dbtables import RAMSTKAllocationTable, RAMSTKHardwareTable
from tests import MockDAO


@pytest.fixture()
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _allocation_1 = RAMSTKAllocationRecord()
    _allocation_1.revision_id = 1
    _allocation_1.hardware_id = 1
    _allocation_1.availability_alloc = 0.0
    _allocation_1.env_factor = 1
    _allocation_1.goal_measure_id = 1
    _allocation_1.hazard_rate_alloc = 0.0
    _allocation_1.hazard_rate_goal = 0.0
    _allocation_1.included = 1
    _allocation_1.int_factor = 1
    _allocation_1.allocation_method_id = 1
    _allocation_1.mission_time = 100.0
    _allocation_1.mtbf_alloc = 0.0
    _allocation_1.mtbf_goal = 0.0
    _allocation_1.n_sub_systems = 1
    _allocation_1.n_sub_elements = 1
    _allocation_1.parent_id = 0
    _allocation_1.percent_weight_factor = 0.0
    _allocation_1.reliability_alloc = 1.0
    _allocation_1.reliability_goal = 0.999
    _allocation_1.op_time_factor = 1
    _allocation_1.soa_factor = 1
    _allocation_1.weight_factor = 1

    _allocation_2 = RAMSTKAllocationRecord()
    _allocation_2.revision_id = 1
    _allocation_2.hardware_id = 2
    _allocation_2.availability_alloc = 0.0
    _allocation_2.env_factor = 1
    _allocation_2.goal_measure_id = 1
    _allocation_2.hazard_rate_alloc = 0.0
    _allocation_2.hazard_rate_goal = 0.0
    _allocation_2.included = 1
    _allocation_2.int_factor = 1
    _allocation_2.allocation_method_id = 1
    _allocation_2.mission_time = 100.0
    _allocation_2.mtbf_alloc = 0.0
    _allocation_2.mtbf_goal = 0.0
    _allocation_2.n_sub_systems = 1
    _allocation_2.n_sub_elements = 1
    _allocation_2.parent_id = 1
    _allocation_2.percent_weight_factor = 0.0
    _allocation_2.reliability_alloc = 1.0
    _allocation_2.reliability_goal = 0.9999
    _allocation_2.op_time_factor = 1
    _allocation_2.soa_factor = 1
    _allocation_2.weight_factor = 1

    _allocation_3 = RAMSTKAllocationRecord()
    _allocation_3.revision_id = 1
    _allocation_3.hardware_id = 3
    _allocation_3.availability_alloc = 0.0
    _allocation_3.env_factor = 1
    _allocation_3.goal_measure_id = 1
    _allocation_3.hazard_rate_alloc = 0.0
    _allocation_3.hazard_rate_goal = 0.0
    _allocation_3.included = 1
    _allocation_3.int_factor = 1
    _allocation_3.allocation_method_id = 1
    _allocation_3.mission_time = 100.0
    _allocation_3.mtbf_alloc = 0.0
    _allocation_3.mtbf_goal = 0.0
    _allocation_3.n_sub_systems = 1
    _allocation_3.n_sub_elements = 1
    _allocation_3.parent_id = 1
    _allocation_3.percent_weight_factor = 0.0
    _allocation_3.reliability_alloc = 1.0
    _allocation_3.reliability_goal = 0.99999
    _allocation_3.op_time_factor = 1
    _allocation_3.soa_factor = 1
    _allocation_3.weight_factor = 1

    dao = MockDAO()
    dao.table = [
        _allocation_1,
        _allocation_2,
        _allocation_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Allocation attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "availability_alloc": 0.0,
        "env_factor": 1,
        "goal_measure_id": 1,
        "hazard_rate_alloc": 0.0,
        "hazard_rate_goal": 0.0,
        "included": 1,
        "int_factor": 1,
        "allocation_method_id": 1,
        "mission_time": 100.0,
        "mtbf_alloc": 0.0,
        "mtbf_goal": 0.0,
        "n_sub_systems": 1,
        "n_sub_elements": 1,
        "parent_id": 7,
        "percent_weight_factor": 0.0,
        "reliability_alloc": 1.0,
        "reliability_goal": 0.999,
        "op_time_factor": 1,
        "soa_factor": 1,
        "weight_factor": 1,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKAllocationTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_allocation")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_allocation")
    pub.unsubscribe(dut.do_update, "request_update_allocation")
    pub.unsubscribe(dut.do_get_tree, "request_get_allocation_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_allocation")
    pub.unsubscribe(dut.do_insert, "request_insert_allocation")
    pub.unsubscribe(
        dut.do_calculate_agree_allocation, "request_calculate_agree_allocation"
    )
    pub.unsubscribe(
        dut.do_calculate_arinc_allocation, "request_calculate_arinc_allocation"
    )
    pub.unsubscribe(
        dut.do_calculate_equal_allocation, "request_calculate_equal_allocation"
    )
    pub.unsubscribe(dut.do_calculate_foo_allocation, "request_calculate_foo_allocation")
    pub.unsubscribe(
        dut.do_calculate_allocation_goals, "request_calculate_allocation_goals"
    )
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_hardware_table(test_program_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_hardware")
    pub.unsubscribe(dut.do_update, "request_update_hardware")
    pub.unsubscribe(dut.do_get_tree, "request_get_hardware_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_hardware")
    pub.unsubscribe(dut.do_insert, "request_insert_hardware")

    # Delete the device under test.
    del dut
