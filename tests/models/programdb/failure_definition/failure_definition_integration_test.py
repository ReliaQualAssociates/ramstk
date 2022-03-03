# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.definition.definition_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing definition module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureDefinitionRecord
from ramstk.models.dbtables import RAMSTKFailureDefinitionTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFailureDefinitionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"function_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_definition")
    pub.unsubscribe(dut.do_update, "request_update_definition")
    pub.unsubscribe(dut.do_get_tree, "request_get_definition_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_definition")
    pub.unsubscribe(dut.do_insert, "request_insert_definition")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["definition"],
            RAMSTKFailureDefinitionRecord,
        )
        print("\033[36m\nsucceed_retrieve_definition topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinitionRecord instances on success when there is already a tree
        of definitions."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_definitions")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_all_definition")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class to test data controller insert methods using actual database."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree[3].data["definition"], RAMSTKFailureDefinitionRecord)
        print("\033[36m\nsucceed_insert_definition topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_fail_insert_no_function(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_function_id)=(40) is not present in table "
            '"ramstk_function".'
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message after successfully inserting a
        new definition."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_definition")

        test_attributes["parent_id"] = 0
        test_attributes["record_id"] = 0
        assert test_tablemodel.tree.get_node(4) is None

        pub.sendMessage("request_insert_definition", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(4).data["definition"],
            RAMSTKFailureDefinitionRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_definition")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """do_insert() should send the fail_insert_definition message when attempting
        to insert a new definition with a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_definition")

        test_attributes["parent_id"] = 0
        test_attributes["record_id"] = 0
        test_attributes["revision_id"] = 40
        pub.sendMessage("request_insert_definition", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_definition")

    @pytest.mark.integration
    def test_do_insert_no_function(self, test_attributes, test_tablemodel):
        """do_insert() should send the fail_insert_definition message when attempting
        to insert a new definition with a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_function, "fail_insert_definition")

        test_attributes["parent_id"] = 0
        test_attributes["record_id"] = 0
        test_attributes["function_id"] = 40
        pub.sendMessage("request_insert_definition", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_function, "fail_insert_definition")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_definition topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Definition ID 10.")
        print("\033[35m\nfail_delete_definition topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Definition ID 2.")
        print("\033[35m\nfail_delete_definition topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """_do_delete_definition() should send the success message after successfully
        deleting a definition."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_definition")

        pub.sendMessage("request_delete_definition", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_definition")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """_do_delete_definition() should send the fail message when attempting to
        delete a non-existent definition."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_definition")

        assert test_tablemodel.tree.get_node(10) is None

        pub.sendMessage("request_delete_definition", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_definition")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """should send the fail message when the node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_definition")

        test_tablemodel.tree.remove_node(2)
        pub.sendMessage("request_delete_definition", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_definition")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["definition"].definition == "Big test definition"
        print("\033[36m\nsucceed_update_definition topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for "
            "definition ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_definition topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_definition topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent definition "
            "with definition ID 100."
        )
        print("\033[35m\nfail_update_definition topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for definition ID 1."
        )
        print("\033[35m\nfail_update_definition topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should send the succeed_update_definition on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_definition")

        _definition = test_tablemodel.do_select(1)
        _definition.definition = "Big test definition"
        pub.sendMessage("request_update_definition", node_id=1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_definition")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all definition() should return None on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _definition = test_tablemodel.do_select(1)
        _definition.definition = "Big test definition #1"
        _definition = test_tablemodel.do_select(2)
        _definition.definition = "Big test definition #2"

        pub.sendMessage("request_update_all_definitions")

        _definition = test_tablemodel.do_select(1)
        assert _definition.definition == "Big test definition #1"

        _definition = test_tablemodel.do_select(2)
        assert _definition.definition == "Big test definition #2"

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should send the succeed_update_definition on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_definition")

        test_tablemodel.tree.get_node(1).data["definition"].definition = {
            1: "Big test definition",
        }
        pub.sendMessage("request_update_definition", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_definition")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_definition",
        )

        test_tablemodel.tree.get_node(1).data["definition"].definition = {
            1: "Big test definition",
        }
        pub.sendMessage("request_update_definition", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_definition",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update_definition() should broadcast the fail message when attempting to
        save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_definition")

        pub.sendMessage("request_update_definition", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_definition")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Function ID
        that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_definition")

        test_tablemodel.tree.get_node(1).data.pop("definition")
        pub.sendMessage("request_update_definition", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_definition")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["revision_id"] == 1
        assert attributes["definition"] == "Failure Definition"
        print("\033[36m\nsucceed_get_definition_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["definition"], RAMSTKFailureDefinitionRecord
        )
        print("\033[36m\nsucceed_get_definition_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["definition"].definition == "Test " "Description"
        print("\033[36m\nsucceed_get_definition_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """_do_get_attributes() should return a dict of definition records on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_definition_attributes"
        )

        test_tablemodel.do_get_attributes(node_id=1)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_definition_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """on_get_tree() should return the definition treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_definition_tree"
        )

        pub.sendMessage("request_definition_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_definition_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_definition_tree")

        pub.sendMessage(
            "request_set_definition_attributes",
            node_id=1,
            package={"definition": "Test Description"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_definition_tree")
