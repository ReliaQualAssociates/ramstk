# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_allocation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the reliability allocation module."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import Allocation

ATTRIBUTES = {
    'availability_alloc': 0.9998,
    'duty_cycle': 100.0,
    'env_factor': 6,
    'goal_measure_id': 1,
    'hazard_rate_alloc': 0.0,
    'hazard_rate_goal': 0.0,
    'included': 1,
    'int_factor': 3,
    'allocation_method_id': 1,
    'mission_time': 100.0,
    'mtbf_alloc': 0.0,
    'mtbf_goal': 0.0,
    'n_sub_systems': 3,
    'n_sub_elements': 3,
    'parent_id': 1,
    'percent_weight_factor': 0.8,
    'reliability_alloc': 0.99975,
    'reliability_goal': 0.999,
    'op_time_factor': 5,
    'soa_factor': 2,
    'weight_factor': 1
}


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment():
    """_calculate_agree_apportionment() should return a tuple of allocated measures on success."""
    _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
        100.0, 1, 4, 2, 0.999)

    assert _mtbf_alloc == pytest.approx(199899.98332499)
    assert _hazard_rate_alloc == pytest.approx(5.00250167e-06)
    assert _reliability_alloc == pytest.approx(0.99949987)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_zero_sub_elements():
    """_calculate_agree_apportionment() should raise a ZeroDivisionError when passed n_sub_elements=0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the AGREE "
                             "method; one or more inputs had a value of 0.0.  "
                             "Subsystem mission time=100.000000, weight "
                             "factor=1.000000, # of subsystems=4, # of "
                             "subelements=0.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_agree_apportionment(100.0, 1, 4, 0, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_string_input():
    """_calculate_agree_apportionment() should raise a TypeError when passed a string for any input."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            '100.0', 1, 4, 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, '1', 4, 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 1, '4', 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 1, 4, '2', 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 1, 4, 2, '0.999')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_negative_parent_goal():
    """_calculate_agree_apportionment() should raise a ValueError when passed a parent_goal<0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the AGREE "
                             "method; zero or negative value passed for "
                             "parent hardware item's goal.  Parent goal is "
                             "-0.999000.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_agree_apportionment(100.0, 1, 4, 0, -0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment():
    """_calculate_arinc_apportionment() should return a tuple of allocated measures on success."""
    _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
        100.0, 0.025730994152, 0.0000482)

    assert _mtbf_alloc == pytest.approx(806299.50961901)
    assert _hazard_rate_alloc == pytest.approx(1.24023392e-06)
    assert _reliability_alloc == pytest.approx(0.99987598)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment_zero_weight_factor():
    """_calculate_arinc_apportionment() should raise a ZeroDivisionError when passed a weight factor=0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the ARINC "
                             "method; one or more inputs had a value of 0.0. "
                             "Weight factor=0.000000 and parent "
                             "goal=0.000048.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_arinc_apportionment(100.0, 0.0, 0.0000482)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment_zero_parent_goal():
    """_calculate_arinc_apportionment() should raise a ZeroDivisionError when passed a parent goal=0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the ARINC "
                             "method; one or more inputs had a value of 0.0. "
                             "Weight factor=0.025731 and parent "
                             "goal=0.000000.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_arinc_apportionment(100.0, 0.025730994152, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment_string_input():
    """_calculate_arinc_apportionment() should raise a TypeError when passed a string for any argument."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            '100.0', 0.000342, 0.0000482)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, '0.000342', 0.0000482)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, 0.000342, '0.0000482')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_apportionment():
    """_calculate_equal_apportionment() should return a tuple of allocated measures on success."""
    _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
        100.0, 1 / 3, 0.999)

    assert _mtbf_alloc == pytest.approx(299849.9749875)
    assert _hazard_rate_alloc == pytest.approx(0.000003335)
    assert _reliability_alloc == pytest.approx(0.9996665)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_zero_weight_factor():
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed weight factor=0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the equal "
                             "method; one or more inputs had a value of 0.0. "
                             "Mission time=100.000000 and weight "
                             "factor=0.000000.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_equal_apportionment(100.0, 0, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_zero_mission_time():
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed mission_time=0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the equal "
                             "method; one or more inputs had a value of 0.0. "
                             "Mission time=0.000000 and weight "
                             "factor=0.333333.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_equal_apportionment(0.0, 1 / 3, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_zero_goal():
    """_calculate_equal_apportionment() should raise a ValueError if passed a parent goal=0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the equal "
                             "method; a negative or zero value passed for "
                             "parent hardware item's goal.  Parent goal is "
                             "0.000000.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_equal_apportionment(100.0, 1 / 3, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_negative_goal():
    """_calculate_equal_apportionment() should raise a ValueError if passed a parent goal<0.0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the equal "
                             "method; a negative or zero value passed for "
                             "parent hardware item's goal.  Parent goal is "
                             "-0.999950.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_equal_apportionment(100.0, 1 / 3, -0.99995)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_string_input():
    """_calculate_equal_apportionment() should raise a TypeError if passed a string for any input."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            '100.0', 1 / 3, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            100.0, '1/3', 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            100.0, 1 / 3, '0.999')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_foo_apportionment():
    """_calulcate_foo_apportionment() should return a tuple of allocated measures on success."""
    (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc, _weight_factor,
     _percent_weight_factor) = Allocation._calculate_foo_apportionment(
         {
             'intricacy': 4,
             'state_of_art': 6,
             'operating_time': 9,
             'environment': 2
         }, 100.0, 3528, 0.0000482)

    assert _mtbf_alloc == pytest.approx(169432.91839557)
    assert _hazard_rate_alloc == pytest.approx(5.90204082e-06)
    assert _reliability_alloc == pytest.approx(0.99940997)
    assert _weight_factor == pytest.approx(432)
    assert _percent_weight_factor == pytest.approx(0.12244898)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_foo_zero_cum_weight():
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed a cumulative weight=0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the "
                             "Feasibility of Objectives method; one or more "
                             "inputs had a value of 0.0. Intricacy "
                             "factor=4, state of the art factor=6, operating "
                             "time factor=9, environment factor=2, "
                             "cumulative weight=0, parent goal=0.000048.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_foo_apportionment(
        {
            'intricacy': 4,
            'state_of_art': 6,
            'operating_time': 9,
            'environment': 2
        }, 100.0, 0, 0.0000482)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_foo_zero_factor():
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed one or more factors=0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the "
                             "Feasibility of Objectives method; one or more "
                             "inputs had a value of 0.0. Intricacy "
                             "factor=4, state of the art factor=0, operating "
                             "time factor=9, environment factor=2, "
                             "cumulative weight=3528, parent goal=0.000048.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_foo_apportionment(
        {
            'intricacy': 4,
            'state_of_art': 0,
            'operating_time': 9,
            'environment': 2
        }, 100.0, 3528, 0.0000482)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_foo_zero_goal():
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed a parent goal=0."""

    def on_message(error_msg):
        assert error_msg == ("Failed to apportion reliability using the "
                             "Feasibility of Objectives method; one or more "
                             "inputs had a value of 0.0. Intricacy "
                             "factor=4, state of the art factor=6, operating "
                             "time factor=9, environment factor=2, "
                             "cumulative weight=3528, parent goal=0.000000.")

    pub.subscribe(on_message, 'fail_allocate_reliability')

    Allocation._calculate_foo_apportionment(
        {
            'intricacy': 4,
            'state_of_art': 6,
            'operating_time': 9,
            'environment': 2
        }, 100.0, 3528, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_foo_string_input():
    """_calculate_foo_apportionment() should raise a TypeError if passed a string argument."""
    with pytest.raises(TypeError):
        (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc, _weight_factor,
         _percent_weight_factor) = Allocation._calculate_foo_apportionment(
             {
                 'intricacy': 4,
                 'state_of_art': 6,
                 'operating_time': 9,
                 'environment': 2
             }, '100.0', 3528, 0.0000482)

    with pytest.raises(TypeError):
        (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc, _weight_factor,
         _percent_weight_factor) = Allocation._calculate_foo_apportionment(
             {
                 'intricacy': 4,
                 'state_of_art': 6,
                 'operating_time': 9,
                 'environment': 2
             }, 100.0, 3528, '0.0000482')


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("method_id", [1, 2, 3, 4, 5])
def test_do_allocate_reliability(method_id):
    """do_allocate_reliability() should return the Allocation attributes dict with updated values on success."""
    ATTRIBUTES['allocation_method_id'] = method_id
    ATTRIBUTES['system_hr'] = 0.003418
    ATTRIBUTES['hazard_rate'] = 0.00004328
    ATTRIBUTES['mission_time'] = 100.0
    ATTRIBUTES['duty_cycle'] = 90.0
    ATTRIBUTES['n_sub_systems'] = 3
    ATTRIBUTES['n_sub_elements'] = 5

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert attributes['mtbf_alloc'] == pytest.approx({
            1: 51274.34572286,
            2: 1113.48385028,
            3: 299849.97498753,
            4: 3343.51171082,
            5: 0.0
        }[attributes['allocation_method_id']])
        assert attributes['hazard_rate_alloc'] == pytest.approx({
            1: 1.95029305e-05,
            2: 0.00089808218,
            3: 3.33500111e-06,
            4: 0.00029908673,
            5: 0.0
        }[attributes['allocation_method_id']])
        assert attributes['reliability_alloc'] == pytest.approx({
            1: 0.99824628,
            2: 0.91410648,
            3: 0.99966656,
            4: 0.97053417,
            5: 1.0
        }[attributes['allocation_method_id']])

    pub.subscribe(on_message, 'succeed_allocate_reliability')

    if method_id == 1:
        _goal = 0.999
        ATTRIBUTES['weight_factor'] = 0.95
    elif method_id == 2:
        _goal = 0.0058621
        ATTRIBUTES['weight_factor'] = 0.00058621 / 0.0038264
    elif method_id == 3:
        _goal = 0.999
        ATTRIBUTES['weight_factor'] = 1 / 3
    elif method_id == 4:
        _goal = 0.0058621
    elif method_id == 5:
        _goal = 0.99975

    Allocation.do_allocate_reliability(_goal, 3528, **ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("goal_measure_id", [1, 2, 3, 4])
def test_calculate_goals(goal_measure_id):
    """calculate_goals() should return the Allocation attributes dict with updated values on success."""
    ATTRIBUTES['goal_measure_id'] = goal_measure_id
    if goal_measure_id == 1:
        ATTRIBUTES['hazard_rate_goal'] = 0.0
        ATTRIBUTES['mtbf_goal'] = 0.0
        ATTRIBUTES['reliability_goal'] = 0.99975
    elif goal_measure_id == 2:
        ATTRIBUTES['hazard_rate_goal'] = 2.5003126e-06
        ATTRIBUTES['mtbf_goal'] = 0.0
        ATTRIBUTES['reliability_goal'] = 0.0
    elif goal_measure_id == 3:
        ATTRIBUTES['hazard_rate_goal'] = 0.0
        ATTRIBUTES['mtbf_goal'] = 400000
        ATTRIBUTES['reliability_goal'] = 0.0

    _attributes = Allocation.do_calculate_goals(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_goal'] == pytest.approx({
        1: 2.50031255e-06,
        2: 2.5003126e-06,
        3: 2.5e-06,
        4: 0.0
    }[goal_measure_id])
    assert _attributes['mtbf_goal'] == pytest.approx({
        1: 399949.99791645,
        2: 399949.99025322,
        3: 400000.0,
        4: 0.0
    }[goal_measure_id])
    assert _attributes['reliability_goal'] == pytest.approx({
        1: 0.99975,
        2: 0.99975,
        3: 0.99975003,
        4: 1.0
    }[goal_measure_id])


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_negative_reliability():
    """calulate_goals() should raise a ValueError when passed a negative reliability goal."""
    ATTRIBUTES['goal_measure_id'] = 1
    ATTRIBUTES['reliability_goal'] = -0.99975

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate the MTBF and hazard rate "
                             "goals given the reliability goal.  Reliability "
                             "goal=-0.999750.")

    pub.subscribe(on_message, 'fail_calculate_allocation_goal')

    Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_zero_reliability_goal():
    """calulate_goals() should raise a ValueError when passed a reliability goal=0.0."""
    ATTRIBUTES['goal_measure_id'] = 1
    ATTRIBUTES['reliability_goal'] = 0.0

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate the MTBF and hazard rate "
                             "goals given the reliability goal.  Reliability "
                             "goal=0.000000.")

    pub.subscribe(on_message, 'fail_calculate_allocation_goal')

    Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_zero_hazard_rate_goal():
    """calulate_goals() should raise a ZeroDivisionError when passed a hazard rate goal=0.0."""
    ATTRIBUTES['goal_measure_id'] = 2
    ATTRIBUTES['hazard_rate_goal'] = 0.0

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate the MTBF and reliability "
                             "goals given the hazard rate goal.  Hazard rate "
                             "goal=0.000000.")

    pub.subscribe(on_message, 'fail_calculate_allocation_goal')

    Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_zero_mtbf_goal():
    """calulate_goals() should raise a ZeroDivisionError when passed a mtbf goal=0.0."""
    ATTRIBUTES['goal_measure_id'] = 3
    ATTRIBUTES['mtbf_goal'] = 0.0

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate the hazard rate and "
                             "reliability goals given the MTBF goal.  MTBF "
                             "goal=0.000000.")

    pub.subscribe(on_message, 'fail_calculate_allocation_goal')

    Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("method_id", [1, 2, 3, 4])
def test_get_allocation_goal(method_id):
    """get_allocation_goal() should return the proper allocation goal (hazard rate or reliability) on success."""
    ATTRIBUTES['allocation_method_id'] = method_id
    ATTRIBUTES['hazard_rate_goal'] = 0.0058621
    ATTRIBUTES['mtbf_goal'] = 175.0
    ATTRIBUTES['reliability_goal'] = 0.99995

    _goal = Allocation.get_allocation_goal(**ATTRIBUTES)

    assert isinstance(_goal, float)
    assert _goal == {
        1: 0.99995,
        2: 0.0058621,
        3: 0.99995,
        4: 0.0058621
    }[method_id]
