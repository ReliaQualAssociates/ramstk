# -*- coding: utf-8 -*-
#
#       tests.models.programdb.environment.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Environment module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKEnvironmentRecord
from ramstk.models.dbtables import RAMSTKEnvironmentTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _environment_1 = RAMSTKEnvironmentRecord()
    _environment_1.revision_id = 1
    _environment_1.mission_id = 1
    _environment_1.mission_phase_id = 1
    _environment_1.environment_id = 1
    _environment_1.name = "Condition Name"
    _environment_1.units = "Units"
    _environment_1.minimum = 0.0
    _environment_1.maximum = 0.0
    _environment_1.mean = 0.0
    _environment_1.variance = 0.0
    _environment_1.ramp_rate = 0.0
    _environment_1.low_dwell_time = 0.0
    _environment_1.high_dwell_time = 0.0

    _environment_2 = RAMSTKEnvironmentRecord()
    _environment_2.revision_id = 1
    _environment_2.mission_id = 1
    _environment_2.mission_phase_id = 1
    _environment_2.environment_id = 2
    _environment_2.name = "Condition Name"
    _environment_2.units = "Units"
    _environment_2.minimum = 0.0
    _environment_2.maximum = 0.0
    _environment_2.mean = 0.0
    _environment_2.variance = 0.0
    _environment_2.ramp_rate = 0.0
    _environment_2.low_dwell_time = 0.0
    _environment_2.high_dwell_time = 0.0

    _environment_3 = RAMSTKEnvironmentRecord()
    _environment_3.revision_id = 1
    _environment_3.mission_id = 1
    _environment_3.mission_phase_id = 1
    _environment_3.environment_id = 3
    _environment_3.name = "Condition Name"
    _environment_3.units = "Units"
    _environment_3.minimum = 0.0
    _environment_3.maximum = 0.0
    _environment_3.mean = 0.0
    _environment_3.variance = 0.0
    _environment_3.ramp_rate = 0.0
    _environment_3.low_dwell_time = 0.0
    _environment_3.high_dwell_time = 0.0

    dao = MockDAO()
    dao.table = [
        _environment_1,
        _environment_2,
        _environment_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Environment attributes."""
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "mission_phase_id": 1,
        "environment_id": 1,
        "name": "Condition Name",
        "units": "Units",
        "minimum": 0.0,
        "maximum": 0.0,
        "mean": 0.0,
        "variance": 0.0,
        "ramp_rate": 0.0,
        "low_dwell_time": 0.0,
        "high_dwell_time": 0.0,
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKEnvironmentTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut
