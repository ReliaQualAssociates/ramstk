# -*- coding: utf-8 -*-
#
#       tests.models.programdb.mode.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Mode module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModeRecord
from ramstk.models.dbtables import RAMSTKModeTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _mode_1 = RAMSTKModeRecord()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ""
    _mode_1.mission = "Default Mission"
    _mode_1.other_indications = ""
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ""
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ""
    _mode_1.detection_method = ""
    _mode_1.operator_actions = ""
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ""
    _mode_1.severity_class = ""
    _mode_1.description = "Test Failure Mode #1"
    _mode_1.mission_phase = ""
    _mode_1.mode_probability = ""
    _mode_1.remarks = ""
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ""
    _mode_1.effect_end = ""
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.8

    _mode_2 = RAMSTKModeRecord()
    _mode_2.revision_id = 1
    _mode_2.hardware_id = 1
    _mode_2.mode_id = 2
    _mode_2.effect_local = ""
    _mode_2.mission = "Default Mission"
    _mode_2.other_indications = ""
    _mode_2.mode_criticality = 0.0
    _mode_2.single_point = 0
    _mode_2.design_provisions = ""
    _mode_2.type_id = 0
    _mode_2.rpn_severity_new = 1
    _mode_2.effect_next = ""
    _mode_2.detection_method = ""
    _mode_2.operator_actions = ""
    _mode_2.critical_item = 0
    _mode_2.hazard_rate_source = ""
    _mode_2.severity_class = ""
    _mode_2.description = "Test Failure Mode #2"
    _mode_2.mission_phase = ""
    _mode_2.mode_probability = ""
    _mode_2.remarks = ""
    _mode_2.mode_ratio = 0.0
    _mode_2.mode_hazard_rate = 0.0
    _mode_2.rpn_severity = 1
    _mode_2.isolation_method = ""
    _mode_2.effect_end = ""
    _mode_2.mode_op_time = 0.0
    _mode_2.effect_probability = 0.0

    dao = MockDAO()
    dao.table = [
        _mode_1,
        _mode_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Mode attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 4,
        "critical_item": 0,
        "description": "",
        "design_provisions": "",
        "detection_method": "",
        "effect_end": "",
        "effect_local": "",
        "effect_next": "",
        "effect_probability": 0.0,
        "hazard_rate_source": "",
        "isolation_method": "",
        "mission": "Default Mission",
        "mission_phase": "",
        "mode_criticality": 0.0,
        "mode_hazard_rate": 0.0,
        "mode_op_time": 0.0,
        "mode_probability": "",
        "mode_ratio": 0.0,
        "operator_actions": "",
        "other_indications": "",
        "remarks": "",
        "rpn_severity": 1,
        "rpn_severity_new": 1,
        "severity_class": "",
        "single_point": 0,
        "type_id": 0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKModeTable()

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
    pub.unsubscribe(dut.do_calculate_criticality, "request_calculate_criticality")

    # Delete the device under test.
    del dut
