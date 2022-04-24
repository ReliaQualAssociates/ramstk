# -*- coding: utf-8 -*-
#
#       tests.models.commondb.group.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Group module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKGroupRecord
from ramstk.models.dbtables import RAMSTKGroupTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _group_1 = RAMSTKGroupRecord()
    _group_1.group_id = 1
    _group_1.group_type = "work"
    _group_1.description = "Engineering, RMS"

    _group_2 = RAMSTKGroupRecord()
    _group_2.group_id = 2
    _group_2.group_type = "work"
    _group_2.description = "Engineering, Design"

    dao = MockDAO()
    dao.table = [
        _group_1,
        _group_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Group attributes."""
    yield {
        "group_id": 1,
        "group_type": "work",
        "description": "Engineering, RMS",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKGroupTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_group_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_group_attributes")
    pub.unsubscribe(dut.do_update, "request_update_group")
    pub.unsubscribe(dut.do_get_tree, "request_get_group_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_group_attributes")

    # Delete the device under test.
    del dut
