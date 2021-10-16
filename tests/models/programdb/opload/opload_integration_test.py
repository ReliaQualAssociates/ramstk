# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opload.opload_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing operating load integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKOpLoadRecord, RAMSTKOpLoadTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpLoadTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 4,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["opload"], RAMSTKOpLoadRecord)
        print("\033[36m\nsucceed_retrieve_opload topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoadRecord instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_opload")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["opload"], RAMSTKOpLoadRecord)
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_mechanism_id)=(30) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message with the ID of the newly
        inserted node and the data manager's tree after successfully inserting a new
        opload."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")

        assert test_tablemodel.tree.get_node(5) is None

        pub.sendMessage("request_insert_opload", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(5).data["opload"], RAMSTKOpLoadRecord
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_tablemodel):
        """_do_insert_opload() should send the fail message if attempting to add an
        operating load to a non-existent opload ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_opload")

        assert test_tablemodel.tree.get_node(6) is None

        test_attributes["mechanism_id"] = 30
        pub.sendMessage("request_insert_opload", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(6) is None

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_opload")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_opload topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Opload ID 300.")
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Opload ID 4.")
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_opload")

        pub.sendMessage("request_delete_opload", node_id=3)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_opload")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """_do_delete() should send the fail message when attempting to delete a node
        ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

        pub.sendMessage("request_delete_opload", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")

        test_tablemodel.tree.remove_node(4)
        pub.sendMessage("request_delete_opload", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["opload"].description == ("Test failure opload")
        assert tree.get_node(4).data["opload"].priority_id == 4
        print("\033[36m\nsucceed_update_opload topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for opload ID 4 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_opload topic was broadcast on wrong data type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_opload topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent opload with opload ID 100."
        )
        print("\033[35m\nfail_update_opload topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for opload ID 4.")
        print("\033[35m\nfail_update_opload topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_opload")

        test_tablemodel.tree.get_node(4).data[
            "opload"
        ].description = "Test failure opload"
        test_tablemodel.tree.get_node(4).data["opload"].priority_id = 4

        pub.sendMessage("request_update_opload", node_id=4, table="opload")

        assert (
            test_tablemodel.tree.get_node(4).data["opload"].description
            == "Test failure opload"
        )
        assert test_tablemodel.tree.get_node(4).data["opload"].priority_id == 4

        pub.unsubscribe(self.on_succeed_update, "succeed_update_opload")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_oploads")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

        _opload = test_tablemodel.do_select(4)
        _opload.priority_id = {1: 2}

        pub.sendMessage("request_update_opload", node_id=4, table="opload")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opload"
        )

        _opload = test_tablemodel.do_select(4)
        _opload.priority_id = {1: 2}

        pub.sendMessage("request_update_opload", node_id=0, table="opload")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opload"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed an OpLoad ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

        pub.sendMessage("request_update_opload", node_id=100, table="opload")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a FMEA ID that
        has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_opload")

        test_tablemodel.tree.get_node(4).data.pop("opload")
        pub.sendMessage("request_update_opload", node_id=4, table="opload")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_opload")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["load_id"] == 1
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["opload"], RAMSTKOpLoadRecord)
        print("\033[36m\nsucceed_get_opload_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["opload"].description == "Jared Kushner"
        print("\033[36m\nsucceed_get_opload_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of mode attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        pub.sendMessage("request_get_opload_attributes", node_id=4, table="opload")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_tablemodel):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree")

        pub.sendMessage("request_get_opload_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting operating
        load attributes."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree")

        pub.sendMessage(
            "request_set_opload_attributes",
            node_id=[4],
            package={"description": "Big test operating load."},
        )

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree"
        )
