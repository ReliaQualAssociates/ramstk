# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.allocation.allocation_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Allocation module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKAllocation
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmAllocation
from ramstk.models.programdb import RAMSTKAllocation


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _allocation_1 = MockRAMSTKAllocation()
    _allocation_1.revision_id = 1
    _allocation_1.hardware_id = 1
    _allocation_1.availability_alloc = 0.0
    _allocation_1.env_factor = 1
    _allocation_1.goal_measure_id = 1
    _allocation_1.hazard_rate_alloc = 0.0
    _allocation_1.hazard_rate_goal = 0.0
    _allocation_1.included = 1
    _allocation_1.int_factor = 1
    _allocation_1.allocation_method_id = 1
    _allocation_1.mission_time = 100.0
    _allocation_1.mtbf_alloc = 0.0
    _allocation_1.mtbf_goal = 0.0
    _allocation_1.n_sub_systems = 1
    _allocation_1.n_sub_elements = 1
    _allocation_1.parent_id = 0
    _allocation_1.percent_weight_factor = 0.0
    _allocation_1.reliability_alloc = 1.0
    _allocation_1.reliability_goal = 0.999
    _allocation_1.op_time_factor = 1
    _allocation_1.soa_factor = 1
    _allocation_1.weight_factor = 1

    _allocation_2 = MockRAMSTKAllocation()
    _allocation_2.revision_id = 1
    _allocation_2.hardware_id = 2
    _allocation_2.availability_alloc = 0.0
    _allocation_2.env_factor = 1
    _allocation_2.goal_measure_id = 1
    _allocation_2.hazard_rate_alloc = 0.0
    _allocation_2.hazard_rate_goal = 0.0
    _allocation_2.included = 1
    _allocation_2.int_factor = 1
    _allocation_2.allocation_method_id = 1
    _allocation_2.mission_time = 100.0
    _allocation_2.mtbf_alloc = 0.0
    _allocation_2.mtbf_goal = 0.0
    _allocation_2.n_sub_systems = 1
    _allocation_2.n_sub_elements = 1
    _allocation_2.parent_id = 1
    _allocation_2.percent_weight_factor = 0.0
    _allocation_2.reliability_alloc = 1.0
    _allocation_2.reliability_goal = 0.9999
    _allocation_2.op_time_factor = 1
    _allocation_2.soa_factor = 1
    _allocation_2.weight_factor = 1

    _allocation_3 = MockRAMSTKAllocation()
    _allocation_3.revision_id = 1
    _allocation_3.hardware_id = 3
    _allocation_3.availability_alloc = 0.0
    _allocation_3.env_factor = 1
    _allocation_3.goal_measure_id = 1
    _allocation_3.hazard_rate_alloc = 0.0
    _allocation_3.hazard_rate_goal = 0.0
    _allocation_3.included = 1
    _allocation_3.int_factor = 1
    _allocation_3.allocation_method_id = 1
    _allocation_3.mission_time = 100.0
    _allocation_3.mtbf_alloc = 0.0
    _allocation_3.mtbf_goal = 0.0
    _allocation_3.n_sub_systems = 1
    _allocation_3.n_sub_elements = 1
    _allocation_3.parent_id = 1
    _allocation_3.percent_weight_factor = 0.0
    _allocation_3.reliability_alloc = 1.0
    _allocation_3.reliability_goal = 0.99999
    _allocation_3.op_time_factor = 1
    _allocation_3.soa_factor = 1
    _allocation_3.weight_factor = 1

    DAO = MockDAO()
    DAO.table = [
        _allocation_1,
        _allocation_2,
        _allocation_3,
    ]

    yield DAO


@pytest.fixture
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "availability_alloc": 0.0,
        "env_factor": 1,
        "goal_measure_id": 1,
        "hazard_rate_alloc": 0.0,
        "hazard_rate_goal": 0.0,
        "included": 1,
        "int_factor": 1,
        "allocation_method_id": 1,
        "mission_time": 100.0,
        "mtbf_alloc": 0.0,
        "mtbf_goal": 0.0,
        "n_sub_systems": 1,
        "n_sub_elements": 1,
        "parent_id": 1,
        "percent_weight_factor": 0.0,
        "reliability_alloc": 1.0,
        "reliability_goal": 0.999,
        "op_time_factor": 1,
        "soa_factor": 1,
        "weight_factor": 1,
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmAllocation()
    dut.do_connect(mock_program_dao)

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
    pub.unsubscribe(dut.do_calculate_allocation, "request_calculate_allocation")
    pub.unsubscribe(
        dut.do_calculate_allocation_goals, "request_calculate_allocation_goals"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a table manager instance."""
        assert isinstance(test_datamanager, dmAllocation)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "allocation"
        assert test_datamanager._root == 0
        assert test_datamanager._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_datamanager._revision_id == 0
        assert test_datamanager._record == RAMSTKAllocation
        assert test_datamanager.last_id == 0
        assert test_datamanager.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_allocation_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_allocation_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_allocation"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_allocation"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_allocation_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_allocation")
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_allocation")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_allocation")
        assert pub.isSubscribed(
            test_datamanager.do_calculate_allocation, "request_calculate_allocation"
        )
        assert pub.isSubscribed(
            test_datamanager.do_calculate_allocation_goals,
            "request_calculate_allocation_goals",
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with DB records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["allocation"], MockRAMSTKAllocation
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["allocation"], MockRAMSTKAllocation
        )
        assert isinstance(
            test_datamanager.tree.get_node(3).data["allocation"], MockRAMSTKAllocation
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return the record for the passed record ID."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _allocation = test_datamanager.do_select(1)

        assert isinstance(_allocation, MockRAMSTKAllocation)
        assert _allocation.included == 1
        assert _allocation.parent_id == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """should return None when a non-existent record ID is requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_datamanager):
        """should return a new record instance with ID fields populated."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _new_record = test_datamanager.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKAllocation)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a new record to the records tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 4
        assert isinstance(
            test_datamanager.tree.get_node(4).data["allocation"], RAMSTKAllocation
        )
        assert test_datamanager.tree.get_node(4).data["allocation"].revision_id == 1
        assert test_datamanager.tree.get_node(4).data["allocation"].hardware_id == 4
        assert test_datamanager.tree.get_node(4).data["allocation"].parent_id == 1


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _last_id = test_datamanager.last_id
        test_datamanager.do_delete(node_id=_last_id)

        assert test_datamanager.last_id == 2
        assert test_datamanager.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_goals_reliability_specified(
        self, test_attributes, test_datamanager
    ):
        """should calculate h(t) and MTBF goals from a specified R(t) goal."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _allocation = test_datamanager.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 1
        _allocation.mission_time = 100.0
        _allocation.reliability_goal = 0.99732259

        test_datamanager.do_calculate_allocation_goals(1)
        _attributes = test_datamanager.do_select(1).get_attributes()

        assert _attributes["hazard_rate_goal"] == pytest.approx(0.00002681)
        assert _attributes["mtbf_goal"] == pytest.approx(37299.5151063)

    @pytest.mark.unit
    def test_do_calculate_goals_hazard_rate_specified(
        self, test_attributes, test_datamanager
    ):
        """should calculate MTBF and R(t) goals from a specified h(t) goal."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _allocation = test_datamanager.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 2
        _allocation.mission_time = 100.0
        _allocation.hazard_rate_goal = 0.00002681

        test_datamanager.do_calculate_allocation_goals(1)
        _attributes = test_datamanager.do_select(1).get_attributes()

        assert _attributes["mtbf_goal"] == pytest.approx(37299.5151063)
        assert _attributes["reliability_goal"] == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_goals_mtbf_specified(self, test_attributes, test_datamanager):
        """should calculate the h(t) and R(t) goals from a specified MTBF goal."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _allocation = test_datamanager.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 3
        _allocation.mission_time = 100.0
        _allocation.mtbf_goal = 37300.0

        test_datamanager.do_calculate_allocation_goals(1)
        _attributes = test_datamanager.do_select(1).get_attributes()

        assert _attributes["hazard_rate_goal"] == pytest.approx(2.68096515e-05)
        assert _attributes["reliability_goal"] == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_agree_total_elements(self, test_attributes, test_datamanager):
        """should calculate the total number of sub-elements and subsystems."""
        test_datamanager.do_select_all(attributes=test_attributes)

        (
            _n_sub_elements,
            _n_sub_systems,
        ) = test_datamanager._do_calculate_agree_total_elements(1)

        assert _n_sub_elements == 2
        assert _n_sub_systems == 2

    @pytest.mark.unit
    def test_do_calculate_agree_allocation(self, test_attributes, test_datamanager):
        """should apportion the record ID reliability goal using the AGREE method."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _record = test_datamanager.do_select(1)
        _record.allocation_method_id = 2
        _record.reliability_goal = 0.717

        _record = test_datamanager.do_select(2)
        _record.duty_cycle = 90.0
        _record.mission_time = 100.0
        _record.n_sub_subsystems = 6
        _record.n_sub_elements = 2
        _record.weight_factor = 0.95
        test_datamanager._do_calculate_agree_allocation(1)

        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.005836481)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(171.3361074)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.5913878)

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation(self, test_attributes, test_datamanager):
        """should apportion the record ID reliability goal using the ARINC method."""
        test_datamanager.do_select_all(attributes=test_attributes)

        test_datamanager._node_hazard_rate = 0.000628
        test_datamanager._system_hazard_rate = 0.002681

        _record = test_datamanager.do_select(1)
        _record.allocation_method_id = 3
        _record.goal_measure_id = 2
        _record.hazard_rate_goal = 0.000617

        test_datamanager._do_calculate_arinc_allocation(1)

        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.0001445267)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(6919.1382176)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.9856513)

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation(self, test_attributes, test_datamanager):
        """should raise ZeroDivisionError using ARINC method with system h(t)=0.0."""
        test_datamanager.do_select_all(attributes=test_attributes)

        test_datamanager._node_hazard_rate = 0.000628
        test_datamanager._system_hazard_rate = 0.0

        with pytest.raises(ZeroDivisionError):
            test_datamanager._do_calculate_arinc_allocation(1)

    @pytest.mark.unit
    def test_do_calculate_equal_allocation(self, test_attributes, test_datamanager):
        """should apportion the record ID reliability goal using equal allocation."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _record = test_datamanager.do_select(1)
        _record.allocation_method_id = 1
        _record.goal_measure_id = 1
        _record.reliability_goal = 0.995

        test_datamanager._do_calculate_equal_allocation(1)

        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(5.012542e-05)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(19949.9582288)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.995)

    @pytest.mark.unit
    def test_do_calculate_foo_cumulative_weight(
        self, test_attributes, test_datamanager
    ):
        """should apportion the record ID cumulative weight for the FOO method."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _record = test_datamanager.do_select(2)
        _record.env_factor = 6
        _record.soa_factor = 2
        _record.op_time_factor = 9
        _record.int_factor = 3

        _record = test_datamanager.do_select(3)
        _record.env_factor = 3
        _record.soa_factor = 5
        _record.op_time_factor = 10
        _record.int_factor = 4

        _cum_weight = test_datamanager._do_calculate_foo_cumulative_weight(1)

        assert _cum_weight == 924
        assert test_datamanager.tree.get_node(2).data["allocation"].weight_factor == 324
        assert test_datamanager.tree.get_node(3).data["allocation"].weight_factor == 600

    @pytest.mark.unit
    def test_do_calculate_foo_allocation(self, test_attributes, test_datamanager):
        """should apportion the record ID reliability goal using the FOO method."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _record = test_datamanager.do_select(1)
        _record.allocation_method_id = 4
        _record.goal_measure_id = 1
        _record.hazard_rate_goal = 0.000617

        _record = test_datamanager.do_select(2)
        _record.env_factor = 6
        _record.soa_factor = 2
        _record.op_time_factor = 9
        _record.int_factor = 3

        _record = test_datamanager.do_select(3)
        _record.env_factor = 3
        _record.soa_factor = 5
        _record.op_time_factor = 10
        _record.int_factor = 4

        test_datamanager._do_calculate_foo_allocation(1)

        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.0002163506)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(4622.126178)
        assert test_datamanager.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.9785973)
