# -*- coding: utf-8 -*-
#
#       tests.models.programdb.program_status.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Program Status module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramStatusRecord
from ramstk.models.dbtables import RAMSTKProgramStatusTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _status_1 = RAMSTKProgramStatusRecord()
    _status_1.revision_id = 1
    _status_1.status_id = 1
    _status_1.cost_remaining = 284.98
    _status_1.date_status = date.today() - timedelta(days=1)
    _status_1.time_remaining = 125.0

    _status_2 = RAMSTKProgramStatusRecord()
    _status_2.revision_id = 1
    _status_2.status_id = 2
    _status_2.cost_remaining = 212.32
    _status_2.date_status = date.today()
    _status_2.time_remaining = 112.5

    dao = MockDAO()
    dao.table = [
        _status_1,
        _status_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Program Status attributes."""
    yield {
        "revision_id": 1,
        "status_id": 1,
        "cost_remaining": 0.0,
        "date_status": date.today(),
        "time_remaining": 0.0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramStatusTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_program_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_program_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_program_status")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_program_status_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_program_status")
    pub.unsubscribe(dut.do_insert, "request_insert_program_status")
    pub.unsubscribe(dut.do_get_actual_status, "request_get_actual_status")
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_program_remaining")

    # Delete the device under test.
    del dut
