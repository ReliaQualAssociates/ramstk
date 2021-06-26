# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.hazards.hazards_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazards module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmHazards


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
    pub.unsubscribe(dut.do_select_all, "selected_function")
    pub.unsubscribe(dut.do_set_all_attributes, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut._do_delete, "request_delete_hazard")
    pub.unsubscribe(dut._do_insert_hazard, "request_insert_hazard")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "_do_insert_hazard: A database error "
            "occurred when attempting to add a child "
            "function to parent function ID 1."
        )
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    def on_fail_insert_no_function(self, error_message):
        assert error_message == ("An error occured with RAMSTK.")
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_insert_no_revision(self, test_datamanager):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")

        test_datamanager.revision_id = 40
        test_datamanager._do_insert_hazard(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_hazard")

    @pytest.mark.integration
    def test_insert_no_function(self, test_datamanager):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_function, "fail_insert_hazard")

        test_datamanager.function_id = 40
        test_datamanager._do_insert_hazard(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_function, "fail_insert_hazard")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["hazard"].potential_hazard == "Big Hazard"
        print("\033[36m\nsucceed_update_hazard topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for hazard ID 1 "
            "was the wrong type."
        )
        print("\033[35m\nfail_update_hazard topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_hazard")

        test_datamanager.tree.get_node(1).data["hazard"].potential_hazard = "Big Hazard"
        test_datamanager.do_update(1, "hazard")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_hazard")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        test_datamanager.tree.get_node(1).data[
            "hazard"
        ].potential_hazard = "Big test hazard"

        pub.sendMessage("request_update_all_functions")

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
        test_datamanager.do_update(1, "hazard")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_hazard")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        test_datamanager.tree.get_node(1).data["hazard"].assembly_effect = {1: "What?"}
        test_datamanager.do_update(0, "hazard")
