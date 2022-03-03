# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.allocation.allocation_integration_test.py is part of The
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
from ramstk.models.dbtables import RAMSTKAllocationTable


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
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

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocationRecord)
        print("\033[36m\n\t\tsucceed_retrieve_allocation topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_allocation")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_allocation")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(6).data["allocation"], RAMSTKAllocationRecord)
        assert tree.get_node(6).data["allocation"].revision_id == 1
        assert tree.get_node(6).data["allocation"].hardware_id == 6
        assert tree.get_node(6).data["allocation"].parent_id == 2
        print("\033[36m\n\t\tsucceed_insert_allocation topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == ("do_insert: Parent node '9' is not in the tree")
        print("\033[35m\n\t\tfail_insert_allocation topic was broadcast on no parent.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print(
            "\033[35m\n\t\tfail_insert_allocation topic was broadcast on no revision."
        )

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey "
            "(fld_hardware_id)=(9) is not present in table "
            '"ramstk_hardware".'
        )
        print(
            "\033[35m\n\t\tfail_insert_allocation topic was broadcast on no hardware."
        )

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_allocation")

        assert test_datamanager.tree.get_node(6) is None

        test_attributes["hardware_id"] = 6
        test_attributes["parent_id"] = 2
        test_attributes["record_id"] = 6
        pub.sendMessage("request_insert_allocation", attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(6).data["allocation"], RAMSTKAllocationRecord
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, test_datamanager):
        """should not add a record when passed a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_allocation")

        assert test_datamanager.tree.get_node(7) is None

        test_attributes["hardware_id"] = 7
        test_attributes["parent_id"] = 9
        test_attributes["record_id"] = 6
        pub.sendMessage("request_insert_allocation", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_datamanager):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")

        assert test_datamanager.tree.get_node(8) is None

        test_attributes["revision_id"] = 40
        test_attributes["hardware_id"] = 8
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 6
        pub.sendMessage("request_insert_allocation", attributes=test_attributes)

        assert test_datamanager.tree.get_node(8) is None

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_allocation")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_datamanager):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")

        assert test_datamanager.tree.get_node(9) is None

        test_attributes["hardware_id"] = 9
        test_attributes["record_id"] = 6
        pub.sendMessage("request_insert_allocation", attributes=test_attributes)

        assert test_datamanager.tree.get_node(9) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_allocation")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_allocation topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Allocation ID 300.")
        print(
            "\033[35m\nfail_delete_allocation topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Allocation ID 2.")
        print(
            "\033[35m\nfail_delete_allocation topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_allocation")

        _last_id = test_datamanager.last_id
        pub.sendMessage("request_delete_allocation", node_id=_last_id)

        assert test_datamanager.last_id == 4
        assert test_datamanager.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_allocation")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_allocation")

        pub.sendMessage("request_delete_allocation", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_allocation")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_datamanager):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_allocation")

        test_datamanager.tree.get_node(1).data.pop("allocation")
        pub.sendMessage("request_delete_allocation", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_allocation")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].parent_id == 1
        assert tree.get_node(2).data["allocation"].percent_weight_factor == 0.9832
        assert tree.get_node(2).data["allocation"].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_allocation topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast for Allocation.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for allocation "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_allocation topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_allocation topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent allocation with "
            "allocation ID 100."
        )
        print(
            "\033[35m\nfail_update_allocation topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for allocation ID 1."
        )
        print(
            "\033[35m\nfail_update_allocation topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_allocation")

        _allocation = test_datamanager.do_select(2)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        pub.sendMessage("request_update_allocation", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_allocation")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _allocation = test_datamanager.do_select(1)
        _allocation.percent_weight_factor = 0.9832
        _allocation.mtbf_goal = 12000
        _allocation = test_datamanager.do_select(2)
        _allocation.percent_weight_factor = 0.9961
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
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

        _allocation = test_datamanager.do_select(1)
        _allocation.mtbf_goal = {1: 2}
        pub.sendMessage("request_update_allocation", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_allocation")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_allocation"
        )

        _allocation = test_datamanager.do_select(1)
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
    def test_do_update_no_data_package(self, test_datamanager):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_allocation")

        test_datamanager.tree.get_node(1).data.pop("allocation")
        pub.sendMessage("request_update_allocation", node_id=1)

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
        assert isinstance(tree.get_node(1).data["allocation"], RAMSTKAllocationRecord)
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["allocation"].hazard_rate_goal == 0.00005
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_datamanager):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_allocation_attributes"
        )

        test_datamanager.do_get_attributes(node_id=2)

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


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast on AGREE.")

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast on ARINC.")

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast on equal.")

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
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast on FOO.")

    @pytest.mark.integration
    def test_do_calculate_agree_allocation(self, test_datamanager):
        """should apportion the record ID reliability goal using the AGREE method."""
        pub.subscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

        test_datamanager.tree.get_node(1).data["allocation"].allocation_method_id = 2
        test_datamanager.tree.get_node(1).data["allocation"].reliability_goal = 0.717
        test_datamanager.tree.get_node(2).data["allocation"].mission_time = 100.0
        test_datamanager.tree.get_node(2).data["allocation"].n_sub_subsystems = 6
        test_datamanager.tree.get_node(2).data["allocation"].n_sub_elements = 2
        test_datamanager.tree.get_node(2).data["allocation"].weight_factor = 0.95

        pub.sendMessage(
            "request_calculate_agree_allocation",
            node_id=1,
            duty_cycle=90.0,
        )

        pub.unsubscribe(self.on_succeed_calculate_agree, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_arinc_allocation(self, test_datamanager):
        """should apportion the record ID reliability goal using the ARINC method."""
        pub.subscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

        test_datamanager._node_hazard_rate = 0.000628
        test_datamanager._system_hazard_rate = 0.002681

        test_datamanager.tree.get_node(1).data["allocation"].allocation_method_id = 3
        test_datamanager.tree.get_node(1).data["allocation"].goal_measure_id = 2
        test_datamanager.tree.get_node(1).data["allocation"].hazard_rate_goal = 0.000617
        test_datamanager.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_active = 0.000628

        pub.sendMessage("request_calculate_arinc_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_arinc, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_equal_allocation(self, test_datamanager):
        """should apportion the record ID reliability goal using the equal method."""
        pub.subscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

        test_datamanager.tree.get_node(1).data["allocation"].allocation_method_id = 1
        test_datamanager.tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_datamanager.tree.get_node(1).data["allocation"].reliability_goal = 0.995

        pub.sendMessage("request_calculate_equal_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_equal, "succeed_calculate_allocation")

    @pytest.mark.integration
    def test_do_calculate_foo_allocation(self, test_datamanager):
        """should apportion the record ID reliability goal using the FOO method."""
        pub.subscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")

        test_datamanager.tree.get_node(1).data["allocation"].allocation_method_id = 4
        test_datamanager.tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_datamanager.tree.get_node(1).data["allocation"].hazard_rate_goal = 0.000617
        test_datamanager.tree.get_node(2).data["allocation"].env_factor = 6
        test_datamanager.tree.get_node(2).data["allocation"].soa_factor = 2
        test_datamanager.tree.get_node(2).data["allocation"].op_time_factor = 9
        test_datamanager.tree.get_node(2).data["allocation"].int_factor = 3

        pub.sendMessage("request_calculate_foo_allocation", node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_foo, "succeed_calculate_allocation")
