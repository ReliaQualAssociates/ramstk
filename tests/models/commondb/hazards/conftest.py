# -*- coding: utf-8 -*-
#
#       tests.models.commondb.hazards.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Hazards module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardsRecord
from ramstk.models.dbtables import RAMSTKHazardsTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _hazards_1 = RAMSTKHazardsRecord()
    _hazards_1.hazard_id = 1
    _hazards_1.hazard_category = "Common Causes"
    _hazards_1.hazard_subcategory = "Fire"

    _hazards_2 = RAMSTKHazardsRecord()
    _hazards_2.hazard_id = 2
    _hazards_2.hazard_category = "Common Causes"
    _hazards_2.hazard_subcategory = "Dust/Dirt"

    dao = MockDAO()
    dao.table = [
        _hazards_1,
        _hazards_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Hazards attributes."""
    yield {
        "hazard_id": 1,
        "hazard_category": "Common Causes",
        "hazard_subcategory": "Fire",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHazardsTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazards_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazards_attributes")
    pub.unsubscribe(dut.do_update, "request_update_hazards")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazards_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_hazards_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHazardsTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"hazard_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazards_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazards_attributes")
    pub.unsubscribe(dut.do_update, "request_update_hazards")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazards_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_hazards_attributes")

    # Delete the device under test.
    del dut
