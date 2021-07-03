# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.preferences.preferences_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Preferences module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKProgramInfo
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPreferences
from ramstk.db.base import BaseDatabase


@pytest.fixture(scope="function")
def mock_program_dao(monkeypatch):
    _program_1 = MockRAMSTKProgramInfo()
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

    DAO = MockDAO()
    DAO.table = [
        _program_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmPreferences()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_preference_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_preference_attributes")
    pub.unsubscribe(dut.do_update, "request_update_preference")
    pub.unsubscribe(dut.do_get_tree, "request_get_preferences_tree")
    pub.unsubscribe(dut._do_select_all, "succeed_connect_program_database")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Options data manager."""
        DUT = dmPreferences()

        assert isinstance(DUT, dmPreferences)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._pkey == {
            "programinfo": ["revision_id"],
        }
        assert DUT._tag == "preferences"
        assert DUT._root == 0

        assert pub.isSubscribed(DUT._do_select_all, "succeed_connect_program_database")
        assert pub.isSubscribed(DUT.do_update, "request_update_preference")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_preference_attributes"
        )
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_preferences_tree")
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_preference_attributes"
        )

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_preference_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_preference_attributes")
        pub.unsubscribe(DUT.do_update, "request_update_preference")
        pub.unsubscribe(DUT.do_get_tree, "request_get_preferences_tree")
        pub.unsubscribe(DUT._do_select_all, "succeed_connect_program_database")


@pytest.mark.usefixtures("mock_program_dao", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)

        print("\033[36m\nsucceed_retrieve_preferences topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        test_datamanager._do_select_all(mock_program_dao)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["programinfo"], MockRAMSTKProgramInfo
        )

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao, test_datamanager):
        """do_select() should return an instance of the RAMSTKProgramInfo on
        success."""
        test_datamanager._do_select_all(mock_program_dao)

        _preferences = test_datamanager.do_select(1, table="programinfo")

        assert isinstance(_preferences, MockRAMSTKProgramInfo)
        assert _preferences.function_active == 1
        assert _preferences.requirement_active == 1
        assert _preferences.hardware_active == 1
        assert _preferences.software_active == 0
        assert _preferences.rcm_active == 0
        assert _preferences.testing_active == 0
        assert _preferences.incident_active == 0
        assert _preferences.survival_active == 0
        assert _preferences.vandv_active == 1
        assert _preferences.hazard_active == 1
        assert _preferences.stakeholder_active == 1
        assert _preferences.allocation_active == 1
        assert _preferences.similar_item_active == 1
        assert _preferences.fmea_active == 1
        assert _preferences.pof_active == 1
        assert _preferences.rbd_active == 0
        assert _preferences.fta_active == 0
        assert _preferences.created_on == date.today()
        assert _preferences.created_by == ""
        assert _preferences.last_saved == date.today()
        assert _preferences.last_saved_by == ""

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager._do_select_all(mock_program_dao)

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao, test_datamanager):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_datamanager._do_select_all(mock_program_dao)

        assert test_datamanager.do_select(100, table="programinfo") is None
