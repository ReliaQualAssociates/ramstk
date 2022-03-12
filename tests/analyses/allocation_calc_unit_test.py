# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.allocation_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the reliability allocation module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import allocation


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_agree_apportionment(
    test_attributes_allocation,
):
    """_calculate_agree_apportionment() should return a tuple of allocated measures on
    success."""
    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1
    test_attributes_allocation["n_sub_systems"] = 4
    test_attributes_allocation["n_sub_elements"] = 2
    test_attributes_allocation = allocation._calculate_agree_apportionment(
        0.999,
        test_attributes_allocation,
    )

    assert test_attributes_allocation["mtbf_alloc"] == pytest.approx(199899.98332499)
    assert test_attributes_allocation["hazard_rate_alloc"] == pytest.approx(
        5.00250167e-06
    )
    assert test_attributes_allocation["reliability_alloc"] == pytest.approx(0.99949987)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_arinc_apportionment(
    test_attributes_allocation,
):
    """_calculate_arinc_apportionment() should return a tuple of allocated measures on
    success."""
    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 0.025730994152
    test_attributes_allocation = allocation._calculate_arinc_apportionment(
        0.0000482,
        test_attributes_allocation,
    )

    assert test_attributes_allocation["mtbf_alloc"] == pytest.approx(806299.50961901)
    assert test_attributes_allocation["hazard_rate_alloc"] == pytest.approx(
        1.24023392e-06
    )
    assert test_attributes_allocation["reliability_alloc"] == pytest.approx(0.99987598)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_equal_apportionment(
    test_attributes_allocation,
):
    """_calculate_equal_apportionment() should return a tuple of allocated measures on
    success."""
    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1.0 / 3.0
    test_attributes_allocation = allocation._calculate_equal_apportionment(
        0.999,
        test_attributes_allocation,
    )

    assert test_attributes_allocation["mtbf_alloc"] == pytest.approx(299849.9749875)
    assert test_attributes_allocation["hazard_rate_alloc"] == pytest.approx(0.000003335)
    assert test_attributes_allocation["reliability_alloc"] == pytest.approx(0.9996665)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_foo_apportionment(
    test_attributes_allocation,
):
    """_calulcate_foo_apportionment() should return a tuple of allocated measures on
    success."""
    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["int_factor"] = 4
    test_attributes_allocation["soa_factor"] = 6
    test_attributes_allocation["op_time_factor"] = 9
    test_attributes_allocation["env_factor"] = 2

    test_attributes_allocation = allocation._calculate_foo_apportionment(
        0.0000482,
        3528,
        test_attributes_allocation,
    )

    assert test_attributes_allocation["weight_factor"] == pytest.approx(432)
    assert test_attributes_allocation["percent_weight_factor"] == pytest.approx(
        0.12244898
    )
    assert test_attributes_allocation["mtbf_alloc"] == pytest.approx(169432.91839557)
    assert test_attributes_allocation["hazard_rate_alloc"] == pytest.approx(
        5.90204082e-06
    )
    assert test_attributes_allocation["reliability_alloc"] == pytest.approx(0.99940997)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_foo_string_input(
    test_attributes_allocation,
):
    """_calculate_foo_apportionment() should raise a TypeError if passed a string
    argument."""
    with pytest.raises(TypeError):
        test_attributes_allocation["mission_time"] = 100.0
        test_attributes_allocation["int_factor"] = 4
        test_attributes_allocation["soa_factor"] = 6
        test_attributes_allocation["op_time_factor"] = 9
        test_attributes_allocation["env_factor"] = 2

        test_attributes_allocation = allocation._calculate_foo_apportionment(
            "0.0000482",
            3528,
            test_attributes_allocation,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
@pytest.mark.parametrize("goal_measure_id", [1, 2, 3, 4])
def test_calculate_goals(
    goal_measure_id,
    test_attributes_allocation,
):
    """calculate_goals() should return the allocation attributes dict with updated
    values on success."""
    test_attributes_allocation["goal_measure_id"] = goal_measure_id
    if goal_measure_id == 1:
        test_attributes_allocation["hazard_rate_goal"] = 0.0
        test_attributes_allocation["mtbf_goal"] = 0.0
        test_attributes_allocation["reliability_goal"] = 0.99975
    elif goal_measure_id == 2:
        test_attributes_allocation["hazard_rate_goal"] = 2.5003126e-06
        test_attributes_allocation["mtbf_goal"] = 0.0
        test_attributes_allocation["reliability_goal"] = 0.0
    elif goal_measure_id == 3:
        test_attributes_allocation["hazard_rate_goal"] = 0.0
        test_attributes_allocation["mtbf_goal"] = 400000
        test_attributes_allocation["reliability_goal"] = 0.0

    test_attributes_allocation = allocation.do_calculate_goals(
        **test_attributes_allocation,
    )

    assert isinstance(test_attributes_allocation, dict)
    assert test_attributes_allocation["hazard_rate_goal"] == pytest.approx(
        {1: 2.50031255e-06, 2: 2.5003126e-06, 3: 2.5e-06, 4: 0.0}[goal_measure_id]
    )
    assert test_attributes_allocation["mtbf_goal"] == pytest.approx(
        {1: 399949.99791645, 2: 399949.99025322, 3: 400000.0, 4: 0.0}[goal_measure_id]
    )
    assert test_attributes_allocation["reliability_goal"] == pytest.approx(
        {1: 0.99975, 2: 0.99975, 3: 0.99975003, 4: 1.0}[goal_measure_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_allocation")
@pytest.mark.parametrize("method_id", [1, 2, 3, 4])
def test_get_allocation_goal(
    method_id,
    test_attributes_allocation,
):
    """get_allocation_goal() should return the proper allocation goal (hazard rate or
    reliability) on success."""
    test_attributes_allocation["allocation_method_id"] = method_id
    test_attributes_allocation["hazard_rate_goal"] = 0.0058621
    test_attributes_allocation["mtbf_goal"] = 175.0
    test_attributes_allocation["reliability_goal"] = 0.99995

    _goal = allocation.get_allocation_goal(
        **test_attributes_allocation,
    )

    assert isinstance(_goal, float)
    assert _goal == {1: 0.99995, 2: 0.0058621, 3: 0.99995, 4: 0.0058621}[method_id]
