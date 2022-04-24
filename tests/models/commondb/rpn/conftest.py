# -*- coding: utf-8 -*-
#
#       tests.models.commondb.rpn.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK RPN module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRPNRecord
from ramstk.models.dbtables import RAMSTKRPNTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _rpn_1 = RAMSTKRPNRecord()
    _rpn_1.rpn_id = 1
    _rpn_1.rpn_type = "severity"
    _rpn_1.name = "Very Minor"
    _rpn_1.value = 1
    _rpn_1.description = "System operable with minimal interference."

    _rpn_2 = RAMSTKRPNRecord()
    _rpn_2.rpn_id = 2
    _rpn_2.rpn_type = "occurrence"
    _rpn_2.name = "Remote"
    _rpn_2.value = 1
    _rpn_2.description = "Failure rate is 1 in 1,500,000."

    _rpn_3 = RAMSTKRPNRecord()
    _rpn_3.rpn_id = 3
    _rpn_3.rpn_type = "detection"
    _rpn_3.name = "Almost Certain"
    _rpn_3.value = 1
    _rpn_3.description = (
        "Design control will almost certainly detect a potential "
        "mechanism/cause and subsequent failure mode."
    )

    dao = MockDAO()
    dao.table = [
        _rpn_1,
        _rpn_2,
        _rpn_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of RPN attributes."""
    yield {
        "rpn_id": 1,
        "rpn_type": "severity",
        "name": "Very Minor",
        "value": 1,
        "description": "System operable with minimal interference.",
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKRPNTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_rpn_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_rpn_attributes")
    pub.unsubscribe(dut.do_update, "request_update_rpn")
    pub.unsubscribe(dut.do_get_tree, "request_get_rpn_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_rpn_attributes")

    # Delete the device under test.
    del dut
