# -*- coding: utf-8 -*-
#
#       tests.models.programdb.action.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Action module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKActionRecord
from ramstk.models.dbtables import RAMSTKActionTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _action_1 = RAMSTKActionRecord()
    _action_1.revision_id = 1
    _action_1.hardware_id = 1
    _action_1.mode_id = 6
    _action_1.mechanism_id = 3
    _action_1.cause_id = 3
    _action_1.action_id = 1
    _action_1.description = "Test FMEA Action #1 for Cause ID #3."
    _action_1.action_category = "Detection"
    _action_1.action_owner = ""
    _action_1.action_due_date = date.today() + timedelta(days=30)
    _action_1.action_status = ""
    _action_1.action_taken = ""
    _action_1.action_approved = 0
    _action_1.action_approve_date = date.today() + timedelta(days=30)
    _action_1.action_closed = 0
    _action_1.action_close_date = date.today() + timedelta(days=30)

    _action_2 = RAMSTKActionRecord()
    _action_2.revision_id = 1
    _action_2.hardware_id = 1
    _action_2.mode_id = 6
    _action_2.mechanism_id = 3
    _action_2.cause_id = 3
    _action_2.action_id = 2
    _action_2.description = "Test FMEA Action #2 for Cause ID #3."
    _action_2.action_category = "Detection"
    _action_2.action_owner = ""
    _action_2.action_due_date = date.today() + timedelta(days=23)
    _action_2.action_status = ""
    _action_2.action_taken = ""
    _action_2.action_approved = 0
    _action_2.action_approve_date = date.today() + timedelta(days=23)
    _action_2.action_closed = 0
    _action_2.action_close_date = date.today() + timedelta(days=22)

    dao = MockDAO()
    dao.table = [
        _action_1,
        _action_2,
    ]

    yield dao


@pytest.fixture
def test_attributes():
    """Create a dict of Action attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "action_id": 1,
        "description": "Test FMEA Action #1 for Cause ID #3.",
        "action_category": "",
        "action_owner": "weibullguy",
        "action_due_date": date.today(),
        "action_status": "Closed",
        "action_taken": "Basically just screwed around",
        "action_approved": 1,
        "action_approve_date": date.today(),
        "action_closed": 1,
        "action_close_date": date.today(),
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKActionTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut.do_insert, "request_insert_action")

    # Delete the device under test.
    del dut
