# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.function.function_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFunction
from ramstk.models.programdb import RAMSTKFunction


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFunction()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_function")
    pub.unsubscribe(dut.do_update, "request_update_function")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_function_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_function")
    pub.unsubscribe(dut._do_insert_function, "request_insert_function")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], RAMSTKFunction)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """should clear and then populate the record tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_functions")

        test_datamanager.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_functions")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["function"], RAMSTKFunction)
        assert tree.get_node(4).data["function"].function_id == 4
        assert tree.get_node(4).data["function"].name == "New Function"

        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_succeed_insert_child(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["function"], RAMSTKFunction)
        assert tree.get_node(5).data["function"].parent_id == 2
        assert tree.get_node(5).data["function"].function_id == 5
        assert tree.get_node(5).data["function"].name == "New Function"

        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "_do_insert_function: Attempted to insert "
            "child function under non-existent function ID 40."
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "_do_insert_function: A database error occurred when attempting to add a "
            "child function to parent function ID 1."
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_function")

        pub.sendMessage("request_insert_function", parent_id=0)
        assert test_datamanager.last_id == 4

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_function")

    @pytest.mark.integration
    def test_do_insert_child(self, test_datamanager):
        """should add a record under parent to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_child, "succeed_insert_function")

        pub.sendMessage("request_insert_function", parent_id=2)
        assert test_datamanager.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_child, "succeed_insert_function")

    @pytest.mark.integration
    def test_do_insert_no_parent(self):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_function")

        pub.sendMessage("request_insert_function", parent_id=40)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_function")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """should send the fail message when the revision ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_function")

        test_datamanager._revision_id = 40
        pub.sendMessage("request_insert_function", parent_id=1)
        test_datamanager._revision_id = 1

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_function")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_function topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Function ID 300.")
        print("\033[35m\nfail_delete_function topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Function ID 2.")
        print("\033[35m\nfail_delete_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove a record from the record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_function")

        _last_id = test_datamanager.last_id
        pub.sendMessage("request_delete_function", node_id=_last_id)

        assert test_datamanager.last_id == 2
        assert test_datamanager.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_function")

    @pytest.mark.integration
    def test_do_delete_with_child(self, test_datamanager):
        """should remove a record and children from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_function")

        pub.sendMessage("request_delete_function", node_id=1)

        assert test_datamanager.last_id == 0
        assert test_datamanager.tree.get_node(2) is None
        assert test_datamanager.tree.get_node(1) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_function")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when the function ID does not exist."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_function")

        pub.sendMessage("request_delete_function", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_function")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_function")

        pub.sendMessage("request_delete_function", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_function")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["function"].name == "Test Function"
        print("\033[36m\nsucceed_update_function topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more "
            "attributes for function ID 1 was the wrong "
            "type."
        )
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert (
            error_message == "do_update: Attempted to save non-existent function "
            "with function ID 100."
        )
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == "do_update: No data package found for function ID 1."
        print("\033[35m\nfail_update_function topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_function")

        test_datamanager.tree.get_node(1).data["function"].name = "Test Function"
        pub.sendMessage("request_update_function", node_id=1, table="function")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_function")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should update all the functions in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _function = test_datamanager.do_select(1, table="function")
        _function.name = "Big test function #1"
        _function = test_datamanager.do_select(2, table="function")
        _function.name = "Big test function #2"

        pub.sendMessage("request_update_all_functions")

        assert (
            test_datamanager.tree.get_node(1).data["function"].name
            == "Big test function #1"
        )
        assert (
            test_datamanager.tree.get_node(2).data["function"].name == "Big test "
            "function #2"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_function")

        test_datamanager.tree.get_node(1).data["function"].name = {1: 1.56}
        pub.sendMessage("request_update_function", node_id=1, table="function")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_function")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_function"
        )

        test_datamanager.tree.get_node(1).data["function"].name = {1: 1.56}
        pub.sendMessage("request_update_function", node_id=0, table="function")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_function"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a
        Function ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_function")

        pub.sendMessage("request_update_function", node_id=100, table="function")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_function")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_function")

        test_datamanager.tree.get_node(1).data.pop("function")
        pub.sendMessage("request_update_function", node_id=1, table="function")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_function")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_id"] == 1
        assert attributes["name"] == "Function Name"
        assert attributes["safety_critical"] == 0
        print("\033[36m\nsucceed_get_function_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], MockRAMSTKFunction)
        print("\033[36m\nsucceed_get_function_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["function"].function_code == "-"
        print("\033[36m\nsucceed_get_function_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return a dict of function attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_function_attributes")

        test_datamanager.do_get_attributes(node_id=1, table="function")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_function_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """on_get_tree() should return the function treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_function_tree"
        )

        pub.sendMessage("request_function_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_function_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_function_tree")

        pub.sendMessage(
            "request_set_function_attributes",
            node_id=[1],
            package={"function_code": "-"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_function_tree")
