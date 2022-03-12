# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.allocation_integration_test.py is part of The RAMSTK Project
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


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_agree_apportionment_zero_sub_elements(
    test_attributes_allocation,
):
    """_calculate_agree_apportionment() should raise a ZeroDivisionError when passed
    n_sub_elements=0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the AGREE "
            "method; one or more inputs had a value of 0.0.  "
            "Subsystem mission time=100.0, weight "
            "factor=1.0, # of subsystems=4, # of "
            "subelements=0."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1
    test_attributes_allocation["n_sub_systems"] = 4
    test_attributes_allocation["n_sub_elements"] = 0
    allocation._calculate_agree_apportionment(
        0.999,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_agree_apportionment_negative_parent_goal(
    test_attributes_allocation,
):
    """_calculate_agree_apportionment() should raise a ValueError when passed a
    parent_goal<0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the AGREE "
            "method; zero or negative value passed for "
            "parent hardware item's goal.  Parent goal is "
            "-0.999."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1
    test_attributes_allocation["n_sub_systems"] = 4
    test_attributes_allocation["n_sub_elements"] = 2
    allocation._calculate_agree_apportionment(
        -0.999,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_arinc_apportionment_zero_weight_factor(
    test_attributes_allocation,
):
    """_calculate_arinc_apportionment() should raise a ZeroDivisionError when passed a
    weight factor=0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the ARINC "
            "method; one or more inputs had a value of 0.0. "
            "Weight factor=0.0 and parent "
            "goal=4.82e-05."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 0.0
    allocation._calculate_arinc_apportionment(
        0.0000482,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_arinc_apportionment_zero_parent_goal(
    test_attributes_allocation,
):
    """_calculate_arinc_apportionment() should raise a ZeroDivisionError when passed a
    parent goal=0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the ARINC "
            "method; one or more inputs had a value of 0.0. "
            "Weight factor=0.025730994152 and parent "
            "goal=0.0."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 0.025730994152
    allocation._calculate_arinc_apportionment(
        0.0,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_equal_zero_weight_factor(
    test_attributes_allocation,
):
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed
    weight factor=0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the equal "
            "method; one or more inputs had a value of 0.0. "
            "Mission time=100.0 and weight "
            "factor=0.0."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 0.0
    allocation._calculate_equal_apportionment(
        0.999,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_equal_zero_mission_time(
    test_attributes_allocation,
):
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed
    mission_time=0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the equal "
            "method; one or more inputs had a value of 0.0. "
            "Mission time=0.0 and weight "
            "factor=0.3333333333333333."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 0.0
    test_attributes_allocation["weight_factor"] = 1.0 / 3.0
    allocation._calculate_equal_apportionment(
        0.999,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_equal_zero_goal(
    test_attributes_allocation,
):
    """_calculate_equal_apportionment() should raise a ValueError if passed a parent
    goal=0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the equal "
            "method; a negative or zero value passed for "
            "parent hardware item's goal.  Parent goal is "
            "0.0."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1.0 / 3.0
    allocation._calculate_equal_apportionment(
        0.0,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_equal_negative_goal(
    test_attributes_allocation,
):
    """_calculate_equal_apportionment() should raise a ValueError if passed a parent
    goal<0.0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the equal "
            "method; a negative or zero value passed for "
            "parent hardware item's goal.  Parent goal is "
            "-0.99995."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["weight_factor"] = 1.0 / 3.0
    allocation._calculate_equal_apportionment(
        -0.99995,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_foo_zero_cum_weight(
    test_attributes_allocation,
):
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed a
    cumulative weight=0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the "
            "Feasibility of Objectives method; one or more "
            "inputs had a value of 0.0. Intricacy "
            "factor=4, state of the art factor=6, operating "
            "time factor=9, environment factor=2, "
            "cumulative weight=0, parent goal=4.82e-05."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["int_factor"] = 4
    test_attributes_allocation["soa_factor"] = 6
    test_attributes_allocation["op_time_factor"] = 9
    test_attributes_allocation["env_factor"] = 2

    _attributes = allocation._calculate_foo_apportionment(
        0.0000482,
        0,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_foo_zero_factor(
    test_attributes_allocation,
):
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed one or
    more factors=0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the "
            "Feasibility of Objectives method; one or more "
            "inputs had a value of 0.0. Intricacy "
            "factor=4, state of the art factor=0, operating "
            "time factor=9, environment factor=2, "
            "cumulative weight=3528, parent goal=4.82e-05."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["int_factor"] = 4
    test_attributes_allocation["soa_factor"] = 0
    test_attributes_allocation["op_time_factor"] = 9
    test_attributes_allocation["env_factor"] = 2

    _attributes = allocation._calculate_foo_apportionment(
        0.0000482,
        3528,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_foo_zero_goal(
    test_attributes_allocation,
):
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed a
    parent goal=0."""

    def on_message(error_message):
        assert error_message == (
            "Failed to apportion reliability using the "
            "Feasibility of Objectives method; one or more "
            "inputs had a value of 0.0. Intricacy "
            "factor=4, state of the art factor=6, operating "
            "time factor=9, environment factor=2, "
            "cumulative weight=3528, parent goal=0.0."
        )

    pub.subscribe(on_message, "fail_allocate_reliability")

    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["int_factor"] = 4
    test_attributes_allocation["soa_factor"] = 6
    test_attributes_allocation["op_time_factor"] = 9
    test_attributes_allocation["env_factor"] = 2

    _attributes = allocation._calculate_foo_apportionment(
        0.0,
        3528,
        test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
@pytest.mark.parametrize("method_id", [1, 2, 3, 4, 5])
def test_do_allocate_reliability(
    method_id,
    test_attributes_allocation,
):
    """do_allocate_reliability() should return the allocation attributes dict with
    updated values on success."""
    test_attributes_allocation["allocation_method_id"] = method_id
    test_attributes_allocation["system_hr"] = 0.003418
    test_attributes_allocation["hazard_rate"] = 0.00004328
    test_attributes_allocation["mission_time"] = 100.0
    test_attributes_allocation["duty_cycle"] = 90.0
    test_attributes_allocation["n_sub_systems"] = 3
    test_attributes_allocation["n_sub_elements"] = 5
    test_attributes_allocation["int_factor"] = 4
    test_attributes_allocation["soa_factor"] = 6
    test_attributes_allocation["op_time_factor"] = 9
    test_attributes_allocation["env_factor"] = 2
    test_attributes_allocation["weight_factor"] = 1 / 3
    test_attributes_allocation["goal_measure_id"] = 1
    test_attributes_allocation["reliability_goal"] = 0.995

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert attributes["mtbf_alloc"] == pytest.approx(
            {
                2: 51274.34572286,
                3: 1113.48385028,
                1: 299849.97498753,
                4: 169432.91839557,
                5: 0.0,
            }[attributes["allocation_method_id"]]
        )
        assert attributes["hazard_rate_alloc"] == pytest.approx(
            {
                2: 1.95029305e-05,
                3: 0.00089808218,
                1: 3.33500111e-06,
                4: 5.90204082e-06,
                5: 0.0,
            }[attributes["allocation_method_id"]]
        )
        assert attributes["reliability_alloc"] == pytest.approx(
            {2: 0.99824628, 3: 0.91410648, 1: 0.99966656, 4: 0.99940997, 5: 1.0}[
                attributes["allocation_method_id"]
            ]
        )

    pub.subscribe(on_message, "succeed_allocate_reliability")

    if method_id == 1:
        _goal = 0.999
        test_attributes_allocation["weight_factor"] = 1 / 3
    elif method_id == 2:
        _goal = 0.999
        test_attributes_allocation["weight_factor"] = 0.95
    elif method_id == 3:
        _goal = 0.0058621
        test_attributes_allocation["weight_factor"] = 0.00058621 / 0.0038264
    elif method_id == 4:
        _goal = 0.0000482
    elif method_id == 5:
        _goal = 0.99975

    allocation.do_allocate_reliability(
        _goal,
        3528,
        **test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_goals_negative_reliability(
    test_attributes_allocation,
):
    """calulate_goals() should raise a ValueError when passed a negative reliability
    goal."""
    test_attributes_allocation["goal_measure_id"] = 1
    test_attributes_allocation["reliability_goal"] = -0.99975

    def on_message(error_message):
        assert error_message == (
            "Failed to calculate the MTBF and hazard rate "
            "goals given the reliability goal.  Reliability "
            "goal=-0.99975."
        )

    pub.subscribe(on_message, "fail_calculate_allocation_goal")

    allocation.do_calculate_goals(
        **test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_goals_zero_reliability_goal(
    test_attributes_allocation,
):
    """calulate_goals() should raise a ValueError when passed a reliability
    goal=0.0."""
    test_attributes_allocation["goal_measure_id"] = 1
    test_attributes_allocation["reliability_goal"] = 0.0

    def on_message(error_message):
        assert error_message == (
            "Failed to calculate the MTBF and hazard rate "
            "goals given the reliability goal.  Reliability "
            "goal=0.0."
        )

    pub.subscribe(on_message, "fail_calculate_allocation_goal")

    allocation.do_calculate_goals(
        **test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_goals_zero_hazard_rate_goal(
    test_attributes_allocation,
):
    """calulate_goals() should raise a ZeroDivisionError when passed a hazard rate
    goal=0.0."""
    test_attributes_allocation["goal_measure_id"] = 2
    test_attributes_allocation["hazard_rate_goal"] = 0.0

    def on_message(error_message):
        assert error_message == (
            "Failed to calculate the MTBF and reliability "
            "goals given the hazard rate goal.  Hazard rate "
            "goal=0.0."
        )

    pub.subscribe(on_message, "fail_calculate_allocation_goal")

    allocation.do_calculate_goals(
        **test_attributes_allocation,
    )


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes_allocation")
def test_calculate_goals_zero_mtbf_goal(
    test_attributes_allocation,
):
    """calulate_goals() should raise a ZeroDivisionError when passed a mtbf
    goal=0.0."""
    test_attributes_allocation["goal_measure_id"] = 3
    test_attributes_allocation["mtbf_goal"] = 0.0

    def on_message(error_message):
        assert error_message == (
            "Failed to calculate the hazard rate and "
            "reliability goals given the MTBF goal.  MTBF "
            "goal=0.0."
        )

    pub.subscribe(on_message, "fail_calculate_allocation_goal")

    allocation.do_calculate_goals(
        **test_attributes_allocation,
    )
