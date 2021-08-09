# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism
from ramstk.models.programdb import RAMSTKMechanism


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
    }


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMechanism()
    dut.do_connect(test_program_dao)
    dut.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_mechanism_rpn")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_retrieve_mechanism topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with RAMSTKMechanism
        instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_insert_mechanism topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_mode_id)=(100) is not present in table "
            '"ramstk_mode".'
        )
        print("\033[35m\nfail_insert_mechanism topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the recrod tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mechanism")

        pub.sendMessage("request_insert_mechanism", attributes=test_attributes)

        assert test_datamanager.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mechanism")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_datamanager):
        """should send the fail message if the mode ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_mechanism")

        test_attributes["mode_id"] = 100
        pub.sendMessage("request_insert_mechanism", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_mechanism")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mechanism topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mechanism ID 300.")
        print("\033[35m\nfail_delete_mechanism topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mechanism ID 4.")
        print("\033[35m\nfail_delete_mechanism topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mechanism")

        pub.sendMessage("request_delete_mechanism", node_id=3)

        assert test_datamanager.last_id == 4

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mechanism")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """_do_delete() should send the fail message when attempting to delete a node
        ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

        pub.sendMessage("request_delete_mechanism", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mechanism")

        test_datamanager.tree.remove_node(4)
        pub.sendMessage("request_delete_mechanism", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mechanism")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["mechanism"].description == (
            "Test failure mechanism"
        )
        assert tree.get_node(3).data["mechanism"].rpn_detection == 4
        print("\033[36m\nsucceed_update_mechanism topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for mechanism ID 3 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mechanism with mechanism ID 100."
        )
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mechanism ID 3.")
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mechanism")

        test_datamanager.tree.get_node(3).data[
            "mechanism"
        ].description = "Test failure mechanism"
        test_datamanager.tree.get_node(3).data["mechanism"].rpn_detection = 4
        pub.sendMessage("request_update_mechanism", node_id=3, table="mechanism")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mechanism")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_datamanager.tree.get_node(3).data[
            "mechanism"
        ].description = "Test failure mechanism"
        test_datamanager.tree.get_node(3).data["mechanism"].rpn_detection = 2
        test_datamanager.tree.get_node(4).data[
            "mechanism"
        ].description = "Big test failure mechanism"
        test_datamanager.tree.get_node(4).data["mechanism"].rpn_detection = 7
        pub.sendMessage("request_update_all_mechanisms")

        assert (
            test_datamanager.tree.get_node(3).data["mechanism"].description
            == "Test failure mechanism"
        )
        assert test_datamanager.tree.get_node(3).data["mechanism"].rpn_detection == 2
        assert (
            test_datamanager.tree.get_node(4).data["mechanism"].description
            == "Big test failure mechanism"
        )
        assert test_datamanager.tree.get_node(4).data["mechanism"].rpn_detection == 7

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

        _mechanism = test_datamanager.do_select(3)
        _mechanism.rpn_detection = {1: 2}
        pub.sendMessage("request_update_mechanism", node_id=3, table="mechanism")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_mechanism"
        )

        _mechanism = test_datamanager.do_select(4)
        _mechanism.rpn_detection_new = {1: 2}
        pub.sendMessage("request_update_mechanism", node_id=0, table="mechanism")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_mechanism"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a PoF ID that
        doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mechanism")

        pub.sendMessage("request_update_mechanism", node_id=100, table="mechanism")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mechanism")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a FMEA ID that
        has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mechanism")

        test_datamanager.tree.get_node(3).data.pop("mechanism")
        pub.sendMessage("request_update_mechanism", node_id=3, table="mechanism")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mechanism")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mechanism_id"] == 3
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["mechanism"], RAMSTKMechanism)
        assert isinstance(tree.get_node(4).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_get_mechanism_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["mechanism"].rpn_detection == 4
        print("\033[36m\nsucceed_get_mechanism_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of mode attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        test_datamanager.do_get_attributes(node_id=3, table="mechanism")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the failure Mechanism records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mechanism_tree"
        )

        pub.sendMessage("request_get_mechanism_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mechanism_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting operating
        load attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_mechanism_tree")

        pub.sendMessage(
            "request_set_mechanism_attributes",
            node_id=[4],
            package={"rpn_detection": 4},
        )

        assert test_datamanager.do_select(4).rpn_detection == 4

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_mechanism_tree")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1) is None
        print("\033[36m\nsucceed_delete_mechanism topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mechanism ID 10.")
        print("\033[35m\nfail_delete_mechanism topic was broadcast on non-existent ID.")

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mechanism ID 2.")
        print("\033[35m\nfail_delete_mechanism topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete_mission() should send the success message after successfully
        deleting a mission."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mechanism")

        pub.sendMessage("request_delete_mechanism", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mechanism")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete_mission() should send the sfail message when attempting to delete
        a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

        pub.sendMessage("request_delete_mechanism", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_mechanism")

        test_datamanager.tree.get_node(2).data.pop("mechanism")
        pub.sendMessage("request_delete_mechanism", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_mechanism")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_rpn_mechanism(self, tree: Tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["mechanism"].rpn == 192
        assert tree.get_node(3).data["mechanism"].rpn_new == 64
        print("\033[36m\nsucceed_calculate_mechanism_rpn topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_mechanism_rpn(self, test_attributes, test_datamanager):
        """should calculate the mechanism RPN."""
        pub.subscribe(
            self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_mechanism_rpn"
        )

        test_datamanager.do_select_all(test_attributes)

        test_datamanager.tree.get_node(3).data["mechanism"].rpn_occurrence = 8
        test_datamanager.tree.get_node(3).data["mechanism"].rpn_detection = 3
        test_datamanager.tree.get_node(3).data["mechanism"].rpn_occurrence_new = 4
        test_datamanager.tree.get_node(3).data["mechanism"].rpn_detection_new = 2

        pub.sendMessage("request_calculate_mechanism_rpn", severity=8)

        assert test_datamanager.tree.get_node(3).data["mechanism"].rpn == 192
        assert test_datamanager.tree.get_node(3).data["mechanism"].rpn_new == 64

        pub.unsubscribe(
            self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_mechanism_rpn"
        )
