# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.group.group_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Group module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKGroupRecord, RAMSTKGroupTable


@pytest.fixture(scope="class")
def test_tablemodel(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKGroupTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"group_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_group_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_group_attributes")
    pub.unsubscribe(dut.do_update, "request_update_group")
    pub.unsubscribe(dut.do_get_tree, "request_get_group_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_group_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["group"], RAMSTKGroupRecord)
        # There should be a root node with no data package and a node with
        # the one RAMSTKGroupRecord record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_group topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_tablemodel):
        """do_select_all() should clear nodes from an existing Group tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_group")

        test_tablemodel.do_select_all({"group_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_group")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["group"].description == "New Group"
        assert tree.get_node(1).data["group"].group_type == "swinger"
        print("\033[36m\nsucceed_update_group topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for group ID 1 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_group topic was broadcast on wrong type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_group topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent group with group ID "
            "skullduggery."
        )
        print("\033[35m\nfail_update_group topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for group ID 1.")
        print("\033[35m\nfail_update_group topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_group")

        test_tablemodel.tree.get_node(1).data["group"].description = "New Group"
        test_tablemodel.tree.get_node(1).data["group"].group_type = "swinger"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_group")

        assert test_tablemodel.tree.get_node(1).data["group"].description == "New Group"
        assert test_tablemodel.tree.get_node(1).data["group"].group_type == "swinger"

        test_tablemodel.tree.get_node(1).data["group"].description = "Engineering, RMS"
        test_tablemodel.tree.get_node(1).data["group"].group_type = "work"
        test_tablemodel.do_update(1)

        assert (
            test_tablemodel.tree.get_node(1).data["group"].description
            == "Engineering, RMS"
        )
        assert test_tablemodel.tree.get_node(1).data["group"].group_type == "work"

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_group")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_group")

        test_tablemodel.tree.get_node(1).data["group"].group_type = None
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_group")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_group"
        )

        test_tablemodel.tree.get_node(1).data["group"].group_type = None
        test_tablemodel.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_group"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Group ID that
        doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_group")

        test_tablemodel.do_select_all({"group_id": 1})
        test_tablemodel.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_group")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Group ID that
        doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_group")

        test_tablemodel.tree.get_node(1).data.pop("group")
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_group")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert _attributes["group_id"] == 1
        assert _attributes["group_type"] == "work"
        assert _attributes["description"] == "Engineering, RMS"
        print("\033[36m\nsucceed_get_group_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["group"], RAMSTKGroupRecord)
        print("\033[36m\nsucceed_get_group_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["group"].description == "Party"
        assert tree.get_node(1).data["group"].group_type == "swinger"
        print("\033[36m\nsucceed_get_group_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of site information attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_group_attributes")

        pub.sendMessage("request_get_group_attributes2", attributes={"group_id": 1})

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_group_attributes")

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """on_get_tree() should return the Group treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_group_tree")

        pub.sendMessage("request_get_group_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_group_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting site
        information attributes."""

        pub.sendMessage(
            "request_set_group_attributes",
            node_id=1,
            package={"description": "Party"},
        )

        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_group_tree")

        pub.sendMessage(
            "request_set_group_attributes",
            node_id=1,
            package={"group_type": "swinger"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_group_tree")
