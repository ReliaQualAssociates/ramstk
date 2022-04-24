# -*- coding: utf-8 -*-
#
#       tests.models.programdb.mechanism.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK failure Mechanism module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMechanismRecord
from ramstk.models.dbtables import RAMSTKMechanismTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _mechanism_1 = RAMSTKMechanismRecord()
    _mechanism_1.revision_id = 1
    _mechanism_1.hardware_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 1
    _mechanism_1.description = "Test Failure Mechanism #1"
    _mechanism_1.rpn = 100
    _mechanism_1.rpn_new = 100
    _mechanism_1.rpn_detection = 10
    _mechanism_1.rpn_detection_new = 10
    _mechanism_1.rpn_occurrence_new = 10
    _mechanism_1.rpn_occurrence = 10
    _mechanism_1.pof_include = 1

    _mechanism_2 = RAMSTKMechanismRecord()
    _mechanism_2.revision_id = 1
    _mechanism_2.hardware_id = 1
    _mechanism_2.mode_id = 6
    _mechanism_2.mechanism_id = 2
    _mechanism_2.description = "Test Failure Mechanism #2"
    _mechanism_2.rpn = 100
    _mechanism_2.rpn_new = 100
    _mechanism_2.rpn_detection = 10
    _mechanism_2.rpn_detection_new = 10
    _mechanism_2.rpn_occurrence_new = 10
    _mechanism_2.rpn_occurrence = 10
    _mechanism_2.pof_include = 1

    dao = MockDAO()
    dao.table = [
        _mechanism_1,
        _mechanism_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of failure Mechanism attributes."""
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "description": "",
        "pof_include": 1,
        "rpn": 0,
        "rpn_detection": 10,
        "rpn_detection_new": 10,
        "rpn_new": 0,
        "rpn_occurrence": 10,
        "rpn_occurrence_new": 10,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMechanismTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_mechanism_rpn")

    # Delete the device under test.
    del dut
