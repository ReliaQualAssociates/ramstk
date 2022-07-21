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
    SystemTestUpdateMethods,
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
class TestUpdateAllocation(SystemTestUpdateMethods):
    """Class for testing Allocation update() and update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKAllocationRecord
    _tag = "allocation"
    _update_bad_value_obj = {1: 2}
    _update_field_str = "percent_weight_factor"
    _update_id = 2
    _update_value_obj = 0.9832


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
