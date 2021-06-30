# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.options.options_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOptions
from ramstk.models.commondb import RAMSTKSiteInfo


@pytest.fixture(scope="class")
def test_datamanager(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOptions()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"site_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_option_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_option_attributes")
    pub.unsubscribe(dut.do_update, "request_update_option")
    pub.unsubscribe(dut.do_get_tree, "request_get_options_tree")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["siteinfo"], RAMSTKSiteInfo)
        # There should be a root node with no data package and a node with
        # the one RAMSTKSiteInfo record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_siteinfo topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should clear nodes from an existing Options tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_siteinfo")

        test_datamanager.do_select_all({"site_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_siteinfo")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["siteinfo"].hardware_enabled == 0
        assert tree.get_node(1).data["siteinfo"].vandv_enabled == 0
        print("\033[36m\nsucceed_update_siteinfo topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for siteinfo ID 1 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_siteinfo topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_siteinfo topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent siteinfo with siteinfo ID "
            "skullduggery."
        )
        print("\033[35m\nfail_update_siteinfo topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for siteinfo ID 1.")
        print("\033[35m\nfail_update_siteinfo topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_siteinfo")

        test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled = 0
        test_datamanager.tree.get_node(1).data["siteinfo"].vandv_enabled = 0
        test_datamanager.do_update(1, table="siteinfo")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_siteinfo")

        assert test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled == 0
        assert test_datamanager.tree.get_node(1).data["siteinfo"].vandv_enabled == 0

        test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled = 1
        test_datamanager.tree.get_node(1).data["siteinfo"].vandv_enabled = 1
        test_datamanager.do_update(1, table="siteinfo")

        assert test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled == 1
        assert test_datamanager.tree.get_node(1).data["siteinfo"].vandv_enabled == 1

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_options")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_siteinfo")

        test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled = "Hi ya"
        test_datamanager.do_update(1, table="siteinfo")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_siteinfo")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_siteinfo"
        )

        test_datamanager.tree.get_node(1).data["siteinfo"].hardware_enabled = "Hey bud"
        test_datamanager.do_update(0, table="siteinfo")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_siteinfo"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_siteinfo")

        test_datamanager.do_select_all({"site_id": 1})
        test_datamanager.do_update("skullduggery", table="siteinfo")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_siteinfo")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_siteinfo")

        test_datamanager.tree.get_node(1).data.pop("siteinfo")
        test_datamanager.do_update(1, table="siteinfo")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_siteinfo")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_enabled"] == 1
        assert attributes["requirement_enabled"] == 1
        assert attributes["hardware_enabled"] == 1
        assert attributes["software_enabled"] == 0
        assert attributes["rcm_enabled"] == 0
        assert attributes["testing_enabled"] == 0
        assert attributes["incident_enabled"] == 0
        assert attributes["survival_enabled"] == 0
        assert attributes["vandv_enabled"] == 1
        assert attributes["hazard_enabled"] == 1
        assert attributes["stakeholder_enabled"] == 1
        assert attributes["allocation_enabled"] == 1
        assert attributes["similar_item_enabled"] == 1
        assert attributes["fmea_enabled"] == 1
        assert attributes["pof_enabled"] == 1
        assert attributes["rbd_enabled"] == 0
        print("\033[36m\nsucceed_get_siteinfo_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["siteinfo"], RAMSTKSiteInfo)
        print("\033[36m\nsucceed_get_options_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["siteinfo"].function_enabled == 1
        assert tree.get_node(1).data["siteinfo"].requirement_enabled == 1
        print("\033[36m\nsucceed_get_options_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of site information
        attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_siteinfo_attributes")

        pub.sendMessage("request_get_option_attributes", node_id=1, table="siteinfo")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_siteinfo_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_datamanager):
        """on_get_tree() should return the Options treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_options_tree")

        pub.sendMessage("request_get_options_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_options_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting
        site information attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_options_tree")

        pub.sendMessage(
            "request_set_option_attributes",
            node_id=[1, ""],
            package={"function_enabled": 1},
        )
        pub.sendMessage(
            "request_set_option_attributes",
            node_id=[1, ""],
            package={"requirement_enabled": 1},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_options_tree")
