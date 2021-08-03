# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.failure_definition.failure_definition_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFailureDefinition
from ramstk.models.programdb import RAMSTKFailureDefinition


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "definition_id": 1,
        "definition": "Failure Definition",
    }


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFailureDefinition()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_failure_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_failure_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_failure_definition")
    pub.unsubscribe(dut.do_update, "request_update_failure_definition")
    pub.unsubscribe(dut.do_get_tree, "request_get_failure_definition_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_failure_definition")
    pub.unsubscribe(dut.do_insert, "request_insert_failure_definition")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["failure_definition"],
            RAMSTKFailureDefinition,
        )
        print("\033[36m\nsucceed_retrieve_failure_definition topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinition instances on success when there is already a
        tree of definitions."""
        pub.subscribe(
            self.on_succeed_select_all, "succeed_retrieve_failure_definitions"
        )

        test_datamanager.do_select_all(attributes=test_attributes)

        pub.unsubscribe(
            self.on_succeed_select_all, "succeed_retrieve_failure_definitions"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class to test data controller insert methods using actual database."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree[3].data["failure_definition"], RAMSTKFailureDefinition)
        print("\033[36m\nsucceed_insert_failure_definition topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "_do_insert_failure_definition: Attempting to add failure "
            "definition to non-existent revision 40."
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """do_insert() should send the success message after successfully
        inserting a new failure definition."""
        pub.subscribe(
            self.on_succeed_insert_sibling, "succeed_insert_failure_definition"
        )

        assert test_datamanager.tree.get_node(3) is None

        pub.sendMessage("request_insert_failure_definition", attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(3).data["failure_definition"],
            RAMSTKFailureDefinition,
        )

        pub.unsubscribe(
            self.on_succeed_insert_sibling, "succeed_insert_failure_definition"
        )

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_datamanager):
        """do_insert() should send the fail_insert_failure_definition message
        when attempting to insert a new failure definition with a non-existent
        revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_failure_definition")

        test_attributes["revision_id"] = 40
        pub.sendMessage("request_insert_failure_definition", attributes=test_attributes)

        pub.unsubscribe(
            self.on_fail_insert_no_revision, "fail_insert_failure_definition"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_failure_definition topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "Attempted to delete non-existent Failure Definition ID 10."
        )
        print("\033[35m\nfail_delete_failure_definition topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "Attempted to delete non-existent Failure Definition ID 2."
        )
        print("\033[35m\nfail_delete_failure_definition topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self):
        """_do_delete_failure_definition() should send the success message
        after successfully deleting a definition."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_failure_definition")

        pub.sendMessage("request_delete_failure_definition", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_failure_definition")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete_failure_definition() should send the fail message when
        attempting to delete a non-existent failure definition."""
        pub.subscribe(
            self.on_fail_delete_non_existent_id, "fail_delete_failure_definition"
        )

        assert test_datamanager.tree.get_node(10) is None

        pub.sendMessage("request_delete_failure_definition", node_id=10)

        pub.unsubscribe(
            self.on_fail_delete_non_existent_id, "fail_delete_failure_definition"
        )

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """should send the fail message when the node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_failure_definition")

        test_datamanager.tree.remove_node(2)
        pub.sendMessage("request_delete_failure_definition", node_id=2)

        pub.unsubscribe(
            self.on_fail_delete_not_in_tree, "fail_delete_failure_definition"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["failure_definition"].definition
            == "Big test definition"
        )
        print("\033[36m\nsucceed_update_failure_definition topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for failure "
            "definition ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent failure definition "
            "with failure definition ID 100."
        )
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for failure definition ID 1."
        )
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should send the succeed_update_failure_definition on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_failure_definition")

        _failure_definition = test_datamanager.do_select(1, table="failure_definition")
        _failure_definition.definition = "Big test definition"
        pub.sendMessage(
            "request_update_failure_definition", node_id=1, table="failure_definition"
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_failure_definition")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all failure_definition() should return None on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _failure_definition = test_datamanager.do_select(1, table="failure_definition")
        _failure_definition.definition = "Big test definition #1"
        _failure_definition = test_datamanager.do_select(2, table="failure_definition")
        _failure_definition.definition = "Big test definition #2"

        pub.sendMessage("request_update_all_failure_definitions")

        _failure_definition = test_datamanager.do_select(1, table="failure_definition")
        assert _failure_definition.definition == "Big test definition #1"

        _failure_definition = test_datamanager.do_select(2, table="failure_definition")
        assert _failure_definition.definition == "Big test definition #2"

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should send the succeed_update_failure_definition on
        success."""
        pub.subscribe(
            self.on_fail_update_wrong_data_type, "fail_update_failure_definition"
        )

        test_datamanager.tree.get_node(1).data["failure_definition"].definition = {
            1: "Big test definition",
        }
        pub.sendMessage(
            "request_update_failure_definition", node_id=1, table="failure_definition"
        )

        pub.unsubscribe(
            self.on_fail_update_wrong_data_type, "fail_update_failure_definition"
        )

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_failure_definition",
        )

        test_datamanager.tree.get_node(1).data["failure_definition"].definition = {
            1: "Big test definition",
        }
        pub.sendMessage(
            "request_update_failure_definition", node_id=0, table="failure_definition"
        )

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_failure_definition",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update_failure_definition() should broadcast the fail message
        when attempting to save a non-existent ID."""
        pub.subscribe(
            self.on_fail_update_non_existent_id, "fail_update_failure_definition"
        )

        pub.sendMessage(
            "request_update_failure_definition",
            node_id=100,
            table="failure_definitions",
        )

        pub.unsubscribe(
            self.on_fail_update_non_existent_id, "fail_update_failure_definition"
        )

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(
            self.on_fail_update_no_data_package, "fail_update_failure_definition"
        )

        test_datamanager.tree.get_node(1).data.pop("failure_definition")
        pub.sendMessage(
            "request_update_failure_definition", node_id=1, table="failure_definitions"
        )

        pub.unsubscribe(
            self.on_fail_update_no_data_package, "fail_update_failure_definition"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["revision_id"] == 1
        assert attributes["definition"] == "Failure Definition"
        print("\033[36m\nsucceed_get_failure_definition_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["failure_definition"], RAMSTKFailureDefinition
        )
        print("\033[36m\nsucceed_get_failure_definition_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["failure_definition"].definition == "Test "
            "Description"
        )
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return a dict of failure definition
        records on success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_failure_definition_attributes"
        )

        test_datamanager.do_get_attributes(1, "failure_definition")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_failure_definition_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """on_get_tree() should return the failure definition treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_failure_definition_tree"
        )

        pub.sendMessage("request_failure_definition_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_failure_definition_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should send the success message."""
        pub.subscribe(
            self.on_succeed_set_attributes, "succeed_get_failure_definition_tree"
        )

        pub.sendMessage(
            "request_set_failure_definition_attributes",
            node_id=[1],
            package={"definition": "Test Description"},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes, "succeed_get_failure_definition_tree"
        )
