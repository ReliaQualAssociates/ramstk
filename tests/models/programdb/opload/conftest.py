# -*- coding: utf-8 -*-
#
#       tests.models.programdb.opload.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Operating Load module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpLoadRecord
from ramstk.models.dbtables import RAMSTKOpLoadTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _opload_1 = RAMSTKOpLoadRecord()
    _opload_1.revision_id = 1
    _opload_1.hardware_id = 1
    _opload_1.mode_id = 6
    _opload_1.mechanism_id = 2
    _opload_1.opload_id = 1
    _opload_1.damage_model = 3
    _opload_1.description = "Test Operating Load #1"
    _opload_1.priority_id = 0

    _opload_2 = RAMSTKOpLoadRecord()
    _opload_2.revision_id = 1
    _opload_2.hardware_id = 1
    _opload_2.mode_id = 6
    _opload_2.mechanism_id = 2
    _opload_2.opload_id = 2
    _opload_2.damage_model = 1
    _opload_2.description = "Test Operating Load #2"
    _opload_2.priority_id = 0

    dao = MockDAO()
    dao.table = [
        _opload_1,
        _opload_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Operating Load attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "opload_id": 3,
        "description": "",
        "damage_model": 2,
        "priority_id": 0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpLoadTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut
