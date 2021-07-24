# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.cause.cause_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmCause
from ramstk.models.programdb import RAMSTKCause


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmCause()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 3}
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_cause")
    pub.unsubscribe(dut._do_insert_cause, "request_insert_cause")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["cause"], RAMSTKCause)
        print("\033[36m\nsucceed_retrieve_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """should return a Tree() object populated with RAMSTKCause instances."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_cause")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 1, "mechanism_id": 3}
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_cause")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["cause"], RAMSTKCause)
        print("\033[36m\nsucceed_insert_cause topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_mechanism_id)=(100) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_cause")

        pub.sendMessage("request_insert_cause")

        assert test_datamanager.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_cause")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """should send the fail message if the mechanism ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_cause")

        _parent_id = test_datamanager._parent_id
        test_datamanager._parent_id = 100
        pub.sendMessage("request_insert_cause")
        test_datamanager._parent_id = _parent_id

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_cause")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_cause topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Cause ID 300."
        )
        print("\033[35m\nfail_delete_cause topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Cause ID 4."
        )
        print("\033[35m\nfail_delete_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove the deleted record from the records tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_cause")

        pub.sendMessage("request_delete_cause", node_id=3)

        assert test_datamanager.last_id == 4

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_cause")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when node ID doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_cause")

        pub.sendMessage("request_delete_cause", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_cause")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """should send the fail message when node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_cause")

        test_datamanager.tree.remove_node(4)
        pub.sendMessage("request_delete_cause", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_cause")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["cause"].description == ("Test failure cause")
        assert tree.get_node(3).data["cause"].rpn_detection == 4
        print("\033[36m\nsucceed_update_cause topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for cause ID 3 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_cause topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent cause with cause ID 100."
        )
        print("\033[35m\nfail_update_cause topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for cause ID 3.")
        print("\033[35m\nfail_update_cause topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """should update record in database and records tree."""
        pub.subscribe(self.on_succeed_update, "succeed_update_cause")

        test_datamanager.tree.get_node(3).data[
            "cause"
        ].description = "Test failure cause"
        test_datamanager.tree.get_node(3).data["cause"].rpn_detection = 4
        pub.sendMessage("request_update_cause", node_id=3, table="cause")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_cause")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """should update all records in database and records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_datamanager.tree.get_node(3).data[
            "cause"
        ].description = "Test failure cause"
        test_datamanager.tree.get_node(3).data["cause"].rpn_detection = 2
        test_datamanager.tree.get_node(4).data[
            "cause"
        ].description = "Big test failure cause"
        test_datamanager.tree.get_node(4).data["cause"].rpn_detection = 7
        pub.sendMessage("request_update_all_causes")

        assert (
            test_datamanager.tree.get_node(3).data["cause"].description
            == "Test failure cause"
        )
        assert test_datamanager.tree.get_node(3).data["cause"].rpn_detection == 2
        assert (
            test_datamanager.tree.get_node(4).data["cause"].description
            == "Big test failure cause"
        )
        assert test_datamanager.tree.get_node(4).data["cause"].rpn_detection == 7

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """should send fail message if attribute has wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_cause")

        _cause = test_datamanager.do_select(3, table="cause")
        _cause.rpn_detection = {1: 2}
        pub.sendMessage("request_update_cause", node_id=3, table="cause")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_cause")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """should send fail message when attempting to update root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_cause"
        )

        _cause = test_datamanager.do_select(4, table="cause")
        _cause.rpn_detection_new = {1: 2}
        pub.sendMessage("request_update_cause", node_id=0, table="cause")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_cause"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send fail message when node ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_cause")

        pub.sendMessage("request_update_cause", node_id=100, table="cause")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_cause")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """should send fail message when node ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_cause")

        test_datamanager.tree.get_node(3).data.pop("cause")
        pub.sendMessage("request_update_cause", node_id=3, table="cause")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_cause")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["cause_id"] == 3
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["cause"], RAMSTKCause)
        assert isinstance(tree.get_node(4).data["cause"], RAMSTKCause)
        print("\033[36m\nsucceed_get_cause_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["cause"].rpn_detection == 4
        print("\033[36m\nsucceed_get_cause_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """should return a dict of attribute key:value pairs."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        test_datamanager.do_get_attributes(node_id=3, table="cause")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the data manager records tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_cause_tree")

        pub.sendMessage("request_get_cause_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_cause_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """should set the value of the requested attribute."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_cause_tree")

        pub.sendMessage(
            "request_set_cause_attributes",
            node_id=[4],
            package={"rpn_detection": 4},
        )

        assert test_datamanager.do_select(4, table="cause").rpn_detection == 4

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_cause_tree")
