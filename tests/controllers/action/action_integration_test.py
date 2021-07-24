# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.action.action_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmAction
from ramstk.models.programdb import RAMSTKAction


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmAction()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        {
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_cause")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_action")
    pub.unsubscribe(dut._do_insert_action, "request_insert_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["action"], RAMSTKAction)
        assert isinstance(tree.get_node(4).data["action"], RAMSTKAction)
        print("\033[36m\nsucceed_retrieve_action topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """should return a Tree() object populated with RAMSTKAction instances."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_action")

        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_action")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["action"], RAMSTKAction)
        print("\033[36m\nsucceed_insert_action topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_cause_id)=(100) is not present in table "
            '"ramstk_cause".'
        )
        print("\033[35m\nfail_insert_action topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_action")

        pub.sendMessage("request_insert_action")

        assert test_datamanager.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_action")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """should send the fail message if the parent ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_action")

        _parent_id = test_datamanager._parent_id
        test_datamanager._parent_id = 100
        pub.sendMessage("request_insert_action")
        test_datamanager._parent_id = _parent_id

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_action")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_action topic was broadcast")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Action ID 300."
        )
        print("\033[35m\nfail_delete_action topic was broadcast")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Action ID 4."
        )
        print("\033[35m\nfail_delete_action topic was broadcast")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove the deleted record from records tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_action")

        pub.sendMessage("request_delete_action", node_id=3)

        assert test_datamanager.last_id == 4

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_action")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when node ID doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_action")

        pub.sendMessage("request_delete_action", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_action")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """should send the fail message when node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_action")

        test_datamanager.tree.remove_node(4)
        pub.sendMessage("request_delete_action", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_action")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["action"].action_recommended == ("Get a clue.")
        assert tree.get_node(3).data["action"].action_closed == 1
        print("\033[36m\nsucceed_update_action topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for action ID 3 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_action topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent action with action ID 100."
        )
        print("\033[35m\nfail_update_action topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for action ID 3.")
        print("\033[35m\nfail_update_action topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """should update record in database and records tree."""
        pub.subscribe(self.on_succeed_update, "succeed_update_action")

        test_datamanager.tree.get_node(3).data[
            "action"
        ].action_recommended = "Get a clue."
        test_datamanager.tree.get_node(3).data["action"].action_closed = 1
        pub.sendMessage("request_update_action", node_id=3, table="action")

        assert (
            test_datamanager.tree.get_node(3).data["action"].action_recommended
            == "Get a clue."
        )
        assert test_datamanager.tree.get_node(3).data["action"].action_closed == 1

        pub.unsubscribe(self.on_succeed_update, "succeed_update_action")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """should update all records in database and records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_datamanager.tree.get_node(3).data[
            "action"
        ].description = "Test failure action"
        test_datamanager.tree.get_node(3).data["action"].rpn_detection = 2
        test_datamanager.tree.get_node(4).data[
            "action"
        ].description = "Big test failure action"
        test_datamanager.tree.get_node(4).data["action"].rpn_detection = 7
        pub.sendMessage("request_update_all_actions")

        assert (
            test_datamanager.tree.get_node(3).data["action"].description
            == "Test failure action"
        )
        assert test_datamanager.tree.get_node(3).data["action"].rpn_detection == 2
        assert (
            test_datamanager.tree.get_node(4).data["action"].description
            == "Big test failure action"
        )
        assert test_datamanager.tree.get_node(4).data["action"].rpn_detection == 7

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """should send fail message if attribute has wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_action")

        _action = test_datamanager.do_select(3, table="action")
        _action.action_approved = {1: 2}
        pub.sendMessage("request_update_action", node_id=3, table="action")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_action")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """should send fail message when attempting to update root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_action"
        )

        _action = test_datamanager.do_select(4, table="action")
        _action.action_closed = {1: 2}
        pub.sendMessage("request_update_action", node_id=0, table="action")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_action"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send fail message when node ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_action")

        pub.sendMessage("request_update_action", node_id=100, table="action")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_action")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """should send fail message when node ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_action")

        test_datamanager.tree.get_node(3).data.pop("action")
        pub.sendMessage("request_update_action", node_id=3, table="action")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_action")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["action_id"] == 3
        assert (
            attributes["action_recommended"]
            == "Test FMEA Recommended Action #1 for Cause ID 3"
        )
        print("\033[36m\nsucceed_get_action_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["action"], RAMSTKAction)
        assert isinstance(tree.get_node(4).data["action"], RAMSTKAction)
        print("\033[36m\nsucceed_get_action_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(4).data["action"].action_owner
            == "John Jacob Jingleheimer Schmidt"
        )
        print("\033[36m\nsucceed_get_action_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """should return a dict of attribute key:value pairs."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_action_attributes")

        test_datamanager.do_get_attributes(node_id=3, table="action")

        assert (
            test_datamanager.tree.get_node(3).data["action"].action_recommended
            == "Test FMEA Recommended Action #1 for Cause ID 3"
        )

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_action_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the data manager records tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_action_tree")

        pub.sendMessage("request_get_action_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_action_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """should set the value of the requested attribute."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_action_tree")

        pub.sendMessage(
            "request_set_action_attributes",
            node_id=[4],
            package={"action_owner": "John Jacob Jingleheimer Schmidt"},
        )

        assert (
            test_datamanager.do_select(4, table="action").action_owner
            == "John Jacob Jingleheimer Schmidt"
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_action_tree")
