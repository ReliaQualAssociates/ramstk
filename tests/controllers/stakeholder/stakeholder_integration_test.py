# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.stakeholder.stakeholder_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import amStakeholder, dmStakeholder
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "stakeholder_id": 1,
    }


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    # Create the device under test (dut) and connect to the configuration.
    dut = amStakeholder(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_stakeholder_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_stakeholder_tree")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmStakeholder()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholder")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut.do_insert, "request_insert_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["stakeholder"], RAMSTKStakeholder)
        print("\033[36m\nsucceed_retrieve_stakeholders topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all(1) should clear a populate Tree when selecting a new
        set of stakeholder records."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_stakeholders")

        test_datamanager.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_stakeholders")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["stakeholder"], RAMSTKStakeholder)
        assert tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert (
            tree.get_node(3).data["stakeholder"].description == "New Stakeholder Input"
        )
        print("\033[36m\nsucceed_insert_stakeholder topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(40) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_stakeholder topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """_do_insert_stakeholder() should send the success message after
        successfully inserting a new top-level stakeholder."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_stakeholder")

        pub.sendMessage("request_insert_stakeholder", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_stakeholder")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")

        test_datamanager._fkey["revision_id"] = 40
        pub.sendMessage("request_insert_stakeholder", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_stakeholder topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Stakeholder ID 300.")
        print("\033[35m\nfail_delete_stakeholder topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Stakeholder ID 1.")
        print("\033[35m\nfail_delete_stakeholder topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_stakeholder")

        pub.sendMessage("request_delete_stakeholder", node_id=test_datamanager.last_id)

        assert test_datamanager.last_id == 1

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_stakeholder")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a non-existent stakeholder."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_stakeholder")

        pub.sendMessage("request_delete_stakeholder", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_stakeholder")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_stakeholder")

        test_datamanager.tree.remove_node(1)
        pub.sendMessage("request_delete_stakeholder", node_id=1)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_stakeholder")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["stakeholder"].description == ("Test Stakeholder")
        print("\033[36m\nsucceed_update_stakeholder topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for stakeholder "
            "input ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent stakeholder with stakeholder ID "
            "100."
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for stakeholder ID 1."
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should broadcast the succeed update message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_stakeholders")

        _stakeholder = test_datamanager.do_select(1)
        _stakeholder.description = "Test Stakeholder"
        pub.sendMessage("request_update_stakeholder", node_id=1, table="stakeholder")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_stakeholders")

    @pytest.mark.integration
    def test_do_update_all(self):
        """do_update_all() should update all the functions in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_stakeholder")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should broadcast the fail update message when one or
        more attribute values is the wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholders")

        _stakeholder = test_datamanager.do_select(1)
        _stakeholder.user_float_1 = {1: 2}
        pub.sendMessage("request_update_stakeholder", node_id=1, table="stakeholder")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholders")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should broadcast the fail update message when one or
        more attribute values is the wrong data type and it is attempting to
        update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_stakeholder"
        )

        _stakeholder = test_datamanager.do_select(1)
        _stakeholder.user_float_1 = {1: 2}

        pub.sendMessage("request_update_stakeholder", node_id=0, table="stakeholder")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_stakeholder"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_stakeholder")

        pub.sendMessage("request_update_stakeholder", node_id=100, table="stakeholder")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_stakeholder")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_stakeholder")

        test_datamanager.tree.get_node(1).data.pop("stakeholder")
        pub.sendMessage("request_update_stakeholder", node_id=1, table="stakeholder")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_stakeholder")


class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["stakeholder_id"] == 1
        assert attributes["description"] == "Test Stakeholder Input"
        assert attributes["priority"] == 1
        print("\033[36m\nsucceed_get_stakeholder_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["stakeholder"], RAMSTKStakeholder)
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["stakeholder"].description == "Testing set "
            "description from "
            "moduleview."
        )
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """do_get_attributes() should return a dict of stakeholder attributes
        on success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_stakeholder_attributes"
        )

        pub.sendMessage(
            "request_get_stakeholder_attributes", node_id=1, table="stakeholder"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_stakeholder_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """on_get_tree() should return the stakeholder treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_stakeholder_tree"
        )

        pub.sendMessage("request_get_stakeholder_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_stakeholder_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_stakeholder_tree")

        pub.sendMessage(
            "request_set_stakeholder_attributes",
            node_id=[1],
            package={"description": "Testing set description from moduleview."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_stakeholder_tree")
