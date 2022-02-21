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
from ramstk.models import RAMSTKHazardRecord, RAMSTKHazardTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHazardTable()
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
    pub.unsubscribe(dut.do_set_attributes_all, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut.do_delete, "request_delete_hazard")
    pub.unsubscribe(dut.do_insert, "request_insert_hazard")
    pub.unsubscribe(dut.do_calculate_fha, "request_calculate_fha")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hazard"], RAMSTKHazardRecord)
        print("\033[36m\nsucceed_retrieve_hazards topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_hazards")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["hazard"], RAMSTKHazardRecord
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_hazards")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["hazard"], RAMSTKHazardRecord)
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_function_id)=(10) is not present in table "
            '"ramstk_function".'
        )
        print("\033[35m\nfail_insert_hazard topic was broadcast on no parent.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\nfail_insert_hazard topic was broadcast on no revision.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_hazard")

        assert test_tablemodel.tree.get_node(5) is None

        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        assert test_tablemodel.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_hazard")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_hazard")

        assert test_tablemodel.tree.get_node(7) is None

        test_attributes["function_id"] = 10
        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(7) is None

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_hazard")

    @pytest.mark.integration
    def test_insert_no_revision(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")

        assert test_tablemodel.tree.get_node(7) is None

        test_attributes["revision_id"] = 40
        pub.sendMessage("request_insert_hazard", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(7) is None

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hazard topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hazard ID 10.")
        print("\033[35m\nfail_delete_hazard topic was broadcast on non-existent ID.")

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hazard ID 4.")
        print("\033[35m\nfail_delete_hazard topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_hazard")

        pub.sendMessage("request_delete_hazard", node_id=1)

        assert test_tablemodel.last_id == 4
        assert test_tablemodel.tree.get_node(1) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_hazard")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_hazard")

        pub.sendMessage("request_delete_hazard", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_hazard")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_hazard")

        test_tablemodel.tree.get_node(4).data.pop("hazard")
        pub.sendMessage("request_delete_hazard", node_id=4)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_hazard")


@pytest.mark.usefixtures("test_tablemodel")
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
        print("\033[35m\nfail_update_hazard topic was broadcast on wrong data type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent hazard with hazard ID " "100."
        )
        print("\033[35m\nfail_update_hazard topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for hazard ID 1.")
        print("\033[35m\nfail_update_hazard topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_hazard")

        test_tablemodel.tree.get_node(1).data["hazard"].potential_hazard = "Big Hazard"
        pub.sendMessage("request_update_hazard", node_id=1)

        assert (
            test_tablemodel.tree.get_node(1).data["hazard"].potential_hazard
            == "Big Hazard"
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_hazard")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_tablemodel.tree.get_node(1).data[
            "hazard"
        ].potential_hazard = "Big test hazard"

        pub.sendMessage("request_update_all_hazards")

        assert (
            test_tablemodel.tree.get_node(1).data["hazard"].potential_hazard
            == "Big test hazard"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_hazard")

        test_tablemodel.tree.get_node(1).data["hazard"].assembly_effect = {1: "What?"}
        pub.sendMessage("request_update_hazard", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_hazard")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_hazard"
        )

        test_tablemodel.tree.get_node(1).data["hazard"].assembly_effect = {1: "What?"}
        pub.sendMessage("request_update_hazard", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_hazard"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_hazard")

        pub.sendMessage("request_update_hazard", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_hazard")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_hazard")

        test_tablemodel.tree.get_node(1).data.pop("hazard")
        pub.sendMessage("request_update_hazard", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_hazard")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_id"] == 1
        assert attributes["potential_hazard"] == ""
        print("\033[36m\nsucceed_get_hazards_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hazard"], RAMSTKHazardRecord)
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["hazard"].potential_hazard == "Donald Trump"
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_hazard_attributes")

        test_tablemodel.do_get_attributes(
            node_id=1,
            table="hazard",
        )

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_hazard_attributes")

    @pytest.mark.integration
    def test_on_get_tree(self):
        """should return the records tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_hazard_tree")

        pub.sendMessage("request_get_hazard_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_hazard_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_hazard_tree")

        pub.sendMessage(
            "request_set_hazard_attributes",
            node_id=1,
            package={"potential_hazard": "Donald Trump"},
        )

        assert (
            test_tablemodel.tree.get_node(1).data["hazard"].potential_hazard
            == "Donald Trump"
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_hazard_tree")


@pytest.mark.usefixtures("test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_fha(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_calculate_fha topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_fha(self, test_tablemodel):
        """should calculate the HRI and user-defined hazard analyses."""
        pub.subscribe(self.on_succeed_calculate_fha, "succeed_calculate_fha")

        pub.sendMessage("request_calculate_fha", node_id=1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["assembly_hri"] == 30
        assert _attributes["system_hri"] == 20
        assert _attributes["assembly_hri_f"] == 20
        assert _attributes["system_hri_f"] == 20
        assert _attributes["result_1"] == pytest.approx(1.2)
        assert _attributes["result_2"] == pytest.approx(0.6)

        pub.unsubscribe(self.on_succeed_calculate_fha, "succeed_calculate_fha")
