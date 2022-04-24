# -*- coding: utf-8 -*-
#
#       tests.models.programdb.revision.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Revision module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRevisionRecord
from ramstk.models.dbtables import RAMSTKRevisionTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _revision_1 = RAMSTKRevisionRecord()
    _revision_1.revision_id = 1
    _revision_1.availability_logistics = 0.9986
    _revision_1.availability_mission = 0.99934
    _revision_1.cost = 12532.15
    _revision_1.cost_failure = 0.0000352
    _revision_1.cost_hour = 1.2532
    _revision_1.hazard_rate_active = 0.0
    _revision_1.hazard_rate_dormant = 0.0
    _revision_1.hazard_rate_logistics = 0.0
    _revision_1.hazard_rate_mission = 0.0
    _revision_1.hazard_rate_software = 0.0
    _revision_1.mmt = 0.0
    _revision_1.mcmt = 0.0
    _revision_1.mpmt = 0.0
    _revision_1.mtbf_logistics = 0.0
    _revision_1.mtbf_mission = 0.0
    _revision_1.mttr = 0.0
    _revision_1.name = "Original Revision"
    _revision_1.reliability_logistics = 0.99986
    _revision_1.reliability_mission = 0.99992
    _revision_1.remarks = "This is the original revision."
    _revision_1.revision_code = "Rev. -"
    _revision_1.program_time = 2562
    _revision_1.program_time_sd = 26.83
    _revision_1.program_cost = 26492.83
    _revision_1.program_cost_sd = 15.62

    _revision_2 = RAMSTKRevisionRecord()
    _revision_2.revision_id = 2
    _revision_2.availability_logistics = 1.0
    _revision_2.availability_mission = 1.0
    _revision_2.cost = 0.0
    _revision_2.cost_failure = 0.0
    _revision_2.cost_hour = 0.0
    _revision_2.hazard_rate_active = 0.0
    _revision_2.hazard_rate_dormant = 0.0
    _revision_2.hazard_rate_logistics = 0.0
    _revision_2.hazard_rate_mission = 0.0
    _revision_2.hazard_rate_software = 0.0
    _revision_2.mmt = 0.0
    _revision_2.mcmt = 0.0
    _revision_2.mpmt = 0.0
    _revision_2.mtbf_logistics = 0.0
    _revision_2.mtbf_mission = 0.0
    _revision_2.mttr = 0.0
    _revision_2.name = "Revision A"
    _revision_2.reliability_logistics = 1.0
    _revision_2.reliability_mission = 1.0
    _revision_2.remarks = "This is the second revision."
    _revision_2.revision_code = "Rev. A"
    _revision_2.program_time = 0
    _revision_2.program_time_sd = 0.0
    _revision_2.program_cost = 0.0
    _revision_2.program_cost_sd = 0.0

    dao = MockDAO()
    dao.table = [
        _revision_1,
        _revision_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Revision attributes."""
    yield {
        "revision_id": 1,
        "availability_logistics": 0.9986,
        "availability_mission": 0.99934,
        "cost": 12532.15,
        "cost_failure": 0.0000352,
        "cost_hour": 1.2532,
        "hazard_rate_active": 0.0,
        "hazard_rate_dormant": 0.0,
        "hazard_rate_logistics": 0.0,
        "hazard_rate_mission": 0.0,
        "hazard_rate_software": 0.0,
        "mmt": 0.0,
        "mcmt": 0.0,
        "mpmt": 0.0,
        "mtbf_logistics": 0.0,
        "mtbf_mission": 0.0,
        "mttr": 0.0,
        "name": "Original Revision",
        "reliability_logistics": 0.99986,
        "reliability_mission": 0.99992,
        "remarks": "This is the original revision.",
        "revision_code": "Rev. -",
        "program_time": 2562,
        "program_time_sd": 26.83,
        "program_cost": 26492.83,
        "program_cost_sd": 15.62,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Test fixture for Function data manager."""
    dut = RAMSTKRevisionTable()
    dut.do_connect(mock_dao)
    dut.do_select_all(
        attributes={
            None: None,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_revision")
    pub.unsubscribe(dut.do_update, "request_update_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_revision_tree")
    pub.unsubscribe(dut.do_select_all, "request_retrieve_revisions")
    pub.unsubscribe(dut.do_delete, "request_delete_revision")
    pub.unsubscribe(dut.do_insert, "request_insert_revision")

    # Delete the device under test.
    del dut
