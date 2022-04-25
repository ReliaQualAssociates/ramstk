# -*- coding: utf-8 -*-
#
#       tests.models.commondb.condition.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Condition module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKConditionRecord
from ramstk.models.dbtables import RAMSTKConditionTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _condition_1 = RAMSTKConditionRecord()
    _condition_1.condition_id = 1
    _condition_1.description = "Cavitation"
    _condition_1.condition_type = "operating"

    _condition_2 = RAMSTKConditionRecord()
    _condition_2.condition_id = 2
    _condition_2.description = "Temperature"
    _condition_2.condition_type = "operating"

    dao = MockDAO()
    dao.table = [
        _condition_1,
        _condition_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Condition attributes."""
    yield {
        "condition_id": 1,
        "condition_type": "operating",
        "description": "Cavitation",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each unit test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKConditionTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_condition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_condition_attributes")
    pub.unsubscribe(dut.do_update, "request_update_condition")
    pub.unsubscribe(dut.do_get_tree, "request_get_condition_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_condition_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKConditionTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"condition_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_condition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_condition_attributes")
    pub.unsubscribe(dut.do_update, "request_update_condition")
    pub.unsubscribe(dut.do_get_tree, "request_get_condition_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_condition_attributes")

    # Delete the device under test.
    del dut
