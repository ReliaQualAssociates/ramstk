# -*- coding: utf-8 -*-
#
#       tests.models.programdb.opstress.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Operating Stress module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpStressRecord
from ramstk.models.dbtables import RAMSTKOpStressTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _opstress_1 = RAMSTKOpStressRecord()
    _opstress_1.revision_id = 1
    _opstress_1.hardware_id = 1
    _opstress_1.mode_id = 1
    _opstress_1.mechanism_id = 1
    _opstress_1.opload_id = 1
    _opstress_1.opstress_id = 1
    _opstress_1.description = "Test Operating Stress #1"
    _opstress_1.load_history = 2
    _opstress_1.measurable_parameter = 0
    _opstress_1.remarks = ""

    _opstress_2 = RAMSTKOpStressRecord()
    _opstress_2.revision_id = 1
    _opstress_2.hardware_id = 1
    _opstress_2.mode_id = 1
    _opstress_2.mechanism_id = 1
    _opstress_2.opload_id = 1
    _opstress_2.opstress_id = 2
    _opstress_2.description = "Test Operating Stress #2"
    _opstress_2.load_history = 1
    _opstress_2.measurable_parameter = 1
    _opstress_2.remarks = ""

    dao = MockDAO()
    dao.table = [
        _opstress_1,
        _opstress_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Operating Stress attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "opload_id": 3,
        "opstress_id": 3,
        "description": "",
        "load_history": 4,
        "measurable_parameter": 2,
        "remarks": "",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpStressTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut
