# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.allocation.allocation_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Allocation module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKAllocationRecord
from ramstk.models.dbtables import RAMSTKAllocationTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateAllocationModels:
    """Class for unit testing Allocation model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return an Allocation record model instance."""
        assert isinstance(test_record_model, RAMSTKAllocationRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_allocation"
        assert test_record_model.revision_id == 1
        assert test_record_model.hardware_id == 1
        assert test_record_model.availability_alloc == 0.0
        assert test_record_model.env_factor == 1
        assert test_record_model.goal_measure_id == 1
        assert test_record_model.hazard_rate_alloc == 0.0
        assert test_record_model.hazard_rate_goal == 0.0
        assert test_record_model.included == 1
        assert test_record_model.int_factor == 1
        assert test_record_model.allocation_method_id == 1
        assert test_record_model.mission_time == 100.0
        assert test_record_model.mtbf_alloc == 0.0
        assert test_record_model.mtbf_goal == 0.0
        assert test_record_model.n_sub_systems == 1
        assert test_record_model.n_sub_elements == 1
        assert test_record_model.parent_id == 0
        assert test_record_model.percent_weight_factor == 0.0
        assert test_record_model.reliability_alloc == 1.0
        assert test_record_model.reliability_goal == 0.999
        assert test_record_model.op_time_factor == 1
        assert test_record_model.soa_factor == 1
        assert test_record_model.weight_factor == 1

    @pytest.mark.unit
    def unit_test_table_model_create(self, unit_test_table_model):
        """Return an Allocation table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKAllocationTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._tag == "allocation"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKAllocationRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_allocation_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_allocation_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_allocation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_allocation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_allocation_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_allocation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_allocation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_allocation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_agree_allocation,
            "request_calculate_agree_allocation",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_arinc_allocation,
            "request_calculate_arinc_allocation",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_equal_allocation,
            "request_calculate_equal_allocation",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_foo_allocation,
            "request_calculate_foo_allocation",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_allocation_goals,
            "request_calculate_allocation_goals",
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree,
            "succeed_delete_hardware",
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree,
            "succeed_insert_hardware",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectAllocation(UnitTestSelectMethods):
    """Class for unit testing Allocation table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKAllocationRecord
    _tag = "allocation"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertAllocation(UnitTestInsertMethods):
    """Class for unit testing Allocation table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKAllocationRecord
    _tag = "allocation"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteAllocation(UnitTestDeleteMethods):
    """Class for unit testing Allocation table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKAllocationRecord
    _tag = "allocation"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterAllocation(UnitTestGetterSetterMethods):
    """Class for unit testing Allocation table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]
    _test_attr = "reliability_goal"
    _test_default_value = 1.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["availability_alloc"] == 0.0
        assert _attributes["env_factor"] == 1
        assert _attributes["goal_measure_id"] == 1
        assert _attributes["hazard_rate_alloc"] == 0.0
        assert _attributes["hazard_rate_goal"] == 0.0
        assert _attributes["included"] == 1
        assert _attributes["int_factor"] == 1
        assert _attributes["allocation_method_id"] == 1
        assert _attributes["mission_time"] == 100.0
        assert _attributes["mtbf_alloc"] == 0.0
        assert _attributes["mtbf_goal"] == 0.0
        assert _attributes["n_sub_systems"] == 1
        assert _attributes["n_sub_elements"] == 1
        assert _attributes["parent_id"] == 0
        assert _attributes["percent_weight_factor"] == 0.0
        assert _attributes["reliability_alloc"] == 1.0
        assert _attributes["reliability_goal"] == 0.999
        assert _attributes["op_time_factor"] == 1
        assert _attributes["soa_factor"] == 1
        assert _attributes["weight_factor"] == 1


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestAllocationAnalysisMethods:
    """Class for testing Allocation analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_goals_reliability_specified(
        self, test_attributes, unit_test_table_model
    ):
        """Should calculate h(t) and MTBF goals from a specified R(t) goal."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _allocation = unit_test_table_model.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 1
        _allocation.mission_time = 100.0
        _allocation.reliability_goal = 0.99732259

        unit_test_table_model.do_calculate_allocation_goals(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["hazard_rate_goal"] == pytest.approx(0.00002681)
        assert _attributes["mtbf_goal"] == pytest.approx(37299.5151063)

    @pytest.mark.unit
    def test_do_calculate_goals_hazard_rate_specified(
        self, test_attributes, unit_test_table_model
    ):
        """Should calculate MTBF and R(t) goals from a specified h(t) goal."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _allocation = unit_test_table_model.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 2
        _allocation.mission_time = 100.0
        _allocation.hazard_rate_goal = 0.00002681

        unit_test_table_model.do_calculate_allocation_goals(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["mtbf_goal"] == pytest.approx(37299.5151063)
        assert _attributes["reliability_goal"] == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_goals_mtbf_specified(
        self, test_attributes, unit_test_table_model
    ):
        """Should calculate the h(t) and R(t) goals from a specified MTBF goal."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _allocation = unit_test_table_model.do_select(1)
        _allocation.hardware_id = 1
        _allocation.goal_measure_id = 3
        _allocation.mission_time = 100.0
        _allocation.mtbf_goal = 37300.0

        unit_test_table_model.do_calculate_allocation_goals(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["hazard_rate_goal"] == pytest.approx(2.68096515e-05)
        assert _attributes["reliability_goal"] == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_agree_total_elements(
        self, test_attributes, unit_test_table_model
    ):
        """Should calculate the total number of sub-elements and subsystems."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        (
            _n_sub_elements,
            _n_sub_systems,
        ) = unit_test_table_model._do_calculate_agree_total_elements(1)

        assert _n_sub_elements == 2
        assert _n_sub_systems == 2

    @pytest.mark.unit
    def test_do_calculate_agree_allocation(
        self, test_attributes, unit_test_table_model
    ):
        """Should apportion the record ID reliability goal using the AGREE method."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _record = unit_test_table_model.do_select(1)
        _record.allocation_method_id = 2
        _record.reliability_goal = 0.717

        _record = unit_test_table_model.do_select(2)
        _record.mission_time = 100.0
        _record.n_sub_subsystems = 6
        _record.n_sub_elements = 2
        _record.weight_factor = 0.95
        unit_test_table_model.do_calculate_agree_allocation(1, 90.0)

        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.005836481)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(171.3361074)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.5913878)

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation(
        self, test_attributes, unit_test_table_model
    ):
        """Should apportion the record ID reliability goal using the ARINC method."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model._node_hazard_rate = 0.000628
        unit_test_table_model._system_hazard_rate = 0.002681

        _record = unit_test_table_model.do_select(1)
        _record.allocation_method_id = 3
        _record.goal_measure_id = 2
        _record.hazard_rate_goal = 0.000617

        unit_test_table_model.do_calculate_arinc_allocation(1)

        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.0001445267)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(6919.1382176)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.9856513)

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation_zero_system_rate(
        self, test_attributes, unit_test_table_model
    ):
        """Should raise ZeroDivisionError using ARINC method with system h(t)=0.0."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model._node_hazard_rate = 0.000628
        unit_test_table_model._system_hazard_rate = 0.0

        with pytest.raises(ZeroDivisionError):
            unit_test_table_model.do_calculate_arinc_allocation(1)

    @pytest.mark.unit
    def test_do_calculate_equal_allocation(
        self, test_attributes, unit_test_table_model
    ):
        """Should apportion the record ID reliability goal using equal allocation."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _record = unit_test_table_model.do_select(1)
        _record.allocation_method_id = 1
        _record.goal_measure_id = 1
        _record.reliability_goal = 0.995

        unit_test_table_model.do_calculate_equal_allocation(1)

        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(5.012542e-05)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(19949.9582288)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.995)

    @pytest.mark.unit
    def test_do_calculate_foo_cumulative_weight(
        self, test_attributes, unit_test_table_model
    ):
        """Should apportion the record ID cumulative weight for the FOO method."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _record = unit_test_table_model.do_select(2)
        _record.env_factor = 6
        _record.soa_factor = 2
        _record.op_time_factor = 9
        _record.int_factor = 3

        _record = unit_test_table_model.do_select(3)
        _record.env_factor = 3
        _record.soa_factor = 5
        _record.op_time_factor = 10
        _record.int_factor = 4

        _cum_weight = unit_test_table_model._do_calculate_foo_cumulative_weight(1)

        assert _cum_weight == 924
        assert (
            unit_test_table_model.tree.get_node(2).data["allocation"].weight_factor
            == 324
        )
        assert (
            unit_test_table_model.tree.get_node(3).data["allocation"].weight_factor
            == 600
        )

    @pytest.mark.unit
    def test_do_calculate_foo_allocation(self, test_attributes, unit_test_table_model):
        """Should apportion the record ID reliability goal using the FOO method."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _record = unit_test_table_model.do_select(1)
        _record.allocation_method_id = 4
        _record.goal_measure_id = 1
        _record.hazard_rate_goal = 0.000617

        _record = unit_test_table_model.do_select(2)
        _record.env_factor = 6
        _record.soa_factor = 2
        _record.op_time_factor = 9
        _record.int_factor = 3

        _record = unit_test_table_model.do_select(3)
        _record.env_factor = 3
        _record.soa_factor = 5
        _record.op_time_factor = 10
        _record.int_factor = 4

        unit_test_table_model.do_calculate_foo_allocation(1)

        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].hazard_rate_alloc == pytest.approx(0.0002163506)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].mtbf_alloc == pytest.approx(4622.126178)
        assert unit_test_table_model.tree.get_node(2).data[
            "allocation"
        ].reliability_alloc == pytest.approx(0.9785973)
