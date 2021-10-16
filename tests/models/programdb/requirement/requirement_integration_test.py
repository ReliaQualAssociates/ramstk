# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.requirement.requirement_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module integrations."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKRequirementRecord, RAMSTKRequirementTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKRequirementTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_requirement")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_requirement")
    pub.unsubscribe(dut.do_update, "request_update_requirement")
    pub.unsubscribe(dut.do_create_all_codes, "request_create_all_requirement_codes")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_requirement_tree")
    pub.unsubscribe(dut.do_create_code, "request_create_requirement_code")
    pub.unsubscribe(dut.do_delete, "request_delete_requirement")
    pub.unsubscribe(dut.do_insert, "request_insert_requirement")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["requirement"], RAMSTKRequirementRecord)

        print("\033[36m\nsucceed_retrieve_requirements topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """do_select_all() should clear the existing Tree when a new group of
        requirements is selected."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_requirements")

        test_tablemodel.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_requirements")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["requirement"], RAMSTKRequirementRecord)
        assert tree.get_node(5).data["requirement"].parent_id == 0
        assert tree.get_node(5).data["requirement"].requirement_id == 5
        assert tree.get_node(5).data["requirement"].description == "New Requirement"

        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_succeed_insert_child(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(6).data["requirement"], RAMSTKRequirementRecord)
        assert tree.get_node(6).data["requirement"].parent_id == 1
        assert tree.get_node(6).data["requirement"].requirement_id == 6
        assert tree.get_node(6).data["requirement"].description == "New Requirement"
        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "_do_insert_requirement: Attempted to insert child requirement "
            "under non-existent requirement ID 32."
        )
        print("\033[35m\nfail_insert_requirement topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(10) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\nfail_insert_requirement topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message after successfully inserting a
        new top-level requirement."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_requirement")

        pub.sendMessage("request_insert_requirement", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_requirement")

    @pytest.mark.integration
    def test_do_insert_child(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message after successfully inserting a
        new child requirement."""
        pub.subscribe(self.on_succeed_insert_child, "succeed_insert_requirement")

        test_attributes["parent_id"] = 1
        pub.sendMessage("request_insert_requirement", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_child, "succeed_insert_requirement")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_tablemodel):
        """do_insert() should send the fail message attempting to add a child to a non-
        existent requirement."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_requirement")

        test_attributes["parent_id"] = 32
        pub.sendMessage("request_insert_requirement", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_requirement")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """_do_insert_requirement() should send the success message after successfully
        inserting a n operating stress."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_requirement")

        test_attributes["revision_id"] = 10
        test_attributes["parent_id"] = 1
        pub.sendMessage("request_insert_requirement", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_requirement")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_requirement topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Requirement ID 300.")
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Requirement ID 2.")
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_requirement")

        pub.sendMessage("request_delete_requirement", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_requirement")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """_do_delete() should send the fail message when attempting to delete a non-
        existent requirement."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_requirement")

        pub.sendMessage("request_delete_requirement", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_requirement")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_requirement")

        test_tablemodel.tree.remove_node(2)
        pub.sendMessage("request_delete_requirement", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_requirement")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["requirement"].description == "Test Requirement"
        print("\033[36m\nsucceed_update_requirement topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for requirement "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_requirement topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_requirement topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent requirement with "
            "requirement ID 100."
        )
        print(
            "\033[35m\nfail_update_requirement topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for requirement ID 1."
        )
        print(
            "\033[35m\nfail_update_requirement topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_requirement")

        _requirement = test_tablemodel.do_select(1)
        _requirement.description = "Test Requirement"

        pub.sendMessage("request_update_requirement", node_id=1, table="requirement")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_requirement")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should update all the functions in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _requirement = test_tablemodel.do_select(1)
        _requirement.description = "Big test requirement #1"
        _requirement = test_tablemodel.do_select(2)
        _requirement.description = "Big test requirement #2"

        pub.sendMessage("request_update_all_requirements")

        assert test_tablemodel.do_select(1).description == "Big test requirement #1"
        assert test_tablemodel.do_select(2).description == "Big test requirement #2"

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_requirement")

        _requirement = test_tablemodel.do_select(1)
        _requirement.priority = {1: 2}

        pub.sendMessage("request_update_requirement", node_id=1, table="requirement")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_requirement")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_requirement"
        )

        _requirement = test_tablemodel.do_select(1)
        _requirement.priority = {1: 2}

        pub.sendMessage("request_update_requirement", node_id=0, table="requirement")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_requirement"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_requirement")

        pub.sendMessage("request_update_requirement", node_id=100, table="requirement")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_requirement")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should send the fail_update_requirement message when there is no
        data package attached to the node."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_requirement")

        test_tablemodel.tree.get_node(1).data.pop("requirement")
        pub.sendMessage("request_update_requirement", node_id=1, table="requirement")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_requirement")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["requirement_id"] == 1
        assert attributes["description"] == ""
        assert attributes["priority"] == 0
        print("\033[36m\nsucceed_get_requirement_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["requirement"], RAMSTKRequirementRecord)
        print("\033[36m\nsucceed_get_requirement_tree topic was broadcast on get tree.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["requirement"].requirement_code == "REQ-0001"
        print(
            "\033[36m\nsucceed_get_requirement_tree topic was broadcast on set "
            "attributes."
        )

    def on_succeed_set_attributes_default(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["requirement"].validated_date == date.today()
        print(
            "\033[36m\nsucceed_get_requirement_tree topic was broadcast on set "
            "default attributes."
        )

    def on_succeed_create_code(self, requirement_code):
        assert requirement_code == "DOYLE-0001"
        print("\033[36m\nsucceed_create_requirement_code topic was broadcast")

    def on_fail_create_code_non_existent_id(self, error_message):
        assert error_message == (
            "do_create_code: No data package found for requirement ID 10."
        )
        print("\033[36m\nfail_create_requirement_code topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """_do_get_attributes() should return a dict of requirement attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_requirement_attributes"
        )

        pub.sendMessage(
            "request_get_requirement_attributes", node_id=1, table="requirement"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_requirement_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """on_get_tree() should return the requirement treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_requirements_tree"
        )

        pub.sendMessage("request_get_requirement_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_requirements_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_requirements_tree")

        pub.sendMessage(
            "request_set_requirement_attributes",
            node_id=[1, -1],
            package={"requirement_code": "REQ-0001"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_requirements_tree")

    @pytest.mark.integration
    def test_do_set_attributes_default(self, test_tablemodel):
        """do_set_attributes() should set validation date to today() if no value is
        passed."""
        pub.subscribe(
            self.on_succeed_set_attributes_default, "succeed_get_requirements_tree"
        )

        pub.sendMessage(
            "request_set_requirement_attributes",
            node_id=[1, -1],
            package={"validated_date": None},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes_default, "succeed_get_requirements_tree"
        )

    @pytest.mark.integration
    def test_do_create_code(self, test_tablemodel):
        """do_create_requirement_code() should return."""
        pub.subscribe(self.on_succeed_create_code, "succeed_create_requirement_code")

        pub.sendMessage("request_create_requirement_code", node_id=1, prefix="DOYLE")

        pub.unsubscribe(self.on_succeed_create_code, "succeed_create_requirement_code")

    @pytest.mark.integration
    def test_do_create_code_non_existent_id(self, test_tablemodel):
        """do_create_requirement_code() should send the fail message when there is no
        node in the tree for the passed Requirement ID."""
        pub.subscribe(
            self.on_fail_create_code_non_existent_id, "fail_create_requirement_code"
        )

        pub.sendMessage("request_create_requirement_code", node_id=10, prefix="DOYLE")

        pub.unsubscribe(
            self.on_fail_create_code_non_existent_id, "fail_create_requirement_code"
        )

    @pytest.mark.integration
    def test_do_create_all_codes(self, test_tablemodel):
        """do_create_requirement_code() should return."""
        pub.sendMessage("request_create_all_requirement_codes", prefix="DOYLE")

        assert (
            test_tablemodel.tree.get_node(2).data["requirement"].requirement_code
            == "DOYLE-0002"
        )
