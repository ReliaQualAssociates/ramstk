# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opload.opload_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing operating load integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpLoad
from ramstk.models.programdb import RAMSTKOpLoad


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpLoad()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 1}
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_opload")
    pub.unsubscribe(dut._do_insert_opload, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["opload"], RAMSTKOpLoad)
        print("\033[36m\nsucceed_retrieve_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoad instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_opload")

        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["opload"], RAMSTKOpLoad)
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id)=(1, 1, 6, 100) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id)=(10, 1, 6, 1) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_insert_sibling(self, test_datamanager):
        """do_insert() should send the success message with the ID of the newly
        inserted node and the data manager's tree after successfully inserting
        a new opload."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")

        pub.sendMessage("request_insert_opload", parent_id=2)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_opload() should send the fail message if attempting to
        add an operating load to a non-existent opload ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_opload")

        test_datamanager._parent_id = 100
        pub.sendMessage("request_insert_opload", parent_id=100)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating stress."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_opload")

        test_datamanager._revision_id = 10
        pub.sendMessage("request_insert_opload", parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_opload topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent OpLoad ID 300."
        )
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent OpLoad ID 1."
        )
        print("\033[35m\nfail_delete_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_opload")

        test_datamanager._do_delete(2)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

        test_datamanager._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")

        test_datamanager.tree.remove_node(1)
        test_datamanager._do_delete(1)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["opload"].description == ("Test failure " "opload")
        assert tree.get_node(1).data["opload"].rpn_detection == 4
        print("\033[36m\nsucceed_update_opload topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for opload ID 1 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_opload topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_opload topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent opload with opload ID 100."
        )
        print("\033[35m\nfail_update_opload topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for opload ID 1.")
        print("\033[35m\nfail_update_opload topic was broadcast")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_opload")

        test_datamanager.tree.get_node(1).data[
            "opload"
        ].description = "Test failure opload"
        test_datamanager.tree.get_node(1).data["opload"].rpn_detection = 4

        pub.sendMessage("request_update_opload", node_id=1, table="opload")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_oploads")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

        _opload = test_datamanager.do_select(1, table="opload")
        _opload.rpn_detection = {1: 2}

        pub.sendMessage("request_update_opload", node_id=1, table="opload")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opload"
        )

        _opload = test_datamanager.do_select(1, table="opload")
        _opload.rpn_detection_new = {1: 2}

        pub.sendMessage("request_update_opload", node_id=0, table="opload")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_opload"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed an OpLoad ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

        pub.sendMessage("request_update_opload", node_id=100, table="opload")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_opload")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_opload")

        test_datamanager.tree.get_node(1).data.pop("opload")
        pub.sendMessage("request_update_opload", node_id=1, table="opload")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["load_id"] == 1
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["opload"], RAMSTKOpLoad)
        print("\033[36m\nsucceed_get_opload_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["opload"].description == "Jared Kushner"
        print("\033[36m\nsucceed_get_opload_tree topic was broadcast")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        pub.sendMessage("request_get_opload_attributes", node_id=1, table="opload")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_datamanager):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree")

        pub.sendMessage("request_get_opload_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree"
        )

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree")

        pub.sendMessage(
            "request_set_opload_attributes",
            node_id=[1, ""],
            package={"description": "Big test operating load."},
        )

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_opload_tree"
        )
