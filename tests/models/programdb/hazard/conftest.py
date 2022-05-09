# -*- coding: utf-8 -*-
#
#       tests.models.programdb.hazard.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Hazard module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardRecord
from ramstk.models.dbtables import RAMSTKHazardTable
from tests import MockDAO

TEST_PROBS = {
    "A": "Level A - Frequent",
    "B": "Level B - Reasonably Probable",
    "C": "Level C - Occasional",
}


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _hazard_1 = RAMSTKHazardRecord()
    _hazard_1.revision_id = 1
    _hazard_1.function_id = 1
    _hazard_1.hazard_id = 1
    _hazard_1.assembly_effect = ""
    _hazard_1.assembly_hri = 20
    _hazard_1.assembly_hri_f = 4
    _hazard_1.assembly_mitigation = ""
    _hazard_1.assembly_probability = TEST_PROBS["A"]
    _hazard_1.assembly_probability_f = TEST_PROBS["B"]
    _hazard_1.assembly_severity = "Major"
    _hazard_1.assembly_severity_f = "Medium"
    _hazard_1.function_1 = "uf1*uf2"
    _hazard_1.function_2 = "res1/ui1"
    _hazard_1.function_3 = ""
    _hazard_1.function_4 = ""
    _hazard_1.function_5 = ""
    _hazard_1.potential_cause = ""
    _hazard_1.potential_hazard = ""
    _hazard_1.remarks = ""
    _hazard_1.result_1 = 0.0
    _hazard_1.result_2 = 0.0
    _hazard_1.result_3 = 0.0
    _hazard_1.result_4 = 0.0
    _hazard_1.result_5 = 0.0
    _hazard_1.system_effect = ""
    _hazard_1.system_hri = 20
    _hazard_1.system_hri_f = 20
    _hazard_1.system_mitigation = ""
    _hazard_1.system_probability = TEST_PROBS["A"]
    _hazard_1.system_probability_f = TEST_PROBS["C"]
    _hazard_1.system_severity = "Medium"
    _hazard_1.system_severity_f = "Medium"
    _hazard_1.user_blob_1 = ""
    _hazard_1.user_blob_2 = ""
    _hazard_1.user_blob_3 = ""
    _hazard_1.user_float_1 = 1.5
    _hazard_1.user_float_2 = 0.8
    _hazard_1.user_float_3 = 0.0
    _hazard_1.user_int_1 = 2
    _hazard_1.user_int_2 = 0
    _hazard_1.user_int_3 = 0

    _hazard_2 = RAMSTKHazardRecord()
    _hazard_2.revision_id = 1
    _hazard_2.function_id = 1
    _hazard_2.hazard_id = 2
    _hazard_2.assembly_effect = ""
    _hazard_2.assembly_hri = 20
    _hazard_2.assembly_hri_f = 4
    _hazard_2.assembly_mitigation = ""
    _hazard_2.assembly_probability = TEST_PROBS["A"]
    _hazard_2.assembly_probability_f = TEST_PROBS["B"]
    _hazard_2.assembly_severity = "Major"
    _hazard_2.assembly_severity_f = "Medium"
    _hazard_2.function_1 = "uf1*uf2"
    _hazard_2.function_2 = "res1/ui1"
    _hazard_2.function_3 = ""
    _hazard_2.function_4 = ""
    _hazard_2.function_5 = ""
    _hazard_2.potential_cause = ""
    _hazard_2.potential_hazard = ""
    _hazard_2.remarks = ""
    _hazard_2.result_1 = 0.0
    _hazard_2.result_2 = 0.0
    _hazard_2.result_3 = 0.0
    _hazard_2.result_4 = 0.0
    _hazard_2.result_5 = 0.0
    _hazard_2.system_effect = ""
    _hazard_2.system_hri = 20
    _hazard_2.system_hri_f = 20
    _hazard_2.system_mitigation = ""
    _hazard_2.system_probability = TEST_PROBS["A"]
    _hazard_2.system_probability_f = TEST_PROBS["C"]
    _hazard_2.system_severity = "Medium"
    _hazard_2.system_severity_f = "Medium"
    _hazard_2.user_blob_1 = ""
    _hazard_2.user_blob_2 = ""
    _hazard_2.user_blob_3 = ""
    _hazard_2.user_float_1 = 1.5
    _hazard_2.user_float_2 = 0.8
    _hazard_2.user_float_3 = 0.0
    _hazard_2.user_int_1 = 2
    _hazard_2.user_int_2 = 0
    _hazard_2.user_int_3 = 0

    dao = MockDAO()
    dao.table = [
        _hazard_1,
        _hazard_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Hazard attributes."""
    yield {
        "revision_id": 1,
        "function_id": 1,
        "hazard_id": 1,
        "potential_hazard": "",
        "potential_cause": "",
        "assembly_effect": "",
        "assembly_severity": "Major",
        "assembly_probability": TEST_PROBS["A"],
        "assembly_hri": 20,
        "assembly_mitigation": "",
        "assembly_severity_f": "Major",
        "assembly_probability_f": TEST_PROBS["A"],
        "assembly_hri_f": 20,
        "function_1": "",
        "function_2": "",
        "function_3": "",
        "function_4": "",
        "function_5": "",
        "remarks": "",
        "result_1": 0.0,
        "result_2": 0.0,
        "result_3": 0.0,
        "result_4": 0.0,
        "result_5": 0.0,
        "system_effect": "",
        "system_severity": "Major",
        "system_probability": TEST_PROBS["A"],
        "system_hri": 20,
        "system_mitigation": "",
        "system_severity_f": "Major",
        "system_probability_f": TEST_PROBS["A"],
        "system_hri_f": 20,
        "user_blob_1": "",
        "user_blob_2": "",
        "user_blob_3": "",
        "user_float_1": 0.0,
        "user_float_2": 0.0,
        "user_float_3": 0.0,
        "user_int_1": 0,
        "user_int_2": 0,
        "user_int_3": 0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHazardTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hazard")
    pub.unsubscribe(dut.do_update, "request_update_hazard")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazard_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_set_attributes_all, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut.do_delete, "request_delete_hazard")
    pub.unsubscribe(dut.do_insert, "request_insert_hazard")
    pub.unsubscribe(dut.do_calculate_fha, "request_calculate_fha")

    # Delete the device under test.
    del dut
