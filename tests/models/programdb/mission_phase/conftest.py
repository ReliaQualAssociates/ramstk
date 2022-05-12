# -*- coding: utf-8 -*-
#
#       tests.models.programdb.mission_phase.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Mission Phase module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMissionPhaseRecord
from ramstk.models.dbtables import RAMSTKMissionPhaseTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _mission_phase_1 = RAMSTKMissionPhaseRecord()
    _mission_phase_1.revision_id = 1
    _mission_phase_1.mission_id = 1
    _mission_phase_1.mission_phase_id = 1
    _mission_phase_1.description = "Phase #1 for mission #1"
    _mission_phase_1.name = "Start Up"
    _mission_phase_1.phase_start = 0.0
    _mission_phase_1.phase_end = 0.0

    _mission_phase_2 = RAMSTKMissionPhaseRecord()
    _mission_phase_2.revision_id = 1
    _mission_phase_2.mission_id = 1
    _mission_phase_2.mission_phase_id = 2
    _mission_phase_2.description = "Phase #2 for mission #1"
    _mission_phase_2.name = "Operation"
    _mission_phase_2.phase_start = 0.0
    _mission_phase_2.phase_end = 0.0

    _mission_phase_3 = RAMSTKMissionPhaseRecord()
    _mission_phase_3.revision_id = 1
    _mission_phase_3.mission_id = 1
    _mission_phase_3.mission_phase_id = 3
    _mission_phase_3.description = "Phase #3 for mission #1"
    _mission_phase_3.name = "Shut Down"
    _mission_phase_3.phase_start = 0.0
    _mission_phase_3.phase_end = 0.0

    dao = MockDAO()
    dao.table = [
        _mission_phase_1,
        _mission_phase_2,
        _mission_phase_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Mission Phase attributes."""
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "mission_phase_id": 1,
        "description": "",
        "name": "",
        "phase_start": 0.0,
        "phase_end": 0.0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionPhaseTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut.do_insert, "request_insert_mission_phase")

    # Delete the device under test.
    del dut
