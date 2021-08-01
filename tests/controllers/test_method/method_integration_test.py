# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_method.method_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Test Method integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmTestMethod
from ramstk.models.programdb import RAMSTKTestMethod


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmTestMethod()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "load_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_load")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_test_method")
    pub.unsubscribe(dut._do_insert_test_method, "request_insert_test_method")

    # Delete the device under test.
    del dut


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_retrieve_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self):
        """do_select_all() should return a Tree() object populated with
        RAMSTKTestMethod instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")

        pub.sendMessage(
            "selected_load",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            },
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_insert_test_method topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_load_id)=(100) is not present in table "
            '"ramstk_op_load".'
        )
        print("\033[35m\nfail_insert_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self):
        """_do_insert_test_method() should send the success message after successfully
        inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_test_method")

        pub.sendMessage("request_insert_test_method", parent_id=3)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_test_method")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_test_method() should send the fail message if attempting to add
        an operating load to a non-existent test_method ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_test_method")

        test_datamanager._parent_id = 100
        pub.sendMessage("request_insert_test_method", parent_id=100)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_test_method")


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1) is None
        print("\033[36m\nsucceed_delete_test_method topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Test Method ID 300.")
        print("\033[35m\nfail_delete_test_method topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Test Method ID 4.")
        print("\033[35m\nfail_delete_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_test_method")

        pub.sendMessage("request_delete_test_method", node_id=3)

        assert test_datamanager.last_id == 4

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_test_method")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """_do_delete() should send the fail message when attempting to delete a node
        ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_test_method")

        pub.sendMessage("request_delete_test_method", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_test_method")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_test_method")

        test_datamanager.tree.remove_node(4)
        pub.sendMessage("request_delete_test_method", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_test_method")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["test_method"].description == (
            "Big test test_method."
        )
        assert tree.get_node(3).data["test_method"].boundary_conditions == (
            "Big test boundary conditions."
        )
        print("\033[36m\nsucceed_update_test_method topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for test method ID 3 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_test_method topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent test method with test method "
            "ID 100."
        )
        print("\033[35m\nfail_update_test_method topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for test method ID 4."
        )
        print("\033[35m\nfail_update_test_method topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_test_method")

        test_datamanager.tree.get_node(3).data[
            "test_method"
        ].description = "Big test test_method."
        test_datamanager.tree.get_node(3).data[
            "test_method"
        ].boundary_conditions = "Big test boundary conditions."
        pub.sendMessage("request_update_test_method", node_id=3, table="test_method")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_test_method")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_test_methods")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_test_method")

        _test_method = test_datamanager.do_select(3, table="test_method")
        _test_method.boundary_conditions = {1: 2}

        pub.sendMessage("request_update_test_method", node_id=3, table="test_method")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_test_method")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed the root node
        ID."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_test_method"
        )

        _test_method = test_datamanager.do_select(4, table="test_method")
        _test_method.boundary_conditions = {1: 2}

        pub.sendMessage("request_update_test_method", node_id=0, table="test_method")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_test_method"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a Test Method ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_test_method")

        pub.sendMessage("request_update_test_method", node_id=100, table="test_method")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_test_method")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a FMEA ID that
        has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_test_method")

        test_datamanager.tree.get_node(4).data.pop("test_method")
        pub.sendMessage("request_update_test_method", node_id=4, table="test_method")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_test_method")


class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["load_id"] == 1
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(2).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_get_test_method_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["test_method"].boundary_conditions
            == "Big test boundary condition."
        )
        print("\033[36m\nsucceed_get_test_method_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """do_get_attributes() should return a dict of mode attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        pub.sendMessage(
            "request_get_test_method_attributes", node_id=1, table="test_method"
        )

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_test_method_tree"
        )

        pub.sendMessage("request_get_test_method_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_test_method_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should return None when successfully setting operating
        load attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_test_method_tree")

        pub.sendMessage(
            "request_set_test_method_attributes",
            node_id=[1],
            package={"boundary_conditions": "Big test boundary condition."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_test_method_tree")
