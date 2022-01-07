# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.mission.mission_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMissionRecord, RAMSTKMissionTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mission"], RAMSTKMissionRecord)
        assert isinstance(tree.get_node(2).data["mission"], RAMSTKMissionRecord)
        assert isinstance(tree.get_node(3).data["mission"], RAMSTKMissionRecord)
        print("\033[36m\nsucceed_retrieve_missions topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """do_select_all() should clear out an existing tree and build a new one when
        called on a populated Mission data manager."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_missions")

        test_tablemodel.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_missions")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["mission"], RAMSTKMissionRecord)
        print("\033[36m\nsucceed_insert_mission topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(4) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_mission topic was broadcast on no Revision")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message with the ID of the newly
        inserted node and the data manager's tree after successfully inserting a new
        mission."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mission")

        test_tablemodel.do_insert(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mission")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """do_insert() should send the fail message attempting to insert a new mission
        for an non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_mission")

        test_attributes["revision_id"] = 4
        test_tablemodel.do_insert(attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_mission")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1) is None
        print("\033[36m\nsucceed_delete_mission topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mission ID 10.")
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Mission ID 2.")
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """_do_delete_mission() should send the success message after successfully
        deleting a mission."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mission")

        pub.sendMessage("request_delete_mission", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mission")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """_do_delete_mission() should send the sfail message when attempting to delete
        a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mission")

        pub.sendMessage("request_delete_mission", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mission")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mission")

        test_tablemodel.tree.remove_node(2)
        pub.sendMessage("request_delete_mission", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mission")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["mission"].name == ("Big test mission")
        print("\033[36m\nsucceed_update_mission topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for mission "
            "ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_mission topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_mission topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mission with mission ID 10."
        )
        print("\033[35m\nfail_update_mission topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mission ID 1.")
        print("\033[35m\nfail_update_mission topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mission")

        _mission = test_tablemodel.do_select(1)
        _mission.name = "Big test mission"

        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mission")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed_update_all message on
        success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _mission1 = test_tablemodel.do_select(1)
        _mission2 = test_tablemodel.do_select(2)
        _mission1.name = "Big test mission"
        _mission2.name = "Big test mission 2"

        pub.sendMessage("request_update_all_mission")

        _mission1 = test_tablemodel.do_select(1)
        _mission2 = test_tablemodel.do_select(2)

        assert _mission1.name == "Big test mission"
        assert _mission2.name == "Big test mission 2"

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mission")

        _mission = test_tablemodel.do_select(1)
        _mission.name = {1: 2}

        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mission")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_mission"
        )

        _mission = test_tablemodel.do_select(1)
        _mission.name = {1: 2}

        test_tablemodel.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_mission"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mission")

        test_tablemodel.do_update(10)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mission")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mission")

        test_tablemodel.tree.get_node(1).data.pop("mission")
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mission")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["revision_id"] == 1
        assert attributes["mission_id"] == 1
        assert attributes["description"] == "Test Mission 1"
        print("\033[36m\nsucceed_get_mission_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mission"], RAMSTKMissionRecord)
        print("\033[36m\nsucceed_get_mission_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["mission"].mission_time == 12.86
        print("\033[36m\nsucceed_get_mission_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mission_attributes")

        test_tablemodel.do_get_attributes(1, "mission")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_mission_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree(self, test_tablemodel):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mission_tree")

        test_tablemodel.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mission_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_mission_tree")

        test_tablemodel.do_set_attributes(
            node_id=[1, ""], package={"mission_time": 12.86}
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_mission_tree")
