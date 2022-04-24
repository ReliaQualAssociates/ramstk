# -*- coding: utf-8 -*-
#
#       tests.models.programdb.control.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Control module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKControlRecord
from ramstk.models.dbtables import RAMSTKControlTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _control_1 = RAMSTKControlRecord()
    _control_1.revision_id = 1
    _control_1.hardware_id = 1
    _control_1.mode_id = 6
    _control_1.mechanism_id = 3
    _control_1.cause_id = 3
    _control_1.control_id = 1
    _control_1.description = "Test FMEA Control #1 for Cause ID #3."
    _control_1.type_id = "Detection"

    _control_2 = RAMSTKControlRecord()
    _control_2.revision_id = 1
    _control_2.hardware_id = 1
    _control_2.mode_id = 6
    _control_2.mechanism_id = 3
    _control_2.cause_id = 3
    _control_2.control_id = 2
    _control_2.description = "Test FMEA Control #2 for Cause ID #3."
    _control_2.type_id = "Prevention"

    dao = MockDAO()
    dao.table = [
        _control_1,
        _control_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Control attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "control_id": 3,
        "description": "",
        "type_id": "",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKControlTable()
    dut.do_connect(mock_dao)

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
