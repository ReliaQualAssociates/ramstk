# -*- coding: utf-8 -*-
#
#       tests.models.commondb.manufacturer.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Manufacturer module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKManufacturerRecord
from ramstk.models.dbtables import RAMSTKManufacturerTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _manufacturer_1 = RAMSTKManufacturerRecord()
    _manufacturer_1.manufacturer_id = 1
    _manufacturer_1.cage_code = "47278"
    _manufacturer_1.description = "Eaton"
    _manufacturer_1.location = "Cleveland, OH"

    _manufacturer_2 = RAMSTKManufacturerRecord()
    _manufacturer_2.manufacturer_id = 2
    _manufacturer_2.cage_code = "A43D1"
    _manufacturer_2.description = "GE"
    _manufacturer_2.location = "Orlando, FL"

    dao = MockDAO()
    dao.table = [
        _manufacturer_1,
        _manufacturer_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Manufacturer attributes."""
    yield {
        "manufacturer_id": 1,
        "cage_code": "47278",
        "description": "Eaton",
        "location": "Cleveland, OH",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKManufacturerTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_manufacturer_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_manufacturer_attributes")
    pub.unsubscribe(dut.do_update, "request_update_manufacturer")
    pub.unsubscribe(dut.do_get_tree, "request_get_manufacturer_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_manufacturer_attributes")

    # Delete the device under test.
    del dut
