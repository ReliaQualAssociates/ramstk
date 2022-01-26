# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.environment.environment_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKEnvironmentRecord, RAMSTKEnvironmentTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKEnvironmentTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "phase_id": 1,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["environment"], RAMSTKEnvironmentRecord)
        print("\033[36m\nsucceed_retrieve_environments topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should send success message with record tree as MDS."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_environments")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_environments")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["environment"], RAMSTKEnvironmentRecord)
        print("\033[36m\nsucceed_insert_environment topic was broadcast")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_phase_id)=(20) is not present in table "
            '"ramstk_mission_phase".'
        )
        print("\033[35m\nfail_insert_environment topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(4) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_environment topic was broadcast")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes):
        """should send the success message after adding a new environment."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_environment")

        pub.sendMessage("request_insert_environment", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_environment")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes):
        """should send the fail message when the mission phase ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_environment")

        test_attributes["phase_id"] = 20
        pub.sendMessage("request_insert_environment", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_environment")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """should send the fail message when the revision ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_environment")

        test_attributes["revision_id"] = 4
        pub.sendMessage("request_insert_environment", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_environment")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_environment topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Environment ID 10.")
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Environment ID 2.")
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self):
        """should send the success message after deleting an environment record."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_environment")

        pub.sendMessage("request_delete_environment", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_environment")

    @pytest.mark.integration
    def test_do_delete_mission_non_existent_id(self):
        """should send the fail message when the environment ID does not exist."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_environment")

        pub.sendMessage("request_delete_environment", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_environment")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """should send the fail message when the node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_environment")

        pub.sendMessage("request_delete_environment", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_environment")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["environment"].name == ("Big test environment")
        print("\033[36m\nsucceed_update_environment topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for environment "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_environment topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_environment topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent environment with "
            "environment ID 10."
        )
        print(
            "\033[35m\nfail_update_environment topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for environment ID 1."
        )
        print(
            "\033[35m\nfail_update_environment topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should send the success message after updating an environment record."""
        pub.subscribe(self.on_succeed_update, "succeed_update_environment")

        _environment = test_tablemodel.do_select(1)
        _environment.name = "Big test environment"
        pub.sendMessage("request_update_environment", node_id=1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_environment")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should send the success message after updating all environment records."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _environment = test_tablemodel.do_select(1)
        _environment.name = "Even bigger test environment"

        pub.sendMessage("request_update_all_environments")

        assert test_tablemodel.do_select(1).name == "Even bigger test environment"

        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when data type is wrong for attribute."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_environment")

        _environment = test_tablemodel.do_select(1)
        _environment.name = {1: 2}
        pub.sendMessage("request_update_environment", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_environment")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when data type is wrong for root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_environment"
        )

        _environment = test_tablemodel.do_select(1)
        _environment.name = {1: 2}
        pub.sendMessage("request_update_environment", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_environment"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when the environment ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_environment")

        pub.sendMessage("request_update_environment", node_id=10)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_environment")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when no record exists for environment ID."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_environment")

        test_tablemodel.tree.get_node(1).data.pop("environment")
        pub.sendMessage("request_update_environment", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_environment")


class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["phase_id"] == 1
        assert attributes["environment_id"] == 1
        assert attributes["name"] == "Condition Name"
        print("\033[36m\nsucceed_get_environment_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["environment"], RAMSTKEnvironmentRecord)
        print("\033[36m\nsucceed_get_environment_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["environment"].name == "This is the environment name."
        )
        print("\033[36m\nsucceed_get_environment_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """should send success message when retrieving attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_environment_attributes"
        )

        pub.sendMessage(
            "request_get_environment_attributes", node_id=1, table="environment"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_environment_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree(self):
        """should send success message when retrieving record tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_environment_tree"
        )

        pub.sendMessage("request_get_environment_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_environment_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should send success message when setting attribute(s)."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_environment_tree")

        pub.sendMessage(
            "request_set_environment_attributes",
            node_id=1,
            package={"name": "This is the environment name."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_environment_tree")
