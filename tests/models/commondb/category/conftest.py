# -*- coding: utf-8 -*-
#
#       tests.models.commondb.category.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Category module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCategoryRecord
from ramstk.models.dbtables import RAMSTKCategoryTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _category_1 = RAMSTKCategoryRecord()
    _category_1.category_id = 1
    _category_1.category_type = "hardware"
    _category_1.name = "IC"
    _category_1.value = 1
    _category_1.description = "Integrated Circuit"
    _category_1.harsh_ir_limit = 0.8
    _category_1.mild_ir_limit = 0.9
    _category_1.harsh_pr_limit = 1.0
    _category_1.mild_pr_limit = 1.0
    _category_1.harsh_vr_limit = 1.0
    _category_1.mild_vr_limit = 1.0
    _category_1.harsh_deltat_limit = 0.0
    _category_1.mild_deltat_limit = 0.0
    _category_1.harsh_maxt_limit = 125.0
    _category_1.mild_maxt_limit = 125.0

    _category_2 = RAMSTKCategoryRecord()
    _category_2.category_id = 2
    _category_2.category_type = "hardware"
    _category_2.name = "Semi"
    _category_2.value = 1
    _category_2.description = "Semiconductor"
    _category_2.harsh_ir_limit = 0.8
    _category_2.mild_ir_limit = 0.9
    _category_2.harsh_pr_limit = 1.0
    _category_2.mild_pr_limit = 1.0
    _category_2.harsh_vr_limit = 1.0
    _category_2.mild_vr_limit = 1.0
    _category_2.harsh_deltat_limit = 0.0
    _category_2.mild_deltat_limit = 0.0
    _category_2.harsh_maxt_limit = 125.0
    _category_2.mild_maxt_limit = 125.0

    dao = MockDAO()
    dao.table = [
        _category_1,
        _category_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Category attributes."""
    yield {
        "category_id": 1,
        "category_type": "hardware",
        "name": "IC",
        "value": 1,
        "description": "Integrated Circuit",
        "harsh_ir_limit": 0.8,
        "mild_ir_limit": 0.9,
        "harsh_pr_limit": 1.0,
        "mild_pr_limit": 1.0,
        "harsh_vr_limit": 1.0,
        "mild_vr_limit": 1.0,
        "harsh_deltat_limit": 0.0,
        "mild_deltat_limit": 0.0,
        "harsh_maxt_limit": 125.0,
        "mild_maxt_limit": 125.0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCategoryTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_category_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_category_attributes")
    pub.unsubscribe(dut.do_update, "request_update_category")
    pub.unsubscribe(dut.do_get_tree, "request_get_category_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_category_attributes")

    # Delete the device under test.
    del dut
