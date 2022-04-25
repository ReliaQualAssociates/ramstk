# -*- coding: utf-8 -*-
#
#       tests.models.commondb.load_history.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Load History module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKLoadHistoryRecord
from ramstk.models.dbtables import RAMSTKLoadHistoryTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _history_1 = RAMSTKLoadHistoryRecord()
    _history_1.history_id = 1
    _history_1.description = "Histogram"

    _history_2 = RAMSTKLoadHistoryRecord()
    _history_2.history_id = 2
    _history_2.description = "Waterfall Histogram"

    dao = MockDAO()
    dao.table = [
        _history_1,
        _history_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Load History attributes."""
    yield {
        "history_id": 1,
        "description": "Histogram",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKLoadHistoryTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_load_history_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_load_history_attributes")
    pub.unsubscribe(dut.do_update, "request_update_load_history")
    pub.unsubscribe(dut.do_get_tree, "request_get_load_history_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_load_history_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKLoadHistoryTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"history_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_load_history_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_load_history_attributes")
    pub.unsubscribe(dut.do_update, "request_update_load_history")
    pub.unsubscribe(dut.do_get_tree, "request_get_load_history_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_load_history_attributes")

    # Delete the device under test.
    del dut
