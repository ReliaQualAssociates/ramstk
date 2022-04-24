# -*- coding: utf-8 -*-
#
#       tests.models.commondb.model.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Model module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModelRecord
from ramstk.models.dbtables import RAMSTKModelTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _model_1 = RAMSTKModelRecord()
    _model_1.model_id = 1
    _model_1.model_type = "damage"
    _model_1.description = "Trump, Donald"

    _model_2 = RAMSTKModelRecord()
    _model_2.model_id = 2
    _model_2.model_type = "damage"
    _model_2.description = "Biden, Joe"

    dao = MockDAO()
    dao.table = [
        _model_1,
        _model_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Model attributes."""
    yield {
        "model_id": 1,
        "model_type": "damage",
        "description": "Trump, Donald",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKModelTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_model_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_model_attributes")
    pub.unsubscribe(dut.do_update, "request_update_model")
    pub.unsubscribe(dut.do_get_tree, "request_get_model_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_model_attributes")

    # Delete the device under test.
    del dut
