# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opstress.opstress_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing operating stress integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKOpStressRecord, RAMSTKOpStressTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpStressTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        {
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "opload_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["opstress"], RAMSTKOpStressRecord)
        print("\033[36m\nsucceed_retrieve_opstress topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpStressRecord instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_opstress")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_opstress")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(5).data["opstress"], RAMSTKOpStressRecord)
        print("\033[36m\nsucceed_insert_opstress topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_opload_id)=(100) is not present in table "
            '"ramstk_op_load".'
        )
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should send success message, add record to record tree and update
        last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_opstress")

        pub.sendMessage("request_insert_opstress", attributes=test_attributes)

        assert test_tablemodel.last_id == 5

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_opstress")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_tablemodel):
        """should send the fail message when load ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_opstress")

        test_attributes["opload_id"] = 100
        pub.sendMessage("request_insert_opstress", attributes=test_attributes)

        assert test_tablemodel.last_id == 5

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_opstress")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_opstress topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Opstress ID 300.")
        print("\033[35m\nfail_delete_opstress topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Opstress ID 4.")
        print("\033[35m\nfail_delete_opstress topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_opstress")

        pub.sendMessage("request_delete_opstress", node_id=3)

        assert test_tablemodel.last_id == 4
        assert test_tablemodel.tree.get_node(3) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_opstress")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when stress ID does not exist."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_opstress")

        pub.sendMessage("request_delete_opstress", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_opstress")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """should send the fail message record does not exist in record tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_opstress")

        test_tablemodel.tree.remove_node(4)
        pub.sendMessage("request_delete_opstress", node_id=4)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_opstress")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["opstress"].description == (
            "Test failure opstress"
        )
        assert tree.get_node(3).data["opstress"].measurable_parameter == "Parameter"
        print("\033[36m\nsucceed_update_opstress topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for opstress ID 3 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_opstress topic was broadcast on wrong data type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_opstress topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent opstress with opstress ID 100."
        )
        print("\033[35m\nfail_update_opstress topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for opstress ID 3.")
        print("\033[35m\nfail_update_opstress topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_opstress")

        test_tablemodel.tree.get_node(3).data[
            "opstress"
        ].description = "Test failure opstress"
        test_tablemodel.tree.get_node(3).data[
            "opstress"
        ].measurable_parameter = "Parameter"

        pub.sendMessage("request_update_opstress", node_id=3)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_opstress")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_opstresss")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_opstress")

        _opstress = test_tablemodel.do_select(3)
        _opstress.measurable_parameter = {1: 2}

        pub.sendMessage("request_update_opstress", node_id=3)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_opstress")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opstress"
        )

        _opstress = test_tablemodel.do_select(3)
        _opstress.measurable_parameter = {1: 2}

        pub.sendMessage("request_update_opstress", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opstress"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed an OpStress ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_opstress")

        pub.sendMessage("request_update_opstress", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_opstress")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a FMEA ID that
        has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_opstress")

        test_tablemodel.tree.get_node(3).data.pop("opstress")
        pub.sendMessage("request_update_opstress", node_id=3)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_opstress")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["opload_id"] == 3
        assert attributes["description"] == ""
        print("\033[36m\nsucceed_get_opstress_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["opstress"], RAMSTKOpStressRecord)
        print("\033[36m\nsucceed_get_opstress_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(3).data["opstress"].description == "Big test operating load."
        )
        print("\033[36m\nsucceed_get_opstress_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of mode attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_opstress_attributes")

        pub.sendMessage("request_get_opstress_attributes", node_id=3, table="opstress")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_opstress_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_tablemodel):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opstress_tree"
        )

        pub.sendMessage("request_get_opstress_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opstress_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting operating
        load attributes."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_opstress_tree")

        pub.sendMessage(
            "request_set_opstress_attributes",
            node_id=[3],
            package={"description": "Big test operating load."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_opstress_tree")
