# -*- coding: utf-8 -*-
#
#       tests.models.commondb.failure_mode.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Mode module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureModeRecord
from ramstk.models.dbtables import RAMSTKFailureModeTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _failure_mode_1 = RAMSTKFailureModeRecord()
    _failure_mode_1.category_id = 1
    _failure_mode_1.subcategory_id = 1
    _failure_mode_1.mode_id = 1
    _failure_mode_1.description = "Short (pin-to-pin)"
    _failure_mode_1.mode_ratio = 0.65
    _failure_mode_1.source = "FMD-97"

    _failure_mode_2 = RAMSTKFailureModeRecord()
    _failure_mode_2.category_id = 1
    _failure_mode_2.subcategory_id = 1
    _failure_mode_2.mode_id = 2
    _failure_mode_2.description = "Open"
    _failure_mode_2.mode_ratio = 0.35
    _failure_mode_2.source = "FMD-97"

    dao = MockDAO()
    dao.table = [
        _failure_mode_1,
        _failure_mode_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Failure Mode attributes."""
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "mode_id": 1,
        "description": "Short (pin-to-pin)",
        "mode_ratio": 0.65,
        "source": "FMD-97",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFailureModeTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_failure_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_failure_mode_attributes")
    pub.unsubscribe(dut.do_update, "request_update_failure_mode")
    pub.unsubscribe(dut.do_get_tree, "request_get_failure_mode_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_failure_mode_attributes")

    # Delete the device under test.
    del dut
