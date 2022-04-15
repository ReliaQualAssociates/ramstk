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


@pytest.fixture(scope="class")
def test_table_model(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKAllocationTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_allocation")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_allocation")
    pub.unsubscribe(dut.do_update, "request_update_allocation")
    pub.unsubscribe(dut.do_get_tree, "request_get_allocation_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_allocation")
    pub.unsubscribe(dut.do_insert, "request_insert_allocation")
    pub.unsubscribe(
        dut.do_calculate_agree_allocation, "request_calculate_agree_allocation"
    )
    pub.unsubscribe(
        dut.do_calculate_arinc_allocation, "request_calculate_arinc_allocation"
    )
    pub.unsubscribe(
        dut.do_calculate_equal_allocation, "request_calculate_equal_allocation"
    )
    pub.unsubscribe(dut.do_calculate_foo_allocation, "request_calculate_foo_allocation")
    pub.unsubscribe(
        dut.do_calculate_allocation_goals, "request_calculate_allocation_goals"
    )
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocationRecord)
        print("\033[36m\n\tsucceed_retrieve_all_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_table_model):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_all_allocation")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_all_allocation")


@pytest.mark.usefixtures("test_attributes", "test_table_model", "test_hardware_table")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should add a record to the record tree."""
        assert test_table_model.tree.get_node(9) is None

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
            test_table_model.tree.get_node(9).data["allocation"], RAMSTKAllocationRecord
        )
        assert test_table_model.tree.get_node(9).data["allocation"].revision_id == 1
        assert test_table_model.tree.get_node(9).data["allocation"].hardware_id == 9
        assert test_table_model.tree.get_node(9).data["allocation"].parent_id == 2

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should NOT add a record to the record tree."""
        assert test_table_model.tree.get_node(10) is None

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

        assert test_table_model.tree.get_node(10) is None


@pytest.mark.usefixtures("test_table_model", "test_hardware_table")
class TestDeleteMethods:
    """Class for testing the do_delete() method."""

    def on_succeed_delete_hardware(self, tree):
        assert tree.get_node(7) is None
        print("\033[36m\n\tsucceed_delete_hardware topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_table_model, test_hardware_table):
        """should remove record from record tree."""
        pub.subscribe(self.on_succeed_delete_hardware, "succeed_delete_hardware")

        assert isinstance(
            test_table_model.tree.get_node(7).data["allocation"], RAMSTKAllocationRecord
        )

        # Allocation records are cascade deleted by the database server whenever the
        # corresponding Hardware record is deleted.
        pub.sendMessage("request_delete_hardware", node_id=7)

        assert test_table_model.tree.get_node(7) is None

        pub.unsubscribe(self.on_succeed_delete_hardware, "succeed_delete_hardware")


@pytest.mark.usefixtures("test_table_model")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].parent_id == 1
        assert tree.get_node(2).data["allocation"].percent_weight_factor == 0.9832
        assert tree.get_node(2).data["allocation"].mtbf_goal == 12000
        print("\033[36m\n\tsucceed_update_allocation topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for allocation.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for allocation "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\n\tfail_update_allocation topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\n\tfail_update_allocation topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent allocation with "
            "allocation ID 100."
        )
        print(
            "\033[35m\n\tfail_update_allocation topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for allocation ID 1."
        )
        print(
            "\033[35m\n\tfail_update_allocation topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_table_model):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_allocation")

        _allocation = test_table_model.do_select(2)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        pub.sendMessage("request_update_allocation", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_allocation")

    @pytest.mark.integration
    def test_do_update_all(self, test_table_model):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_allocation")

        _allocation = test_table_model.do_select(1)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        _allocation = test_table_model.do_select(2)
        _allocation.percent_weight_factor = 0.9961
        _allocation.mtbf_goal = 18500

        pub.sendMessage("request_update_all_allocation")

        assert (
            test_table_model.tree.get_node(1).data["allocation"].percent_weight_factor
            == 0.9832
        )
        assert test_table_model.tree.get_node(1).data["allocation"].mtbf_goal == 12000
        assert (
            test_table_model.tree.get_node(2).data["allocation"].percent_weight_factor
            == 0.9961
        )
        assert test_table_model.tree.get_node(2).data["allocation"].mtbf_goal == 18500

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_allocation")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_table_model):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

        _allocation = test_table_model.do_select(1)
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage("request_update_allocation", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_table_model):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_allocation"
        )

        _allocation = test_table_model.do_select(1)
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage("request_update_allocation", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_allocation"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_allocation")

        pub.sendMessage("request_update_allocation", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_allocation")

        test_table_model.tree.get_node(1).data.pop("allocation")
        pub.sendMessage("request_update_allocation", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_allocation")


@pytest.mark.usefixtures("test_table_model", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 2
        assert attributes["availability_alloc"] == 0.0
        assert attributes["env_factor"] == 1
        assert attributes["goal_measure_id"] == 1
        assert attributes["hazard_rate_alloc"] == 0.0
        assert attributes["hazard_rate_goal"] == 0.000617
        assert attributes["included"] == 1
        assert attributes["int_factor"] == 1
        assert attributes["allocation_method_id"] == 4
        assert attributes["mtbf_alloc"] == 0.0
        assert attributes["mtbf_goal"] == 0.0
        assert attributes["n_sub_systems"] == 1
        assert attributes["n_sub_elements"] == 1
        assert attributes["parent_id"] == 1
        assert attributes["percent_weight_factor"] == 0.0
        assert attributes["reliability_alloc"] == 1.0
        assert attributes["op_time_factor"] == 1
        assert attributes["soa_factor"] == 1
        assert attributes["weight_factor"] == 1
        print("\033[36m\n\tsucceed_get_allocation_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocationRecord)
        print("\033[36m\n\tsucceed_get_allocation_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_goal == 0.00005
        print("\033[36m\n\tsucceed_get_allocation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_table_model):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_allocation_attributes"
        )

        test_table_model.do_get_attributes(node_id=2)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_allocation_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_allocation_tree"
        )

        pub.sendMessage("request_get_allocation_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_allocation_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_allocation_tree")

        pub.sendMessage(
            "request_set_allocation_attributes",
            node_id=2,
            package={"hazard_rate_goal": 0.00005},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_allocation_tree")


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_agree(self, tree):
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
    def test_do_calculate_agree_allocation(self, test_table_model):
        """should apportion the record ID reliability goal using the AGREE method."""
        pub.subscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

        test_table_model.tree.get_node(1).data["allocation"].allocation_method_id = 2
        test_table_model.tree.get_node(1).data["allocation"].reliability_goal = 0.717
        test_table_model.tree.get_node(2).data["allocation"].mission_time = 100.0
        test_table_model.tree.get_node(2).data["allocation"].n_sub_subsystems = 6
        test_table_model.tree.get_node(2).data["allocation"].n_sub_elements = 2
        test_table_model.tree.get_node(2).data["allocation"].weight_factor = 0.95

        pub.sendMessage(
            "request_calculate_agree_allocation",
            node_id=1,
            duty_cycle=90.0,
        )

        pub.unsubscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation(self, test_table_model):
        """should apportion the record ID reliability goal using the ARINC method."""
        pub.subscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

        test_table_model._node_hazard_rate = 0.000628
        test_table_model._system_hazard_rate = 0.002681

        test_table_model.tree.get_node(1).data["allocation"].allocation_method_id = 3
        test_table_model.tree.get_node(1).data["allocation"].goal_measure_id = 2
        test_table_model.tree.get_node(1).data["allocation"].hazard_rate_goal = 0.000617
        test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_active = 0.000628

        pub.sendMessage("request_calculate_arinc_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_equal_allocation(self, test_table_model):
        """should apportion the record ID reliability goal using the equal method."""
        pub.subscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

        test_table_model.tree.get_node(1).data["allocation"].allocation_method_id = 1
        test_table_model.tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_table_model.tree.get_node(1).data["allocation"].reliability_goal = 0.995

        pub.sendMessage("request_calculate_equal_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_foo_allocation(self, test_table_model):
        """should apportion the record ID reliability goal using the FOO method."""
        pub.subscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")

        test_table_model.tree.get_node(1).data["allocation"].allocation_method_id = 4
        test_table_model.tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_table_model.tree.get_node(1).data["allocation"].hazard_rate_goal = 0.000617
        test_table_model.tree.get_node(2).data["allocation"].env_factor = 6
        test_table_model.tree.get_node(2).data["allocation"].soa_factor = 2
        test_table_model.tree.get_node(2).data["allocation"].op_time_factor = 9
        test_table_model.tree.get_node(2).data["allocation"].int_factor = 3

        pub.sendMessage("request_calculate_foo_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")
