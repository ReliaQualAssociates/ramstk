# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.hazards.hazards_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazards module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import amHazards, dmHazards
from ramstk.models.programdb import RAMSTKHazardAnalysis


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "function_id": 1,
        "hazard_id": 1,
    }


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    """Get an analysis manager instance for each test class."""
    # Create the device under test (dut) and connect to the user configuration.
    dut = amHazards(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_hazard_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_hazard_tree")
    pub.unsubscribe(dut.do_calculate_fha, "request_calculate_fha")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmHazards()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "function_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hazard")
    pub.unsubscribe(dut.do_update, "request_update_hazard")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazard_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_set_all_attributes, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut.do_delete, "request_delete_hazard")
    pub.unsubscribe(dut.do_insert, "request_insert_hazard")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hazard"], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_retrieve_hazards topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all() should clear nodes from an existing Hazards tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_hazards")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_hazards")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 5
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["hazard"], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_function_id)=(10) is not present in table "
            '"ramstk_function".'
        )
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_hazard")

        assert test_datamanager.tree.get_node(5) is None

        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        assert test_datamanager.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_hazard")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_datamanager):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_hazard")

        assert test_datamanager.tree.get_node(7) is None

        test_datamanager._fkey["function_id"] = 10
        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_hazard")

    @pytest.mark.integration
    def test_insert_no_revision(self, test_attributes, test_datamanager):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")

        assert test_datamanager.tree.get_node(7) is None

        test_datamanager._fkey["revision_id"] = 40
        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hazard topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hazard ID 10.")
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hazard ID 4.")
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_hazard")

        pub.sendMessage("request_delete_hazard", node_id=1)

        assert test_datamanager.last_id == 4
        assert test_datamanager.tree.get_node(1) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_hazard")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """_do_delete_hazard() should send the success method when a hazard is
        successfully deleted."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_hazard")

        pub.sendMessage("request_delete_hazard", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_hazard")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_hazard")

        test_datamanager.tree.remove_node(4)
        pub.sendMessage("request_delete_hazard", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_hazard")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["hazard"].potential_hazard == "Big Hazard"
        print("\033[36m\nsucceed_update_hazard topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for hazard ID 1 "
            "was the wrong type."
        )
        print("\033[35m\nfail_update_hazard topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent hazard with hazard ID " "100."
        )
        print("\033[35m\nfail_update_hazard topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for hazard ID 1.")
        print("\033[35m\nfail_update_hazard topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_hazard")

        test_datamanager.tree.get_node(1).data["hazard"].potential_hazard = "Big Hazard"
        pub.sendMessage("request_update_hazard", node_id=1, table="hazard")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_hazard")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        test_datamanager.tree.get_node(1).data[
            "hazard"
        ].potential_hazard = "Big test hazard"

        pub.sendMessage("request_update_all_hazards")

        assert (
            test_datamanager.tree.get_node(1).data["hazard"].potential_hazard
            == "Big test hazard"
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_hazard")

        test_datamanager.tree.get_node(1).data["hazard"].assembly_effect = {1: "What?"}
        pub.sendMessage("request_update_hazard", node_id=1, table="hazard")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_hazard")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_hazard"
        )

        test_datamanager.tree.get_node(1).data["hazard"].assembly_effect = {1: "What?"}
        pub.sendMessage("request_update_hazard", node_id=0, table="hazard")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_hazard"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_hazard")

        pub.sendMessage("request_update_hazard", node_id=100, table="hazard")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_hazard")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_hazard")

        test_datamanager.tree.get_node(1).data.pop("hazard")
        pub.sendMessage("request_update_hazard", node_id=1, table="hazard")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_hazard")


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_id"] == 1
        assert attributes["potential_hazard"] == ""
        print("\033[36m\nsucceed_get_hazards_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hazard"], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["hazard"].potential_hazard == "Donald Trump"
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return a dict of failure definition
        records on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_hazards_attributes")

        test_datamanager.do_get_attributes(
            node_id=1,
            table="hazard",
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_hazards_attributes"
        )

    @pytest.mark.integration
    def test_on_get_attributes(self, test_analysismanager, test_datamanager):
        """_get_all_attributes() should update the attributes dict on
        success."""
        test_datamanager.do_get_attributes(node_id=1, table="hazard")

        assert test_analysismanager._attributes["function_id"] == 1
        assert test_analysismanager._attributes["potential_hazard"] == ""

    @pytest.mark.integration
    def test_on_get_tree_analysis_manager(self, test_analysismanager, test_datamanager):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_function_tree message."""
        test_datamanager.do_get_tree()

        assert isinstance(test_analysismanager._tree, Tree)
        assert isinstance(
            test_analysismanager._tree.get_node(1).data["hazard"],
            RAMSTKHazardAnalysis,
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """on_get_tree() should return the hazard treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_hazard_tree")

        pub.sendMessage("request_get_hazard_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_hazard_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_hazard_tree")

        pub.sendMessage(
            "request_set_hazard_attributes",
            node_id=[1],
            package={"potential_hazard": "Donald Trump"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_hazard_tree")


@pytest.mark.usefixtures("test_analysismanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.integration
    def test_do_calculate_fha(self, test_analysismanager, test_datamanager):
        """do_calculate_hri() should calculate the hazard risk index hazard
        analysis."""
        pub.sendMessage(
            "request_get_hazard_attributes",
            node_id=1,
            table="hazard",
        )
        pub.sendMessage("request_calculate_fha", node_id=1)

        assert test_analysismanager._attributes["assembly_hri"] == 30
        assert test_analysismanager._attributes["system_hri"] == 20
        assert test_analysismanager._attributes["assembly_hri_f"] == 20
        assert test_analysismanager._attributes["system_hri_f"] == 20
