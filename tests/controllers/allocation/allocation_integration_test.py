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
from ramstk.controllers import amAllocation, dmAllocation
from ramstk.models.programdb import RAMSTKAllocation


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    """Get an analysis manager instance for each test class."""
    # Create the device under test (dut) and connect to the configuration.
    dut = amAllocation(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_allocation_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_allocation_tree")
    pub.unsubscribe(dut.on_get_tree, "succeed_retrieve_allocation")
    pub.unsubscribe(dut.on_get_tree, "succeed_update_allocation")
    pub.unsubscribe(dut._do_calculate_allocation, "request_allocate_reliability")
    pub.unsubscribe(
        dut._do_calculate_allocation_goals, "request_calculate_allocation_goals"
    )
    pub.unsubscribe(dut._do_calculate_allocation, "request_calculate_allocation")
    pub.unsubscribe(
        dut._on_get_hardware_attributes, "succeed_get_all_hardware_attributes"
    )

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmAllocation()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_allocation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_allocation")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_allocation")
    pub.unsubscribe(dut.do_update, "request_update_allocation")
    pub.unsubscribe(dut.do_get_tree, "request_get_allocation_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_set_all_attributes, "succeed_calculate_allocation_goals")
    pub.unsubscribe(dut._do_delete, "request_delete_hardware")
    pub.unsubscribe(dut._do_insert_allocation, "request_insert_allocation")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocation)
        print("\033[36m\nsucceed_retrieve_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should clear nodes from an existing allocation
        tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_allocation")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 8
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(node_id).data["allocation"], RAMSTKAllocation)
        assert tree.get_node(node_id).data["allocation"].revision_id == 1
        assert tree.get_node(node_id).data["allocation"].hardware_id == 8
        assert tree.get_node(node_id).data["allocation"].parent_id == 7
        print("\033[36m\nsucceed_insert_allocation topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "_do_insert_allocation: Attempted to insert child "
            "allocation under non-existent allocation ID 10."
        )
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_hardware_id)=(9) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self):
        """should send the success message after adding a new allocation record."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_allocation")

        pub.sendMessage("request_insert_allocation", hardware_id=8, parent_id=7)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_parent(self):
        """should send the fail message when the parent ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_allocation")

        pub.sendMessage("request_insert_allocation", hardware_id=3, parent_id=10)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """should send the fail message when the revision ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")

        test_datamanager._revision_id = 40
        pub.sendMessage("request_insert_allocation", hardware_id=4, parent_id=1)
        test_datamanager._revision_id = 1

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self):
        """should send the fail message when the hardware ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")

        pub.sendMessage("request_insert_allocation", hardware_id=9, parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_allocation topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent allocation record "
            "with hardware ID 300."
        )
        print("\033[36m\nfail_delete_allocation topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent allocation record "
            "with hardware ID 2."
        )
        print("\033[35m\nfail_delete_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should send the success message after deleting an allocation record."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_allocation")

        _last_id = test_datamanager.last_id
        pub.sendMessage("request_delete_hardware", node_id=test_datamanager.last_id)

        assert test_datamanager.last_id == 6
        assert test_datamanager.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_allocation")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when the allocation ID does not exist."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_allocation")

        pub.sendMessage("request_delete_hardware", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_allocation")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """should send the fail message when the node doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_allocation")

        test_datamanager.tree.remove_node(2)
        pub.sendMessage("request_delete_hardware", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_allocation")


@pytest.mark.usefixtures("test_datamanager", "test_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].parent_id == 1
        assert tree.get_node(2).data["allocation"].percent_weight_factor == 0.9832
        assert tree.get_node(2).data["allocation"].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_allocation topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for allocation "
            "ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent allocation with "
            "allocation ID 100."
        )
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for allocation ID 1."
        )
        print("\033[35m\nfail_update_allocation topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_allocation")

        _allocation = test_datamanager.do_select(2, table="allocation")
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        pub.sendMessage("request_update_allocation", node_id=2, table="allocation")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_allocation")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

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

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage("request_update_allocation", node_id=1, table="allocation")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_allocation"
        )

        _allocation = test_datamanager.do_select(1, table="allocation")
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage("request_update_allocation", node_id=0, table="allocation")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_allocation"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_allocation")

        pub.sendMessage("request_update_allocation", node_id=100, table="allocation")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_allocation")

        test_datamanager.tree.get_node(1).data.pop("allocation")
        pub.sendMessage("request_update_allocation", node_id=1, table="allocation")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_allocation")


@pytest.mark.usefixtures("test_datamanager", "test_toml_user_configuration")
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
        print("\033[36m\nsucceed_get_allocation_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocation)
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_goal == 0.00005
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """do_get_attributes() should return a dict of allocation attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_allocation_attributes"
        )

        test_datamanager.do_get_attributes(
            node_id=2,
            table="allocation",
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_allocation_attributes"
        )

    @pytest.mark.integration
    def test_on_get_attributes(self, test_analysismanager, test_datamanager):
        """_get_all_attributes() should update the attributes dict on
        success."""
        # This test would require using the dmHardware() to get the attributes.
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_datamanager.do_get_attributes(node_id=2, table="allocation")

        assert test_analysismanager._attributes["hardware_id"] == 2
        assert test_analysismanager._attributes["mtbf_alloc"] == 0.0

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_allocation_tree message."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_allocation_tree"
        )

        pub.sendMessage("request_allocation_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_allocation_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_allocation_tree")

        pub.sendMessage(
            "request_set_allocation_attributes",
            node_id=[2],
            package={"hazard_rate_goal": 0.00005},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_allocation_tree")


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestAnalysisMethods:
    """Class for allocation methods test suite."""

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    def on_fail_calculate_arinc(self, error_message):
        assert error_message == (
            "_do_calculate_arinc_weight_factor: Failed "
            "to allocate reliability for allocation "
            "record ID 5.  System hazard rate was 0.0."
        )
        print("\033[35m\nfail_calculate_allocation topic was broadcast")

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    def on_succeed_calculate_foo(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_alloc == pytest.approx(
            0.00049971186
        )
        assert tree.get_node(2).data["allocation"].mtbf_alloc == pytest.approx(
            2001.1532174
        )
        assert tree.get_node(2).data["allocation"].reliability_alloc == pytest.approx(
            0.95125683
        )
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_agree_allocation(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the AGREE method."""
        pub.subscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 2
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].reliability_goal = 0.717
        test_analysismanager._tree.get_node(2).data["allocation"].duty_cycle = 90.0
        test_analysismanager._tree.get_node(2).data["allocation"].mission_time = 100.0
        test_analysismanager._tree.get_node(2).data["allocation"].n_sub_subsystems = 6
        test_analysismanager._tree.get_node(2).data["allocation"].n_sub_elements = 2
        test_analysismanager._tree.get_node(2).data["allocation"].weight_factor = 0.95
        test_analysismanager._do_calculate_allocation(node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the ARINC method."""
        pub.subscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._node_hazard_rate = 0.000628
        test_analysismanager._system_hazard_rate = 0.002681

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 3
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 2
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617
        test_analysismanager._tree.get_node(2).data[
            "allocation"
        ].hazard_rate_active = 0.000628
        test_analysismanager._do_calculate_allocation(node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

    @pytest.mark.skip
    def test_do_calculate_arinc_allocation_zero_system_hazard_rate(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_allocation() should send an error message when
        attempting to allocate an assembly with a zero hazard rate using the
        ARINC method."""
        pub.subscribe(self.on_fail_calculate_arinc, "fail_calculate_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._node_hazard_rate = 0.000628
        test_analysismanager._system_hazard_rate = 0.0

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 3
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 2
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_active = 0.0
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617
        test_analysismanager._tree.get_node(2).data[
            "allocation"
        ].hazard_rate_active = 0.000628
        test_analysismanager._do_calculate_allocation(node_id=1)

        pub.unsubscribe(self.on_fail_calculate_arinc, "fail_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_equal_allocation(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the equal apportionment method."""
        pub.subscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 1
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].reliability_goal = 0.995
        test_analysismanager._do_calculate_allocation(node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_foo_allocation(self, test_analysismanager, test_datamanager):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the feasibility of objectives method."""
        pub.subscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")

        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 4
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617
        test_analysismanager._tree.get_node(2).data["allocation"].env_factor = 6
        test_analysismanager._tree.get_node(2).data["allocation"].soa_factor = 2
        test_analysismanager._tree.get_node(2).data["allocation"].op_time_factor = 9
        test_analysismanager._tree.get_node(2).data["allocation"].int_factor = 3
        test_analysismanager._do_calculate_allocation(node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")
