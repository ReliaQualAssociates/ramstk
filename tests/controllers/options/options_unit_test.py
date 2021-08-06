# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.options.options_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO, MockRAMSTKSiteInfo
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOptions
from ramstk.db.base import BaseDatabase


@pytest.fixture
def mock_common_dao(monkeypatch):
    _site_1 = MockRAMSTKSiteInfo()
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

    DAO = MockDAO()
    DAO.table = [
        _site_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOptions()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_option_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_option_attributes")
    pub.unsubscribe(dut.do_update, "request_update_option")
    pub.unsubscribe(dut.do_get_tree, "request_get_option_tree")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, mock_common_dao):
        """__init__() should return a Options data manager."""
        DUT = dmOptions()

        assert isinstance(DUT, dmOptions)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._lst_id_columns == [
            "site_id",
        ]
        assert DUT._tag == "option"
        assert DUT._root == 0

        assert pub.isSubscribed(DUT.do_update, "request_update_option")
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_option_attributes")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_option_tree")
        assert pub.isSubscribed(DUT.do_set_attributes, "request_set_option_attributes")

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_option_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_option_attributes")
        pub.unsubscribe(DUT.do_update, "request_update_option")
        pub.unsubscribe(DUT.do_get_tree, "request_get_option_tree")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        test_datamanager.do_select_all({"site_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["option"], MockRAMSTKSiteInfo
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKSiteInfo record.
        assert len(test_datamanager.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKSiteInfo on success."""
        test_datamanager.do_select_all({"site_id": 1})

        _options = test_datamanager.do_select(1)

        assert isinstance(_options, MockRAMSTKSiteInfo)
        assert _options.site_id == 1
        assert _options.site_name == "DEMO SITE"
        assert _options.product_key == "DEMO"
        assert _options.expire_on == date.today() + timedelta(30)
        assert _options.function_enabled == 1
        assert _options.requirement_enabled == 1
        assert _options.hardware_enabled == 1
        assert _options.software_enabled == 0
        assert _options.rcm_enabled == 0
        assert _options.testing_enabled == 0
        assert _options.incident_enabled == 0
        assert _options.survival_enabled == 0
        assert _options.vandv_enabled == 1
        assert _options.hazard_enabled == 1
        assert _options.stakeholder_enabled == 1
        assert _options.allocation_enabled == 1
        assert _options.similar_item_enabled == 1
        assert _options.fmea_enabled == 1
        assert _options.pof_enabled == 1
        assert _options.rbd_enabled == 0
        assert _options.fta_enabled == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_datamanager.do_select_all({"site_id": 1})

        assert test_datamanager.do_select(100) is None
