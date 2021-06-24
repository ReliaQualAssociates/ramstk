# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.allocation.allocation_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Allocation module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmAllocation


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Test fixture for Allocation data manager."""
    dut = dmAllocation()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_update, "request_update_allocation")
    pub.unsubscribe(dut.do_set_all_attributes, "succeed_calculate_allocation_goals")
    pub.unsubscribe(dut._do_insert_allocation, "request_insert_allocation")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager", "test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == ("An error occurred with RAMSTK.")
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == ("An error occurred with RAMSTK.")
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")

        test_datamanager._do_insert_allocation(hardware_id=5, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")

        test_datamanager._revision_id = 40
        test_datamanager._do_insert_allocation(hardware_id=1, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")


@pytest.mark.usefixtures("test_datamanager", "test_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].parent_id == 1
        assert tree.get_node(2).data["allocation"].percent_weight_factor == 0.9832
        assert tree.get_node(2).data["allocation"].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_allocation topic was broadcast.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for allocation "
            "ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_allocation topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_allocation")

        _allocation = test_datamanager.do_select(2, table="allocation")
        _allocation.percent_weight_factor = 0.9832
        _allocation = test_datamanager.do_select(2, table="allocation")
        _allocation.mtbf_goal = 12000

        pub.sendMessage("request_update_allocation", node_id=2, table="allocation")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_allocation")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.mtbf_goal = {1: 2}

        test_datamanager.do_update(node_id=1, table="allocation")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.mtbf_goal = {1: 2}

        pub.sendMessage("request_update_allocation", node_id=0, table="allocation")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should return a zero error code on success."""
        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.percent_weight_factor = 0.9832
        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.mtbf_goal = 12000
        _allocation = test_datamanager.do_select(2, table="allocation")
        _allocation.percent_weight_factor = 0.9961
        _allocation = test_datamanager.do_select(2, table="allocation")
        _allocation.mtbf_goal = 18500

        pub.sendMessage("request_update_all_allocation")

        assert (
            test_datamanager.tree.get_node(1).data["allocation"].percent_weight_factor
            == 0.9832
        )
        assert test_datamanager.tree.get_node(1).data["allocation"].mtbf_goal == 12000
        assert (
            test_datamanager.tree.get_node(2).data["allocation"].percent_weight_factor
            == 0.9961
        )
        assert test_datamanager.tree.get_node(2).data["allocation"].mtbf_goal == 18500
