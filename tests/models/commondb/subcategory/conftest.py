# -*- coding: utf-8 -*-
#
#       tests.models.commondb.subcategory.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Subcategory module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSubCategoryRecord
from ramstk.models.dbtables import RAMSTKSubCategoryTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _subcategory_1 = RAMSTKSubCategoryRecord()
    _subcategory_1.category_id = 1
    _subcategory_1.subcategory_id = 1
    _subcategory_1.description = "Linear"

    _subcategory_2 = RAMSTKSubCategoryRecord()
    _subcategory_2.category_id = 1
    _subcategory_2.subcategory_id = 2
    _subcategory_2.description = "Digital"

    dao = MockDAO()
    dao.table = [
        _subcategory_1,
        _subcategory_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Subcategory attributes."""
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "description": "Linear",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSubCategoryTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_subcategory_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_subcategory_attributes")
    pub.unsubscribe(dut.do_update, "request_update_subcategory")
    pub.unsubscribe(dut.do_get_tree, "request_get_subcategory_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_subcategory_attributes")

    # Delete the device under test.
    del dut
