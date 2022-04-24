# -*- coding: utf-8 -*-
#
#       tests.models.programdb.requirement.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Requirement module test fixtures."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRequirementRecord
from ramstk.models.dbtables import RAMSTKRequirementTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _requirement_1 = RAMSTKRequirementRecord()
    _requirement_1.revision_id = 1
    _requirement_1.requirement_id = 1
    _requirement_1.derived = 0
    _requirement_1.description = ""
    _requirement_1.figure_number = ""
    _requirement_1.owner = 0
    _requirement_1.page_number = ""
    _requirement_1.parent_id = 0
    _requirement_1.priority = 0
    _requirement_1.requirement_code = "REL.1"
    _requirement_1.specification = ""
    _requirement_1.requirement_type = 0
    _requirement_1.validated = 0
    _requirement_1.validated_date = date.today()
    _requirement_1.q_clarity_0 = 0
    _requirement_1.q_clarity_1 = 0
    _requirement_1.q_clarity_2 = 0
    _requirement_1.q_clarity_3 = 0
    _requirement_1.q_clarity_4 = 0
    _requirement_1.q_clarity_5 = 0
    _requirement_1.q_clarity_6 = 0
    _requirement_1.q_clarity_7 = 0
    _requirement_1.q_clarity_8 = 0
    _requirement_1.q_complete_0 = 0
    _requirement_1.q_complete_1 = 0
    _requirement_1.q_complete_2 = 0
    _requirement_1.q_complete_3 = 0
    _requirement_1.q_complete_4 = 0
    _requirement_1.q_complete_5 = 0
    _requirement_1.q_complete_6 = 0
    _requirement_1.q_complete_7 = 0
    _requirement_1.q_complete_8 = 0
    _requirement_1.q_complete_9 = 0
    _requirement_1.q_consistent_0 = 0
    _requirement_1.q_consistent_1 = 0
    _requirement_1.q_consistent_2 = 0
    _requirement_1.q_consistent_3 = 0
    _requirement_1.q_consistent_4 = 0
    _requirement_1.q_consistent_5 = 0
    _requirement_1.q_consistent_6 = 0
    _requirement_1.q_consistent_7 = 0
    _requirement_1.q_consistent_8 = 0
    _requirement_1.q_verifiable_0 = 0
    _requirement_1.q_verifiable_1 = 0
    _requirement_1.q_verifiable_2 = 0
    _requirement_1.q_verifiable_3 = 0
    _requirement_1.q_verifiable_4 = 0
    _requirement_1.q_verifiable_5 = 0

    _requirement_2 = RAMSTKRequirementRecord()
    _requirement_2.revision_id = 1
    _requirement_2.requirement_id = 2
    _requirement_2.derived = 1
    _requirement_2.description = "Derived requirement #1 for base requirement #1."
    _requirement_2.figure_number = ""
    _requirement_2.owner = 0
    _requirement_2.page_number = ""
    _requirement_2.parent_id = 1
    _requirement_2.priority = 0
    _requirement_2.requirement_code = "REL.1.1"
    _requirement_2.specification = ""
    _requirement_2.requirement_type = 0
    _requirement_2.validated = 0
    _requirement_2.validated_date = date.today()
    _requirement_2.q_clarity_0 = 0
    _requirement_2.q_clarity_1 = 0
    _requirement_2.q_clarity_2 = 0
    _requirement_2.q_clarity_3 = 0
    _requirement_2.q_clarity_4 = 0
    _requirement_2.q_clarity_5 = 0
    _requirement_2.q_clarity_6 = 0
    _requirement_2.q_clarity_7 = 0
    _requirement_2.q_clarity_8 = 0
    _requirement_2.q_complete_0 = 0
    _requirement_2.q_complete_1 = 0
    _requirement_2.q_complete_2 = 0
    _requirement_2.q_complete_3 = 0
    _requirement_2.q_complete_4 = 0
    _requirement_2.q_complete_5 = 0
    _requirement_2.q_complete_6 = 0
    _requirement_2.q_complete_7 = 0
    _requirement_2.q_complete_8 = 0
    _requirement_2.q_complete_9 = 0
    _requirement_2.q_consistent_0 = 0
    _requirement_2.q_consistent_1 = 0
    _requirement_2.q_consistent_2 = 0
    _requirement_2.q_consistent_3 = 0
    _requirement_2.q_consistent_4 = 0
    _requirement_2.q_consistent_5 = 0
    _requirement_2.q_consistent_6 = 0
    _requirement_2.q_consistent_7 = 0
    _requirement_2.q_consistent_8 = 0
    _requirement_2.q_verifiable_0 = 0
    _requirement_2.q_verifiable_1 = 0
    _requirement_2.q_verifiable_2 = 0
    _requirement_2.q_verifiable_3 = 0
    _requirement_2.q_verifiable_4 = 0
    _requirement_2.q_verifiable_5 = 0

    dao = MockDAO()
    dao.table = [
        _requirement_1,
        _requirement_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Requirement attributes."""
    yield {
        "revision_id": 1,
        "requirement_id": 1,
        "derived": 0,
        "description": "New Requirement",
        "figure_number": "",
        "owner": 0,
        "page_number": "",
        "parent_id": 0,
        "priority": 0,
        "requirement_code": "",
        "specification": "",
        "requirement_type": 0,
        "validated": 0,
        "validated_date": date.today(),
        "q_clarity_0": 0,
        "q_clarity_1": 0,
        "q_clarity_2": 0,
        "q_clarity_3": 0,
        "q_clarity_4": 0,
        "q_clarity_5": 0,
        "q_clarity_6": 0,
        "q_clarity_7": 0,
        "q_clarity_8": 0,
        "q_complete_0": 0,
        "q_complete_1": 0,
        "q_complete_2": 0,
        "q_complete_3": 0,
        "q_complete_4": 0,
        "q_complete_5": 0,
        "q_complete_6": 0,
        "q_complete_7": 0,
        "q_complete_8": 0,
        "q_complete_9": 0,
        "q_consistent_0": 0,
        "q_consistent_1": 0,
        "q_consistent_2": 0,
        "q_consistent_3": 0,
        "q_consistent_4": 0,
        "q_consistent_5": 0,
        "q_consistent_6": 0,
        "q_consistent_7": 0,
        "q_consistent_8": 0,
        "q_verifiable_0": 0,
        "q_verifiable_1": 0,
        "q_verifiable_2": 0,
        "q_verifiable_3": 0,
        "q_verifiable_4": 0,
        "q_verifiable_5": 0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKRequirementTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_requirement")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_requirement")
    pub.unsubscribe(dut.do_update, "request_update_requirement")
    pub.unsubscribe(dut.do_create_all_codes, "request_create_all_requirement_codes")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_requirement_tree")
    pub.unsubscribe(dut.do_create_code, "request_create_requirement_code")
    pub.unsubscribe(dut.do_delete, "request_delete_requirement")
    pub.unsubscribe(dut.do_insert, "request_insert_requirement")

    # Delete the device under test.
    del dut
