# -*- coding: utf-8 -*-
#
#       tests.models.programdb.stakeholder.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Stakeholder module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholderRecord
from ramstk.models.dbtables import RAMSTKStakeholderTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _stakeholder_1 = RAMSTKStakeholderRecord()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = "Stakeholder Input"
    _stakeholder_1.group = ""
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ""
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    _stakeholder_2 = RAMSTKStakeholderRecord()
    _stakeholder_2.revision_id = 1
    _stakeholder_2.requirement_id = 1
    _stakeholder_2.stakeholder_id = 2
    _stakeholder_2.customer_rank = 1
    _stakeholder_2.description = "Stakeholder Input"
    _stakeholder_2.group = ""
    _stakeholder_2.improvement = 0.0
    _stakeholder_2.overall_weight = 0.0
    _stakeholder_2.planned_rank = 1
    _stakeholder_2.priority = 1
    _stakeholder_2.stakeholder = ""
    _stakeholder_2.user_float_1 = 1.0
    _stakeholder_2.user_float_2 = 1.0
    _stakeholder_2.user_float_3 = 1.0
    _stakeholder_2.user_float_4 = 1.0
    _stakeholder_2.user_float_5 = 1.0

    dao = MockDAO()
    dao.table = [
        _stakeholder_1,
        _stakeholder_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Stakeholder attributes."""
    yield {
        "revision_id": 1,
        "stakeholder_id": 1,
        "customer_rank": 1,
        "description": "Stakeholder Input",
        "group": "",
        "improvement": 0.0,
        "overall_weight": 0.0,
        "planned_rank": 1,
        "priority": 1,
        "requirement_id": 0,
        "stakeholder": "",
        "user_float_1": 1.0,
        "user_float_2": 1.0,
        "user_float_3": 1.0,
        "user_float_4": 1.0,
        "user_float_5": 1.0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStakeholderTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholder")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut.do_insert, "request_insert_stakeholder")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut
