# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.allocation.allocation_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Allocation module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKAllocationRecord
from ramstk.models.dbtables import RAMSTKAllocationTable, RAMSTKHardwareTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectAllocation(SystemTestSelectMethods):
    """Class for testing Allocation table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKAllocationRecord
    _select_id = 1
    _tag = "allocation"


@pytest.mark.usefixtures(
    "test_attributes", "integration_test_table_model", "test_hardware_table_model"
)
class TestInsertAllocation:
    """Class for testing the Allocation do_insert() method."""

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should add a record to the record tree."""
        assert integration_test_table_model.tree.get_node(9) is None

        # The allocation record is added by the database whenever a hardware record is
        # added to the database.  Adding the new allocation record to the Allocation
        # tree is triggered by the "succeed_insert_hardware" message.  Only
        # records associated with assembly type hardware are added to the Allocation
        # tree.
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 9,
                "parent_id": 2,
                "part": 0,
            },
        )

        assert isinstance(
            integration_test_table_model.tree.get_node(9).data["allocation"],
            RAMSTKAllocationRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(9).data["allocation"].revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(9).data["allocation"].hardware_id
            == 9
        )
        assert (
            integration_test_table_model.tree.get_node(9).data["allocation"].parent_id
            == 2
        )

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should NOT add a record to the record tree."""
        assert integration_test_table_model.tree.get_node(10) is None

        # The allocation record is added by the database whenever a hardware record is
        # added to the database.  Adding the new allocation record to the Allocation
        # tree is triggered by the "succeed_insert_hardware" message.  Only
        # records associated with assembly type hardware are added to the Allocation
        # tree.
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 10,
                "parent_id": 2,
                "part": 1,
            },
        )

        assert integration_test_table_model.tree.get_node(10) is None


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteAllocation(SystemTestDeleteMethods):
    """Class for testing Allocation table do_delete() method."""

    __test__ = True

    _delete_id = 1
    _next_id = 0
    _record = RAMSTKAllocationRecord
    _tag = "allocation"


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateAllocation:
    """Class for testing Allocation update() and update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKAllocationRecord
    _tag = "allocation"
    _update_id = 2

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(self._update_id).data[self._tag].parent_id == 1
        assert (
            tree.get_node(self._update_id).data[self._tag].percent_weight_factor
            == 0.9832
        )
        assert tree.get_node(self._update_id).data[self._tag].mtbf_goal == 12000
        print(f"\033[36m\n\tsucceed_update_{self._tag} topic was broadcast.")

    def on_succeed_update_all(self):
        """Listen for succeed_update messages."""
        print(
            f"\033[36m\n\tsucceed_update_all topic was broadcast on update all "
            f"{self._tag}s"
        )

    def on_fail_update_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            f"The value for one or more attributes for {self._tag} ID "
            f"{self._update_id} was the wrong type."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on wrong data "
            f"type."
        )

    def on_fail_update_root_node(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent {self._tag} with {self._tag} "
            f"ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == f"No data package found for {self._tag} ID {self._update_id}."
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update record attribute."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        _allocation = integration_test_table_model.do_select(2)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        _allocation = integration_test_table_model.do_select(self._update_id - 1)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        _allocation = integration_test_table_model.do_select(self._update_id)
        _allocation.percent_weight_factor = 0.9961
        _allocation.mtbf_goal = 18500

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id - 1)
            .data[self._tag]
            .percent_weight_factor
            == 0.9832
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id - 1)
            .data[self._tag]
            .mtbf_goal
            == 12000
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .percent_weight_factor
            == 0.9961
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .mtbf_goal
            == 18500
        )

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _allocation = integration_test_table_model.do_select(self._update_id)
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node(self, integration_test_table_model):
        """Should send the do_log_debug message when attempting to update root node."""
        pub.subscribe(self.on_fail_update_root_node, "do_log_debug_msg")

        _allocation = integration_test_table_model.do_select(self._update_id)
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(self.on_fail_update_root_node, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the do_log_debug message with non-existent ID in tree."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the do_log_debug message with no data package in tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterAllocation(SystemTestGetterSetterMethods):
    """Class for testing Allocation table getter and setter methods."""

    __test__ = True

    _package = {"hazard_rate_goal": 0.00005}
    _record = RAMSTKAllocationRecord
    _tag = "allocation"
    _test_id = 1


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestAnalysisAllocation:
    """Class for testing Allocation analytical methods."""

    def on_succeed_calculate_agree(self, tree):
        """Listen for succeed_calculate_allocation message."""
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_alloc == pytest.approx(
            0.0058364814
        )
        assert tree.get_node(2).data["allocation"].mtbf_alloc == pytest.approx(
            171.33610745
        )
        assert tree.get_node(2).data["allocation"].reliability_alloc == pytest.approx(
            0.59138779
        )
        print(
            "\033[36m\n\tsucceed_calculate_allocation topic was broadcast for AGREE "
            "method."
        )

    def on_succeed_calculate_arinc(self, tree):
        """Listen for succeed_calculate_allocation message."""
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_alloc == pytest.approx(
            0.0001445267
        )
        assert tree.get_node(2).data["allocation"].mtbf_alloc == pytest.approx(
            6919.1382176
        )
        assert tree.get_node(2).data["allocation"].reliability_alloc == pytest.approx(
            0.9856513
        )
        print(
            "\033[36m\n\tsucceed_calculate_allocation topic was broadcast for ARINC "
            "method."
        )

    def on_succeed_calculate_equal(self, tree):
        """Listen for succeed_calculate_allocation message."""
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_alloc == pytest.approx(
            5.012542e-05
        )
        assert tree.get_node(2).data["allocation"].mtbf_alloc == pytest.approx(
            19949.9582288
        )
        assert tree.get_node(2).data["allocation"].reliability_alloc == pytest.approx(
            0.995
        )
        print(
            "\033[36m\n\tsucceed_calculate_allocation topic was broadcast for EQUAL "
            "method."
        )

    def on_succeed_calculate_foo(self, tree):
        """Listen for succeed_calculate_allocation message."""
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_alloc == pytest.approx(
            0.0006151015
        )
        assert tree.get_node(2).data["allocation"].mtbf_alloc == pytest.approx(
            1625.747844
        )
        assert tree.get_node(2).data["allocation"].reliability_alloc == pytest.approx(
            0.9403434
        )
        print(
            "\033[36m\n\tsucceed_calculate_allocation topic was broadcast for FOO "
            "method."
        )

    @pytest.mark.integration
    def test_do_calculate_agree_allocation(self, integration_test_table_model):
        """Should apportion the record ID reliability goal using the AGREE method."""
        pub.subscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 2
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].reliability_goal = 0.717
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].mission_time = 100.0
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].n_sub_subsystems = 6
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].n_sub_elements = 2
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].weight_factor = 0.95

        pub.sendMessage(
            "request_calculate_agree_allocation",
            node_id=1,
            duty_cycle=90.0,
        )

        pub.unsubscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation(self, integration_test_table_model):
        """Should apportion the record ID reliability goal using the ARINC method."""
        pub.subscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

        integration_test_table_model._node_hazard_rate = 0.000628
        integration_test_table_model._system_hazard_rate = 0.002681

        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 3
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].goal_measure_id = 2
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_active = 0.000628

        pub.sendMessage("request_calculate_arinc_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_equal_allocation(self, integration_test_table_model):
        """Should apportion the record ID reliability goal using the equal method."""
        pub.subscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 1
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].goal_measure_id = 1
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].reliability_goal = 0.995

        pub.sendMessage("request_calculate_equal_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_foo_allocation(self, integration_test_table_model):
        """Should apportion the record ID reliability goal using the FOO method."""
        pub.subscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")

        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 4
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].goal_measure_id = 1
        integration_test_table_model.tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617
        integration_test_table_model.tree.get_node(2).data["allocation"].env_factor = 6
        integration_test_table_model.tree.get_node(2).data["allocation"].soa_factor = 2
        integration_test_table_model.tree.get_node(2).data[
            "allocation"
        ].op_time_factor = 9
        integration_test_table_model.tree.get_node(2).data["allocation"].int_factor = 3

        pub.sendMessage("request_calculate_foo_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")
