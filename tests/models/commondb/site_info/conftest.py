# -*- coding: utf-8 -*-
#
#       tests.models.commondb.site_info.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Site Information module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSiteInfoRecord
from ramstk.models.dbtables import RAMSTKSiteInfoTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _site_1 = RAMSTKSiteInfoRecord()
    _site_1.site_id = 1
    _site_1.site_name = "DEMO SITE"
    _site_1.product_key = "DEMO"
    _site_1.expire_on = date.today() + timedelta(30)
    _site_1.function_enabled = 1
    _site_1.requirement_enabled = 1
    _site_1.hardware_enabled = 1
    _site_1.software_enabled = 0
    _site_1.rcm_enabled = 0
    _site_1.testing_enabled = 0
    _site_1.incident_enabled = 0
    _site_1.survival_enabled = 0
    _site_1.vandv_enabled = 1
    _site_1.hazard_enabled = 1
    _site_1.stakeholder_enabled = 1
    _site_1.allocation_enabled = 1
    _site_1.similar_item_enabled = 1
    _site_1.fmea_enabled = 1
    _site_1.pof_enabled = 1
    _site_1.rbd_enabled = 0
    _site_1.fta_enabled = 0

    _site_2 = RAMSTKSiteInfoRecord()
    _site_2.site_id = 2
    _site_2.site_name = "DEMO SITE 2"
    _site_2.product_key = "DEMO2"
    _site_2.expire_on = date.today() + timedelta(30)
    _site_2.function_enabled = 1
    _site_2.requirement_enabled = 1
    _site_2.hardware_enabled = 1
    _site_2.software_enabled = 0
    _site_2.rcm_enabled = 0
    _site_2.testing_enabled = 0
    _site_2.incident_enabled = 0
    _site_2.survival_enabled = 0
    _site_2.vandv_enabled = 1
    _site_2.hazard_enabled = 1
    _site_2.stakeholder_enabled = 1
    _site_2.allocation_enabled = 1
    _site_2.similar_item_enabled = 1
    _site_2.fmea_enabled = 1
    _site_2.pof_enabled = 1
    _site_2.rbd_enabled = 0
    _site_2.fta_enabled = 0

    dao = MockDAO()
    dao.table = [
        _site_1,
        _site_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Site Information attributes."""
    yield {
        "site_id": 1,
        "site_name": "",
        "product_key": "",
        "expire_on": date.today() + timedelta(30),
        "function_enabled": 0,
        "requirement_enabled": 0,
        "hardware_enabled": 0,
        "software_enabled": 0,
        "rcm_enabled": 0,
        "testing_enabled": 0,
        "incident_enabled": 0,
        "survival_enabled": 0,
        "vandv_enabled": 0,
        "hazard_enabled": 0,
        "stakeholder_enabled": 0,
        "allocation_enabled": 0,
        "similar_item_enabled": 0,
        "fmea_enabled": 0,
        "pof_enabled": 0,
        "rbd_enabled": 0,
        "fta_enabled": 0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSiteInfoTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_option_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_option_attributes")
    pub.unsubscribe(dut.do_update, "request_update_option")
    pub.unsubscribe(dut.do_get_tree, "request_get_option_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_option_attributes2")

    # Delete the device under test.
    del dut
