# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_method.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Test Method module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTestMethodRecord
from ramstk.models.dbtables import RAMSTKTestMethodTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _test_method_1 = RAMSTKTestMethodRecord()
    _test_method_1.revision_id = 1
    _test_method_1.hardware_id = 1
    _test_method_1.mode_id = 1
    _test_method_1.mechanism_id = 1
    _test_method_1.opload_id = 1
    _test_method_1.test_method_id = 1
    _test_method_1.description = "Test Test Method #1"
    _test_method_1.boundary_conditions = "Waters"
    _test_method_1.remarks = ""

    _test_method_2 = RAMSTKTestMethodRecord()
    _test_method_2.revision_id = 1
    _test_method_2.hardware_id = 1
    _test_method_2.mode_id = 1
    _test_method_2.mechanism_id = 1
    _test_method_2.opload_id = 1
    _test_method_2.test_method_id = 2
    _test_method_2.description = "Test Test Method #2"
    _test_method_2.boundary_conditions = "Sands"
    _test_method_2.remarks = ""

    dao = MockDAO()
    dao.table = [
        _test_method_1,
        _test_method_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Test Method attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 1,
        "mechanism_id": 1,
        "opload_id": 1,
        "test_method_id": 1,
        "description": "",
        "boundary_conditions": "",
        "remarks": "",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKTestMethodTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_test_method")
    pub.unsubscribe(dut.do_insert, "request_insert_test_method")

    # Delete the device under test.
    del dut
