# -*- coding: utf-8 -*-
#
#       tests.models.programdb.mission.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Mission module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMissionRecord
from ramstk.models.dbtables import RAMSTKMissionTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _mission_1 = RAMSTKMissionRecord()
    _mission_1.revision_id = 1
    _mission_1.mission_id = 1
    _mission_1.description = "Test mission #1"
    _mission_1.mission_time = 100.0
    _mission_1.time_units = "hours"

    _mission_2 = RAMSTKMissionRecord()
    _mission_2.revision_id = 1
    _mission_2.mission_id = 2
    _mission_2.description = "Test mission #2"
    _mission_2.mission_time = 24.0
    _mission_2.time_units = "hours"

    dao = MockDAO()
    dao.table = [
        _mission_1,
        _mission_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Mission attributes."""
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "description": "New mission",
        "mission_time": 24.0,
        "time_units": "hours",
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut
