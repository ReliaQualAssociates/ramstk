# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.mission_phase.mission_phase_integration_test.py is
#       part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMissionPhaseRecord
from ramstk.models.dbtables import RAMSTKMissionPhaseTable

_test_name = "Big test mission phase"


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionPhaseTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut.do_insert, "request_insert_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["mission_phase"], RAMSTKMissionPhaseRecord
        )
        print("\033[36m\n\tsucceed_retrieve_all_mission_phase topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all() should clear out an existing tree and build a new one when
        called on a populated Mission Phase data manager."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_all_mission_phase")

        pub.sendMessage("selected_revision", attributes={"revision_id": 1})

        pub.unsubscribe(
            self.on_succeed_select_all, "succeed_retrieve_all_mission_phase"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(4).data["mission_phase"], RAMSTKMissionPhaseRecord
        )
        print("\033[36m\n\tsucceed_insert_mission_phase topic was broadcast")

    def on_fail_insert_no_revision(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_mission_id)=(10) is not present "
            'in table "ramstk_mission".'
        )
        print("\033[35m\n\tfail_insert_mission_phase topic was broadcast")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """do_insert() should send the success message with the ID of the newly
        inserted node and the data manager's tree after successfully inserting a new
        mission."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mission_phase")

        test_attributes["parent_id"] = 1
        pub.sendMessage("request_insert_mission_phase", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mission_phase")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_datamanager):
        """do_insert() should send the success message after successfully inserting a
        new mission phase."""
        pub.subscribe(self.on_fail_insert_no_revision, "do_log_debug_msg")

        test_attributes["parent_id"] = 1
        test_attributes["mission_id"] = 10
        pub.sendMessage("request_insert_mission_phase", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "do_log_debug_msg")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\n\tsucceed_delete_mission_phase topic was broadcast.")

    def on_fail_delete_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        try:
            assert message == "No data package for node ID 10 in module mission_phase."
        except AssertionError:
            assert message == "Attempted to delete non-existent Mission Phase ID 10."
            print(
                "\033[35m\n\tfail_delete_mission_phase topic was broadcast on "
                "non-existent ID."
            )

    def on_fail_delete_not_in_tree(self, logger_name, message):
        assert logger_name == "DEBUG"
        try:
            assert message == "No data package for node ID 2 in module mission_phase."
            print(
                "\033[35m\n\tfail_delete_mission_phase topic was broadcast on no "
                "data package."
            )
        except AssertionError:
            assert message == "Attempted to delete non-existent Mission Phase ID 2."

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should remove the passed mission phase ID and broadcast the
        success message."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mission_phase")

        pub.sendMessage("request_delete_mission_phase", node_id=1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mission_phase")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete_mission_phase() should send the fail message when attempting to
        delete a non-existent mission phase ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_delete_mission_phase", node_id=10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove a node
        that doesn't exist from the tree even if it exists in the database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "do_log_debug_msg")

        pub.sendMessage("request_delete_mission_phase", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "do_log_debug_msg")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["mission_phase"].name == _test_name
        print("\033[36m\n\tsucceed_update_mission_phase topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for mission phase")

    def on_fail_update_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "The value for one or more attributes for mission phase ID 1 was the wrong "
            "type."
        )
        print(
            "\033[35m\n\tfail_update_mission_phase topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print("\033[35m\n\tfail_update_mission_phase topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "Attempted to save non-existent mission phase with mission phase ID 10."
        )
        print(
            "\033[35m\n\tfail_update_mission_phase topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == "No data package found for mission phase ID 1."
        print(
            "\033[35m\n\tfail_update_mission_phase topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mission_phase")

        _mission_phase = test_datamanager.do_select(1)
        _mission_phase.name = _test_name

        pub.sendMessage("request_update_mission_phase", node_id=1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mission_phase")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_mission_phase")

        _mission_phase1 = test_datamanager.do_select(1)
        _mission_phase1.name = _test_name

        pub.sendMessage("request_update_all_mission_phase")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_mission_phase")

    @pytest.mark.skip
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Requirement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _mission_phase = test_datamanager.do_select(1)
        _mission_phase.name = {1: 2}

        pub.sendMessage("request_update_mission_phase", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _mission_phase = test_datamanager.do_select(1)
        _mission_phase.name = {1: 2}

        pub.sendMessage("request_update_mission_phase", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_update_mission_phase", node_id=10)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.skip
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update_usage_profile() should broadcast the fail message when attempting
        to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        test_datamanager.tree.get_node(1).data.pop("mission_phase")
        pub.sendMessage("request_update_mission_phase", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mission_id"] == 1
        assert attributes["mission_phase_id"] == 1
        assert attributes["description"] == "Default Mission Phase 1"
        print("\033[36m\n\tsucceed_get_mission_phase_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["mission_phase"], RAMSTKMissionPhaseRecord
        )
        print("\033[36m\n\tsucceed_get_mission_phase_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["mission_phase"].phase_start == 12.86
        print("\033[36m\n\tsucceed_get_mission_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_mission_phase_attributes"
        )

        pub.sendMessage("request_get_mission_phase_attributes", node_id=1)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_mission_phase_attributes"
        )

    @pytest.mark.skip
    def test_on_get_tree(self, test_datamanager):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mission_phase_tree"
        )

        pub.sendMessage("request_get_mission_phase_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mission_phase_tree"
        )

    @pytest.mark.skip
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_mission_phase_tree")

        pub.sendMessage(
            "request_set_mission_phase_attributes",
            node_id=1,
            package={"phase_start": 12.86},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes, "succeed_get_mission_phase_tree"
        )
