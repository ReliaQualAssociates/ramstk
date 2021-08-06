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
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amAllocation, dmAllocation
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
    _allocation_3.parent_id = 2
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
def test_analysismanager(test_toml_user_configuration):
    """Get an analysis manager instance for each test function."""
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
    pub.unsubscribe(dut.do_set_attributes_all, "succeed_calculate_allocation_goals")
    pub.unsubscribe(dut.do_delete, "request_delete_allocation")
    pub.unsubscribe(dut.do_insert, "request_insert_allocation")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a Allocation data manager."""
        assert isinstance(test_datamanager, dmAllocation)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "allocation"
        assert test_datamanager._root == 0
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
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes_all, "succeed_calculate_allocation_goals"
        )
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_allocation")
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_allocation")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_allocation")

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_analysismanager):
        """__init__() should create an instance of the allocation analysis manager."""
        assert isinstance(test_analysismanager, amAllocation)
        assert isinstance(
            test_analysismanager.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration
        )
        assert isinstance(test_analysismanager._attributes, dict)
        assert isinstance(test_analysismanager._tree, Tree)
        assert test_analysismanager._attributes == {}
        assert test_analysismanager._node_hazard_rate == 0.0
        assert test_analysismanager._system_hazard_rate == 0.0
        assert pub.isSubscribed(
            test_analysismanager.on_get_all_attributes,
            "succeed_get_allocation_attributes",
        )
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_get_allocation_tree"
        )
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_update_allocation"
        )
        assert pub.isSubscribed(
            test_analysismanager._do_calculate_allocation,
            "request_allocate_reliability",
        )
        assert pub.isSubscribed(
            test_analysismanager._do_calculate_allocation_goals,
            "request_calculate_allocation_goals",
        )
        assert pub.isSubscribed(
            test_analysismanager._do_calculate_allocation,
            "request_calculate_allocation",
        )
        assert pub.isSubscribed(
            test_analysismanager._on_get_hardware_attributes,
            "succeed_get_all_hardware_attributes",
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """should build a record tree containing RAMSTKAllocation records."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

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
    def test_do_select(self, test_datamanager):
        """should return a RAMSTKAllocation record."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        _allocation = test_datamanager.do_select(1)

        assert isinstance(_allocation, MockRAMSTKAllocation)
        assert _allocation.included == 1
        assert _allocation.parent_id == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """should return None when a non-existent Allocation ID is requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add new record to record tree and update last_id."""
        test_attributes["hardware_id"] = 4
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 4
        assert isinstance(
            test_datamanager.tree.get_node(4).data["allocation"], RAMSTKAllocation
        )
        assert test_datamanager.tree.get_node(4).data["allocation"].revision_id == 1
        assert test_datamanager.tree.get_node(4).data["allocation"].hardware_id == 4
        assert test_datamanager.tree.get_node(4).data["allocation"].parent_id == 1


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        _last_id = test_datamanager.last_id
        test_datamanager.do_delete(node_id=_last_id)

        assert test_datamanager.last_id == 2
        assert test_datamanager.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestAnalysisMethods:
    """Class for allocation methods test suite."""

    @pytest.mark.skip
    def test_do_calculate_goals_reliability_specified(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_goal() should calculate the equivalent h(t) and MTBF goals from
        a specified reliability goal."""
        test_datamanager.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
            }
        )

        test_analysismanager._tree.get_node(1).data["allocation"].hardware_id = 1
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_analysismanager._tree.get_node(1).data["allocation"].mission_time = 100.0
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].reliability_goal = 0.99732259

        test_analysismanager._do_calculate_allocation_goals(
            test_analysismanager._tree.get_node(1)
        )

        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal == pytest.approx(0.00002681)
        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].mtbf_goal == pytest.approx(37299.5151063)

    @pytest.mark.skip
    def test_do_calculate_goals_hazard_rate_specified(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_goal() should calculate the equivalent MTBF and R(t) goals from
        a specified hazard rate goal."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data["allocation"].hardware_id = 1
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 2
        test_analysismanager._tree.get_node(1).data["allocation"].mission_time = 100.0
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.00002681
        test_analysismanager._do_calculate_allocation_goals(
            node=test_analysismanager._tree.get_node(1)
        )

        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].mtbf_goal == pytest.approx(37299.5151063)
        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].reliability_goal == pytest.approx(0.99732259)

    @pytest.mark.skip
    def test_do_calculate_goals_mtbf_specified(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_goal() should calculate the equivalent h(t) and R(t) goals from
        a specified MTBF goal."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data["allocation"].hardware_id = 1
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 3
        test_analysismanager._tree.get_node(1).data["allocation"].mission_time = 100.0
        test_analysismanager._tree.get_node(1).data["allocation"].mtbf_goal = 37300.0
        test_analysismanager._do_calculate_allocation_goals(
            node=test_analysismanager._tree.get_node(1)
        )

        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal == pytest.approx(2.68096515e-05)
        assert test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].reliability_goal == pytest.approx(0.99732259)

    @pytest.mark.skip
    def test_do_calculate_no_allocation_method(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_allocation() should apportion the node ID reliability goal
        using the feasibility of objectives method."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].allocation_method_id = 16
        test_analysismanager._tree.get_node(1).data["allocation"].goal_measure_id = 1
        test_analysismanager._tree.get_node(1).data[
            "allocation"
        ].hazard_rate_goal = 0.000617

        assert test_analysismanager._do_calculate_allocation(1) is None

    @pytest.mark.unit
    def test_on_select_hardware(self, test_analysismanager, test_datamanager):
        """_on_select_hardware() should assign the node hazard rate to the
        _node_hazard_rate attribute."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._on_get_hardware_attributes(
            attributes={
                "revision_id": 1,
                "hazard_rate_active": 0.00032,
                "hardware_id": 2,
            },
        )

        assert test_analysismanager._node_hazard_rate == 0.00032
        assert test_analysismanager._system_hazard_rate == 0.0

    @pytest.mark.unit
    def test_on_select_hardware_system(self, test_analysismanager, test_datamanager):
        """_on_select_hardware() should assign the node and system hazard rate when the
        system node is selected."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        test_analysismanager._on_get_hardware_attributes(
            attributes={
                "revision_id": 1,
                "hazard_rate_active": 0.00032,
                "hardware_id": 1,
            },
        )

        assert test_analysismanager._node_hazard_rate == 0.00032
        assert test_analysismanager._system_hazard_rate == 0.00032

    @pytest.mark.unit
    @pytest.mark.parametrize("method_id", [1, 2, 3, 4])
    def test_do_get_allocation_goal(
        self, test_analysismanager, test_datamanager, method_id
    ):
        """do_calculate_goal() should return the proper allocation goal measure."""
        test_datamanager.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_datamanager.do_get_tree()
        test_datamanager.do_get_attributes(node_id=2, table="allocation")

        test_analysismanager._attributes["allocation_method_id"] = method_id
        test_analysismanager._attributes["hazard_rate_goal"] = 0.00002681
        test_analysismanager._attributes["reliability_goal"] = 0.9995

        _goal = test_analysismanager._do_get_allocation_goal()

        if method_id in [2, 4]:
            assert _goal == 0.00002681
        else:
            assert _goal == 0.9995
