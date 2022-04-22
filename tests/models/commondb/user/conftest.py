# -*- coding: utf-8 -*-
#
#       tests.models.commondb.user.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK User module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKUserRecord
from ramstk.models.dbtables import RAMSTKUserTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _user_1 = RAMSTKUserRecord()
    _user_1.user_id = 1
    _user_1.user_lname = "Sweetheart"
    _user_1.user_fname = "Monica"
    _user_1.user_email = "monica.sweetheart@myclub.com"
    _user_1.user_phone = "269-867-5309"
    _user_1.user_group_id = "10"

    _user_2 = RAMSTKUserRecord()
    _user_2.user_id = 2
    _user_2.user_lname = "Janson"
    _user_2.user_fname = "Jillian"
    _user_2.user_email = "jillian.janson@myclub.com"
    _user_2.user_phone = "269-867-5310"
    _user_2.user_group_id = "8"

    dao = MockDAO()
    dao.table = [
        _user_1,
        _user_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of User attributes."""
    yield {
        "user_id": 1,
        "user_lname": "Sweetheart",
        "user_fname": "Monica",
        "user_email": "monica.sweetheart@myclub.com",
        "user_phone": "269-867-5309",
        "user_group_id": "10",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKUserTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_user_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_user_attributes")
    pub.unsubscribe(dut.do_update, "request_update_user")
    pub.unsubscribe(dut.do_get_tree, "request_get_user_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_user_attributes")

    # Delete the device under test.
    del dut
