# -*- coding: utf-8 -*-
#
#       tests.models.commondb.status.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Status module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStatusRecord
from ramstk.models.dbtables import RAMSTKStatusTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _status_1 = RAMSTKStatusRecord()
    _status_1.status_id = 1
    _status_1.status_type = "action"
    _status_1.name = "Initiated"
    _status_1.description = "Action has been initiated."

    _status_2 = RAMSTKStatusRecord()
    _status_2.status_id = 2
    _status_2.status_type = "action"
    _status_2.name = "Assigned"
    _status_2.description = "Action has been assigned."

    dao = MockDAO()
    dao.table = [
        _status_1,
        _status_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Status attributes."""
    yield {
        "status_id": 1,
        "status_type": "action",
        "name": "Initiated",
        "description": "Action has been initiated.",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStatusTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_status")
    pub.unsubscribe(dut.do_get_tree, "request_get_status_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_status_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStatusTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"status_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_status")
    pub.unsubscribe(dut.do_get_tree, "request_get_status_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_status_attributes")

    # Delete the device under test.
    del dut
