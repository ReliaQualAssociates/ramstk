# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.preferences.preferences_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Preferences integrations."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPreferences
from ramstk.models.programdb import RAMSTKProgramInfo


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmPreferences()
    dut._do_select_all(test_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_preference_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_preference_attributes")
    pub.unsubscribe(dut.do_update, "request_update_preference")
    pub.unsubscribe(dut.do_get_tree, "request_get_preference_tree")
    pub.unsubscribe(dut._do_select_all, "succeed_connect_program_database")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["preference"], RAMSTKProgramInfo)
        # There should be a root node with no data package and a node with
        # the one RAMSTKProgramInfo record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_preferences topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager, test_program_dao):
        """do_select_all() should clear nodes from an existing Options tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_preferences")

        pub.sendMessage("succeed_connect_program_database", dao=test_program_dao)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_preferences")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_preferences topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more "
            "attributes for Preferences 1 was the wrong "
            "type."
        )
        print("\033[35m\nfail_update_preferences topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_preferences topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent " "Program ID skullduggery."
        )
        print("\033[35m\nfail_update_preferences topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for " "Preference 1."
        )
        print("\033[35m\nfail_update_preferences topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_preferences")

        test_datamanager.tree.get_node(1).data["preference"].hardware_active = 0
        test_datamanager.tree.get_node(1).data["preference"].vandv_active = 0

        pub.sendMessage("request_update_preference", node_id=1, table="preference")

        assert test_datamanager.tree.get_node(1).data["preference"].hardware_active == 0
        assert test_datamanager.tree.get_node(1).data["preference"].vandv_active == 0

        pub.unsubscribe(self.on_succeed_update, "succeed_update_preferences")

        test_datamanager.tree.get_node(1).data["preference"].hardware_active = 1
        test_datamanager.tree.get_node(1).data["preference"].vandv_active = 1

        pub.sendMessage("request_update_preference", node_id=1, table="preference")

        assert test_datamanager.tree.get_node(1).data["preference"].hardware_active == 1
        assert test_datamanager.tree.get_node(1).data["preference"].vandv_active == 1

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_preferences")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_preferences")

        test_datamanager.tree.get_node(1).data["preference"].hardware_active = {0: 1}
        pub.sendMessage("request_update_preference", node_id=1, table="preference")

        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_preferences")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_preferences")

        test_datamanager.tree.get_node(1).data["preference"].hardware_active = {0: 1}

        pub.sendMessage("request_update_preference", node_id=1, table="preference")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_preferences")

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_preferences")

        pub.sendMessage(
            "request_update_preference", node_id="skullduggery", table="preference"
        )

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_preferences")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_preferences")

        test_datamanager.tree.get_node(1).data.pop("preference")

        pub.sendMessage("request_update_preference", node_id=1, table="preference")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_preferences")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_active"] == 1
        assert attributes["requirement_active"] == 1
        assert attributes["hardware_active"] == 1
        assert attributes["software_active"] == 0
        assert attributes["rcm_active"] == 0
        assert attributes["testing_active"] == 0
        assert attributes["incident_active"] == 0
        assert attributes["survival_active"] == 0
        assert attributes["vandv_active"] == 1
        assert attributes["hazard_active"] == 1
        assert attributes["stakeholder_active"] == 1
        assert attributes["allocation_active"] == 1
        assert attributes["similar_item_active"] == 1
        assert attributes["fmea_active"] == 1
        assert attributes["pof_active"] == 1
        assert attributes["rbd_active"] == 0
        assert attributes["fta_active"] == 0
        assert attributes["created_on"] == date.today()
        assert attributes["created_by"] == ""
        assert attributes["last_saved"] == date.today()
        assert attributes["last_saved_by"] == ""
        print("\033[36m\nsucceed_get_programinfo_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["preference"], RAMSTKProgramInfo)
        print("\033[36m\nsucceed_get_preferences_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["preference"].function_active == 0
        print("\033[36m\nsucceed_get_options_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of program information
        attributes on success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_programinfo_attributes"
        )

        pub.sendMessage(
            "request_get_preference_attributes", node_id=1, table="preference"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_programinfo_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_datamanager):
        """on_get_tree() should return the Preferences treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_preferences_tree"
        )

        pub.sendMessage("request_get_preference_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_preferences_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting
        program information attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_preferences_tree")

        pub.sendMessage(
            "request_set_preference_attributes",
            node_id=[1],
            package={"function_active": 0},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_preferences_tree")

        pub.sendMessage(
            "request_set_preference_attributes",
            node_id=[1],
            package={"function_active": 1},
        )
        assert test_datamanager.do_select(1, table="preference").function_active == 1
