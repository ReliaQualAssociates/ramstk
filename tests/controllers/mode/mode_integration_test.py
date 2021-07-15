# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mode.mode_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure mode integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMode
from ramstk.models.programdb import RAMSTKMode


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMode()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mode")
    pub.unsubscribe(dut._do_insert_mode, "request_insert_mode")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["mode"], RAMSTKMode)
        print("\033[36m\nsucceed_retrieve_mode topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should clear out an existing tree and build a new
        one when called on a populated Mission Phase data manager."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_modes")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_modes")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 7
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(7).data["mode"], RAMSTKMode)
        assert tree.get_node(7).data["mode"].mode_id == 7
        assert tree.get_node(7).data["mode"].description == ""
        print("\033[36m\nsucceed_insert_mode topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(100) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_mode topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey (fld_revision_id, "
            "fld_hardware_id)=(4, 100) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_mode topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_datamanager):
        """do_insert() should send the success message with the ID of the newly
        inserted node and the data manager's tree after successfully inserting
        a new mode."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mode")

        pub.sendMessage("request_insert_mode")

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mode")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_mechanism() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_mode")

        _parent_id = test_datamanager._parent_id
        test_datamanager._parent_id = 100
        pub.sendMessage("request_insert_mode")
        test_datamanager._parent_id = _parent_id

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_mode")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_mode() should send the fail message if attempting to add
        a mode to a non-existent Revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_mode")

        test_datamanager._revision_id = 4
        pub.sendMessage("request_insert_mode")

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_mode")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4) is None
        print("\033[36m\nsucceed_delete_mode topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 300."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 5."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mode")

        test_datamanager._do_delete(4)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mode")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

        test_datamanager._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")

        test_datamanager.tree.remove_node(5)
        test_datamanager._do_delete(5)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["mode"].description == ("Test failure mode")
        assert tree.get_node(4).data["mode"].operator_actions == (
            "Take evasive actions."
        )
        print("\033[36m\nsucceed_update_mode topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for mode ID 4 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_mode topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_mode topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mode with mode ID 100."
        )
        print("\033[35m\nfail_update_mode topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mode ID 4.")
        print("\033[35m\nfail_update_mode topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mode")

        test_datamanager.tree.get_node(4).data["mode"].description = "Test failure mode"
        test_datamanager.tree.get_node(4).data[
            "mode"
        ].operator_actions = "Take evasive actions."

        pub.sendMessage("request_update_mode", node_id=4, table="mode")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mode")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_modes")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        mode ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

        _mode = test_datamanager.do_select(4, table="mode")
        _mode.mode_criticality = {1: 2}

        pub.sendMessage("request_update_mode", node_id=4, table="mode")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        mode ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "fail_update_mode")

        _mode = test_datamanager.do_select(4, table="mode")
        _mode.mode_criticality = {1: 2}

        pub.sendMessage("request_update_mode", node_id=0, table="mode")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_mode"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a mode ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mode")

        pub.sendMessage("request_update_mode", node_id=100, table="mode")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mode")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a mode ID that
        has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mode")

        test_datamanager.tree.get_node(4).data.pop("mode")
        pub.sendMessage("request_update_mode", node_id=4, table="mode")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mode")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mode_id"] == 2
        assert attributes["description"] == "Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["mode"], RAMSTKMode)
        assert isinstance(tree.get_node(5).data["mode"], RAMSTKMode)
        assert isinstance(tree.get_node(6).data["mode"], RAMSTKMode)
        print("\033[36m\nsucceed_get_mode_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["mode"].description == "Jared Kushner"
        print("\033[36m\nsucceed_get_mode_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        pub.sendMessage("request_get_mode_attributes", node_id=2, table="mode")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_datamanager):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mode_tree")

        pub.sendMessage("request_get_mode_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mode_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_mode_tree")

        pub.sendMessage(
            "request_set_mode_attributes",
            node_id=[4, ""],
            package={"description": "Jared Kushner"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_mode_tree")
