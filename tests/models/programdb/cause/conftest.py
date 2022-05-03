# -*- coding: utf-8 -*-
#
#       tests.models.programdb.cause.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Cause module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord
from ramstk.models.dbtables import RAMSTKCauseTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _cause_1 = RAMSTKCauseRecord()
    _cause_1.revision_id = 1
    _cause_1.mode_id = 6
    _cause_1.mechanism_id = 3
    _cause_1.cause_id = 1
    _cause_1.description = "Test Failure Cause #1 for Mechanism ID 3"
    _cause_1.rpn = 0
    _cause_1.rpn_new = 0
    _cause_1.rpn_detection = 3
    _cause_1.rpn_detection_new = 3
    _cause_1.rpn_occurrence_new = 6
    _cause_1.rpn_occurrence = 4

    _cause_2 = RAMSTKCauseRecord()
    _cause_2.revision_id = 1
    _cause_2.hardware_id = 1
    _cause_2.mode_id = 6
    _cause_2.mechanism_id = 3
    _cause_2.cause_id = 2
    _cause_2.description = "Test Failure Cause #2 for Mechanism ID 3"
    _cause_2.rpn = 0
    _cause_2.rpn_detection = 6
    _cause_2.rpn_detection_new = 3
    _cause_2.rpn_new = 0
    _cause_2.rpn_occurrence = 6
    _cause_2.rpn_occurrence_new = 4

    dao = MockDAO()
    dao.table = [
        _cause_1,
        _cause_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Cause attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "description": "Test Failure Cause #1 for Mechanism ID 3",
        "rpn": 0,
        "rpn_detection": 10,
        "rpn_detection_new": 10,
        "rpn_new": 0,
        "rpn_occurrence": 10,
        "rpn_occurrence_new": 10,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCauseTable()
    dut.do_connect(mock_dao)

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
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_cause_rpn")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCauseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

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
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_cause_rpn")

    # Delete the device under test.
    del dut
