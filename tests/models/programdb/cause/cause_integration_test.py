# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.cause.cause_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKCauseRecord, RAMSTKCauseTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCauseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        {
            "revision_id": 1,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_cause")
    pub.unsubscribe(dut.do_insert, "request_insert_cause")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_cause_rpn")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["cause"], RAMSTKCauseRecord)
        print("\033[36m\nsucceed_retrieve_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_tablemodel):
        """should return a Tree() object populated with RAMSTKCauseRecord instances."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_cause")

        pub.sendMessage(
            "selected_revision",
            attributes={
                "revision_id": 1,
            },
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_cause")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["cause"], RAMSTKCauseRecord)
        print("\033[36m\nsucceed_insert_cause topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == ("do_insert: Parent node '100' is not in the tree")
        print("\033[35m\nfail_insert_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_cause")

        pub.sendMessage("request_insert_cause", attributes=test_attributes)

        assert test_tablemodel.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_cause")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_tablemodel):
        """should send the fail message if the mechanism ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_cause")

        _parent_id = test_tablemodel._parent_id
        test_tablemodel._parent_id = 100
        pub.sendMessage("request_insert_cause", attributes=test_attributes)
        test_tablemodel._parent_id = _parent_id

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_cause")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_cause topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Cause ID 300.")
        print("\033[35m\nfail_delete_cause topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Cause ID 4.")
        print("\033[35m\nfail_delete_cause topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove the deleted record from the records tree and update
        last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_cause")

        pub.sendMessage("request_delete_cause", node_id=3)

        assert test_tablemodel.last_id == 4

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_cause")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when node ID doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_cause")

        pub.sendMessage("request_delete_cause", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_cause")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """should send the fail message when node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_cause")

        test_tablemodel.tree.remove_node(4)
        pub.sendMessage("request_delete_cause", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_cause")


@pytest.mark.usefixtures("test_tablemodel")
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
        print("\033[35m\nfail_update_cause topic was broadcast on wrong data type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent cause with cause ID 100."
        )
        print("\033[35m\nfail_update_cause topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for cause ID 3.")
        print("\033[35m\nfail_update_cause topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update record in database and records tree."""
        pub.subscribe(self.on_succeed_update, "succeed_update_cause")

        test_tablemodel.tree.get_node(3).data[
            "cause"
        ].description = "Test failure cause"
        test_tablemodel.tree.get_node(3).data["cause"].rpn_detection = 4
        pub.sendMessage("request_update_cause", node_id=3)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_cause")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in database and records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_tablemodel.tree.get_node(3).data[
            "cause"
        ].description = "Test failure cause"
        test_tablemodel.tree.get_node(3).data["cause"].rpn_detection = 2
        test_tablemodel.tree.get_node(4).data[
            "cause"
        ].description = "Big test failure cause"
        test_tablemodel.tree.get_node(4).data["cause"].rpn_detection = 7
        pub.sendMessage("request_update_all_causes")

        assert (
            test_tablemodel.tree.get_node(3).data["cause"].description
            == "Test failure cause"
        )
        assert test_tablemodel.tree.get_node(3).data["cause"].rpn_detection == 2
        assert (
            test_tablemodel.tree.get_node(4).data["cause"].description
            == "Big test failure cause"
        )
        assert test_tablemodel.tree.get_node(4).data["cause"].rpn_detection == 7

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send fail message if attribute has wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_cause")

        _cause = test_tablemodel.do_select(3)
        _cause.rpn_detection = {1: 2}
        pub.sendMessage("request_update_cause", node_id=3)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_cause")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send fail message when attempting to update root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_cause"
        )

        _cause = test_tablemodel.do_select(4)
        _cause.rpn_detection_new = {1: 2}
        pub.sendMessage("request_update_cause", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_cause"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send fail message when node ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_cause")

        pub.sendMessage("request_update_cause", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_cause")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send fail message when node ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_cause")

        test_tablemodel.tree.get_node(3).data.pop("cause")
        pub.sendMessage("request_update_cause", node_id=3)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_cause")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["cause_id"] == 3
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["cause"], RAMSTKCauseRecord)
        assert isinstance(tree.get_node(4).data["cause"], RAMSTKCauseRecord)
        print("\033[36m\nsucceed_get_cause_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["cause"].rpn_detection == 4
        print("\033[36m\nsucceed_get_cause_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return a dict of attribute key:value pairs."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        test_tablemodel.do_get_attributes(node_id=3, table="cause")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the data manager records tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_cause_tree")

        pub.sendMessage("request_get_cause_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_cause_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """should set the value of the requested attribute."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_cause_tree")

        pub.sendMessage(
            "request_set_cause_attributes",
            node_id=4,
            package={"rpn_detection": 4},
        )

        assert test_tablemodel.do_select(4).rpn_detection == 4

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_cause_tree")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_rpn_cause(self, tree: Tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["cause"].rpn == 192
        assert tree.get_node(3).data["cause"].rpn_new == 64
        print("\033[36m\nsucceed_calculate_cause_rpn topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_cause_rpn(self, test_attributes, test_tablemodel):
        """should calculate the cause RPN."""
        pub.subscribe(
            self.on_succeed_calculate_rpn_cause, "succeed_calculate_cause_rpn"
        )

        test_tablemodel.do_select_all(test_attributes)

        test_tablemodel.tree.get_node(3).data["cause"].rpn_occurrence = 8
        test_tablemodel.tree.get_node(3).data["cause"].rpn_detection = 3
        test_tablemodel.tree.get_node(3).data["cause"].rpn_occurrence_new = 4
        test_tablemodel.tree.get_node(3).data["cause"].rpn_detection_new = 2

        pub.sendMessage("request_calculate_cause_rpn", severity=8)

        assert test_tablemodel.tree.get_node(3).data["cause"].rpn == 192
        assert test_tablemodel.tree.get_node(3).data["cause"].rpn_new == 64

        pub.unsubscribe(
            self.on_succeed_calculate_rpn_cause, "succeed_calculate_cause_rpn"
        )
