# -*- coding: utf-8 -*-
#
#       tests.models.programdb.fmea.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK FMEA module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbtables import (
    RAMSTKActionTable,
    RAMSTKCauseTable,
    RAMSTKControlTable,
    RAMSTKMechanismTable,
    RAMSTKModeTable,
)
from ramstk.models.dbviews import RAMSTKFMEAView
from tests import MockDAO


@pytest.fixture
def test_attributes():
    """Create a dict of FMEA attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "control_id": 1,
        "action_id": 1,
        "mode_description": "Test FMEA Mode #6 for Hardware ID #1.",
        "mechanism_description": "Test FMEA Mechanism #3 for Mode ID #6.",
        "cause_description": "Test FMEA Cause #3 for Mechanism ID #3.",
        "control_description": "Test FMEA Control #1 for Cause ID #3.",
        "action_description": "Test FMEA Action #1 for Cause ID #3.",
        "mission": "Big Mission",
        "mission_phase": "Phase 1",
        "effect_local": "Local Effect",
        "effect_next": "Next Effect",
        "effect_end": "End Effect",
        "detection_method": "Detection Method",
        "other_indications": "Other Indications",
        "isolation_method": "Isolation Method",
        "design_provisions": "Design Provisions",
        "operator_actions": "Operations Actions",
        "severity_class": "III",
        "hazard_rate_source": "MIL-HDBK-217FN2",
        "mode_probability": "Maybe?",
        "effect_probability": 1.0,
        "hazard_rate_active": 0.000035,
        "mode_ratio": 0.5,
        "mode_hazard_rate": 0.0,
        "mode_op_time": 1.0,
        "mode_criticality": 0.5,
        "type_id": 1,
        "rpn_severity": 5,
        "rpn_occurrence": 6,
        "rpn_detection": 3,
        "rpn": 90,
        "action_category": "",
        "action_owner": "weibullguy",
        "action_due_date": date.today(),
        "action_status": "Closed",
        "action_taken": "Basically just screwed around",
        "action_approved": 1,
        "action_approve_date": date.today(),
        "action_closed": 1,
        "action_close_date": date.today(),
        "rpn_severity_new": 5,
        "rpn_occurrence_new": 3,
        "rpn_detection_new": 3,
        "rpn_new": 45,
        "single_point": 1,
        "pof_include": 1,
        "remarks": "Say something about this failure mode.",
        "hardware_description": "Capacitor, Ceramic, 10uF",
    }


@pytest.fixture(scope="function")
def unit_test_view_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFMEAView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_view_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFMEAView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_mode(test_program_dao):
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
def test_mechanism(test_program_dao):
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
def test_cause(test_program_dao):
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
def test_control(test_program_dao):
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
def test_action(test_program_dao):
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
