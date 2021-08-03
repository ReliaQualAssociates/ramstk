# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision
from ramstk.models.programdb import RAMSTKRevision


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "name": "New Revision",
    }


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    dut = dmRevision()
    dut.do_connect(test_program_dao)
    dut.do_select_all()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_revision")
    pub.unsubscribe(dut.do_update, "request_update_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_revision_tree")
    pub.unsubscribe(dut.do_select_all, "request_retrieve_revisions")
    pub.unsubscribe(dut.do_delete, "request_delete_revision")
    pub.unsubscribe(dut.do_insert, "request_insert_revision")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["revision"], RAMSTKRevision)
        print("\033[36m\nsucceed_retrieve_revision topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select() should clear any existing tree when selecting
        revisions."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_revisions")

        test_datamanager.do_select_all()

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_revisions")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["revision"], RAMSTKRevision)
        assert tree.get_node(3).data["revision"].revision_id == 3
        assert tree.get_node(3).data["revision"].name == "New Revision"

        print("\033[36m\nsucceed_insert_revision topic was broadcast")

    def on_fail_insert_no_database(self, error_message):
        assert error_message == (
            "dao.do_insert: No database connected when attempting to add a record."
        )
        print("\033[35m\nfail_insert_revision topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_revision")

        pub.sendMessage("request_insert_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_revision")

    @pytest.mark.integration
    def test_do_insert_no_database(self, test_attributes):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_fail_insert_no_database, "fail_insert_revision")

        DUT = dmRevision()
        DUT.do_insert(attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_database, "fail_insert_revision")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_revision topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Revision ID 300.")
        print("\033[35m\nfail_delete_revision topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Revision ID 1.")
        print("\033[35m\nfail_delete_revision topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_revision")

        pub.sendMessage("request_delete_revision", node_id=2)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_revision")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a non-existent revision."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_revision")

        pub.sendMessage("request_delete_revision", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_revision")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_revision")

        test_datamanager.tree.remove_node(1)
        pub.sendMessage("request_delete_revision", node_id=1)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_revision")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["revision"].name == "Test Revision"
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for revision ID "
            "1 was the wrong type."
        )
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent revision with revision "
            "ID 100."
        )
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for revision ID 1.")
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should send the succeed_update_revision message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_revision")

        _revision = test_datamanager.do_select(1, table="revision")
        _revision.name = "Test Revision"

        pub.sendMessage("request_update_revision", node_id=1, table="revision")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_revision")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update() should send the succeed_update_revision message on
        success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _revision = test_datamanager.do_select(1, table="revision")
        _revision.name = "Big test revision"

        pub.sendMessage("request_update_all_revisions")

        assert (
            test_datamanager.do_select(1, table="revision").name == "Big test revision"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should send the fail_update_revision message when passed
        a revision ID that that has a wrong data type for one or more
        attributes."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_revision")

        test_datamanager.tree.get_node(1).data["revision"].cost = None
        pub.sendMessage("request_update_revision", node_id=1, table="revision")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_revision")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should end the fail_update_revision message when passed
        a revision ID that has no data package."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_revision"
        )

        pub.sendMessage("request_update_revision", node_id=0, table="revision")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_revision"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        revision ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_revision")

        pub.sendMessage("request_update_revision", node_id=100, table="revision")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_revision")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_revision")

        test_datamanager.tree.get_node(1).data.pop("revision")
        pub.sendMessage("request_update_revision", node_id=1, table="revision")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_revision")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["revision_id"] == 1
        assert attributes["name"] == "Test Revision"
        assert attributes["program_time"] == 0.0
        print("\033[36m\nsucceed_get_revision_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["revision"], RAMSTKRevision)
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["revision"].revision_code == "ABC"
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return a dict of revision attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_revision_attributes")

        pub.sendMessage("request_get_revision_attributes", node_id=1, table="revision")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_revision_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_datamanager):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_revision_tree"
        )

        pub.sendMessage("request_get_revision_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_revision_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_revision_tree")

        pub.sendMessage(
            "request_set_revision_attributes",
            node_id=[1],
            package={"revision_code": "ABC"},
        )

        assert test_datamanager.tree.get_node(1).data["revision"].revision_code == "ABC"

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_revision_tree")
