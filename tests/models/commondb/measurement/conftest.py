# -*- coding: utf-8 -*-
#
#       tests.models.commondb.measurement.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Measurement module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMeasurementRecord
from ramstk.models.dbtables import RAMSTKMeasurementTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _measurement_1 = RAMSTKMeasurementRecord()
    _measurement_1.measurement_id = 1
    _measurement_1.measurement_type = "unit"
    _measurement_1.code = "CBT"
    _measurement_1.description = "Cubic Butt Ton"

    _measurement_2 = RAMSTKMeasurementRecord()
    _measurement_2.measurement_id = 2
    _measurement_2.measurement_type = "unit"
    _measurement_2.code = "A"
    _measurement_2.description = "Amperes"

    dao = MockDAO()
    dao.table = [
        _measurement_1,
        _measurement_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Measurement attributes."""
    yield {
        "measurement_id": 1,
        "code": "CBT",
        "description": "Cubic Butt Ton",
        "measurement_type": "unit",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMeasurementTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_measurement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_measurement_attributes")
    pub.unsubscribe(dut.do_update, "request_update_measurement")
    pub.unsubscribe(dut.do_get_tree, "request_get_measurement_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_measurement_attributes")

    # Delete the device under test.
    del dut
