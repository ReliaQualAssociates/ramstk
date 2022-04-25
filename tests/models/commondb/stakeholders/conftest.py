# -*- coding: utf-8 -*-
#
#       tests.models.commondb.stakeholders.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Stakeholders module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholdersRecord
from ramstk.models.dbtables import RAMSTKStakeholdersTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _stakeholders_1 = RAMSTKStakeholdersRecord()
    _stakeholders_1.stakeholders_id = 1
    _stakeholders_1.stakeholder = "Customer"

    _stakeholders_2 = RAMSTKStakeholdersRecord()
    _stakeholders_2.stakeholders_id = 2
    _stakeholders_2.stakeholder = "Regulator"

    dao = MockDAO()
    dao.table = [
        _stakeholders_1,
        _stakeholders_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Stakeholders attributes."""
    yield {
        "stakeholders_id": 1,
        "stakeholder": "Customer",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStakeholdersTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholders_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholders_attributes")
    pub.unsubscribe(dut.do_update, "request_update_stakeholders")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholders_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_stakeholders_attributes")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_table_model(test_common_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStakeholdersTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"stakeholders_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholders_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholders_attributes")
    pub.unsubscribe(dut.do_update, "request_update_stakeholders")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholders_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_stakeholders_attributes")

    # Delete the device under test.
    del dut
