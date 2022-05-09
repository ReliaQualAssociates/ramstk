# -*- coding: utf-8 -*-
#
#       tests.models.programdb.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK program database module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbtables import (
    RAMSTKActionTable,
    RAMSTKCauseTable,
    RAMSTKControlTable,
    RAMSTKEnvironmentTable,
    RAMSTKHardwareTable,
    RAMSTKMechanismTable,
    RAMSTKMissionPhaseTable,
    RAMSTKMissionTable,
    RAMSTKModeTable,
    RAMSTKOpLoadTable,
    RAMSTKOpStressTable,
    RAMSTKTestMethodTable,
)


@pytest.fixture(scope="class")
def test_action_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKActionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_action")
    pub.unsubscribe(dut.do_insert, "request_insert_action")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_cause_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCauseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_cause")
    pub.unsubscribe(dut.do_insert, "request_insert_cause")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_control_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKControlTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_control")
    pub.unsubscribe(dut.do_update, "request_update_control")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_control_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_control")
    pub.unsubscribe(dut.do_insert, "request_insert_control")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_environment_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKEnvironmentTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_hardware_table_model(test_program_dao):
    """Create test hardware table."""
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


@pytest.fixture(scope="class")
def test_mechanism_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMechanismTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_mission_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_mission_phase_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionPhaseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut.do_insert, "request_insert_mission_phase")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_mode_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKModeTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mode")
    pub.unsubscribe(dut.do_insert, "request_insert_mode")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opload_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpLoadTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opstress_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpStressTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "opload_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_test_method_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKTestMethodTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "opload_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_test_method")
    pub.unsubscribe(dut.do_insert, "request_insert_test_method")

    # Delete the device under test.
    del dut
