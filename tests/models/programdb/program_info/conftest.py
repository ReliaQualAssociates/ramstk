# -*- coding: utf-8 -*-
#
#       tests.models.programdb.program_info.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Program Information module test fixtures."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramInfoRecord
from ramstk.models.dbtables import RAMSTKProgramInfoTable
from tests import MockDAO


@pytest.fixture(scope="function")
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _program_1 = RAMSTKProgramInfoRecord()
    _program_1.revision_id = 1
    _program_1.function_active = 1
    _program_1.requirement_active = 1
    _program_1.hardware_active = 1
    _program_1.software_active = 0
    _program_1.rcm_active = 0
    _program_1.testing_active = 0
    _program_1.incident_active = 0
    _program_1.survival_active = 0
    _program_1.vandv_active = 1
    _program_1.hazard_active = 1
    _program_1.stakeholder_active = 1
    _program_1.allocation_active = 1
    _program_1.similar_item_active = 1
    _program_1.fmea_active = 1
    _program_1.pof_active = 1
    _program_1.rbd_active = 0
    _program_1.fta_active = 0
    _program_1.created_on = date.today()
    _program_1.created_by = ""
    _program_1.last_saved = date.today()
    _program_1.last_saved_by = ""

    _program_2 = RAMSTKProgramInfoRecord()
    _program_2.revision_id = 2
    _program_2.function_active = 1
    _program_2.requirement_active = 1
    _program_2.hardware_active = 1
    _program_2.software_active = 0
    _program_2.rcm_active = 0
    _program_2.testing_active = 0
    _program_2.incident_active = 0
    _program_2.survival_active = 0
    _program_2.vandv_active = 1
    _program_2.hazard_active = 1
    _program_2.stakeholder_active = 1
    _program_2.allocation_active = 1
    _program_2.similar_item_active = 1
    _program_2.fmea_active = 1
    _program_2.pof_active = 1
    _program_2.rbd_active = 0
    _program_2.fta_active = 0
    _program_2.created_on = date.today()
    _program_2.created_by = ""
    _program_2.last_saved = date.today()
    _program_2.last_saved_by = ""

    dao = MockDAO()
    dao.table = [
        _program_1,
        _program_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Program Information attributes."""
    yield {
        "revision_id": 1,
        "function_active": 1,
        "requirement_active": 1,
        "hardware_active": 1,
        "software_active": 0,
        "rcm_active": 0,
        "testing_active": 0,
        "incident_active": 0,
        "survival_active": 0,
        "vandv_active": 1,
        "hazard_active": 1,
        "stakeholder_active": 1,
        "allocation_active": 1,
        "similar_item_active": 1,
        "fmea_active": 1,
        "pof_active": 1,
        "rbd_active": 0,
        "fta_active": 0,
        "created_on": date.today(),
        "created_by": "",
        "last_saved": date.today(),
        "last_saved_by": "",
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramInfoTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_preference_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_preference_attributes")
    pub.unsubscribe(dut.do_update, "request_update_preference")
    pub.unsubscribe(dut.do_get_tree, "request_get_preference_tree")
    pub.unsubscribe(dut.do_select_all, "request_program_preferences")

    # Delete the device under test.
    del dut
