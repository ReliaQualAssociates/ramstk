# -*- coding: utf-8 -*-
#
#       tests.models.commondb.method.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Method module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMethodRecord
from ramstk.models.dbtables import RAMSTKMethodTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _method_1 = RAMSTKMethodRecord()
    _method_1.method_id = 1
    _method_1.method_type = "detection"
    _method_1.name = "Sniff"
    _method_1.description = "Smell Test"

    _method_2 = RAMSTKMethodRecord()
    _method_2.method_id = 2
    _method_2.method_type = "detection"
    _method_2.name = "Whiff"
    _method_2.description = "Whiff Test"

    dao = MockDAO()
    dao.table = [
        _method_1,
        _method_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Method attributes."""
    yield {
        "method_id": 1,
        "method_type": "detection",
        "name": "Sniff",
        "description": "Smell Test",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMethodTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_method_attributes")
    pub.unsubscribe(dut.do_update, "request_update_method")
    pub.unsubscribe(dut.do_get_tree, "request_get_method_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_method_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMethodTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"method_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_method_attributes")
    pub.unsubscribe(dut.do_update, "request_update_method")
    pub.unsubscribe(dut.do_get_tree, "request_get_method_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_method_attributes")

    # Delete the device under test.
    del dut
