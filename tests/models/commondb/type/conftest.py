# -*- coding: utf-8 -*-
#
#       tests.models.commondb.type.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Type module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTypeRecord
from ramstk.models.dbtables import RAMSTKTypeTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _type_1 = RAMSTKTypeRecord()
    _type_1.type_id = 1
    _type_1.type_type = "incident"
    _type_1.code = "PLN"
    _type_1.description = "Planning"

    _type_2 = RAMSTKTypeRecord()
    _type_2.type_id = 2
    _type_2.type_type = "incident"
    _type_2.code = "PLN"
    _type_2.description = "Planning"

    dao = MockDAO()
    dao.table = [
        _type_1,
        _type_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Type attributes."""
    yield {
        "type_id": 1,
        "type_type": "incident",
        "code": "PLN",
        "description": "Planning",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKTypeTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_type_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_type_attributes")
    pub.unsubscribe(dut.do_update, "request_update_type")
    pub.unsubscribe(dut.do_get_tree, "request_get_type_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_type_attributes")

    # Delete the device under test.
    del dut
