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
    'method_id': 1,
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
        100.0, 100.0, 1, 4, 2, 0.999)

    assert _mtbf_alloc == pytest.approx(199899.98332499)
    assert _hazard_rate_alloc == pytest.approx(5.00250167e-06)
    assert _reliability_alloc == pytest.approx(0.99949987)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_zero_sub_elements():
    """_calculate_agree_apportionment() should raise a ZeroDivisionError when passed n_sub_elements=0."""
    with pytest.raises(ZeroDivisionError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, 1, 4, 0, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_string_input():
    """_calculate_agree_apportionment() should raise a TypeError when passed a string for any input."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            '100.0', 100.0, 1, 4, 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, '100.0', 1, 4, 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, '1', 4, 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, 1, '4', 2, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, 1, 4, '2', 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, 1, 4, 2, '0.999')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_agree_apportionment_negative_parent_goal():
    """_calculate_agree_apportionment() should raise a ValueError when passed a parent_goal<0.0."""
    with pytest.raises(ValueError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_agree_apportionment(
            100.0, 100.0, 1, 4, 0, -0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment():
    """_calculate_arinc_apportionment() should return a tuple of allocated measures on success."""
    _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
        100.0, 0.000342, 0.0000482, 0.0000088)

    assert _mtbf_alloc == pytest.approx(806299.50961901)
    assert _hazard_rate_alloc == pytest.approx(1.24023392e-06)
    assert _reliability_alloc == pytest.approx(0.99987598)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment_zero_system_hr():
    """_calculate_arinc_apportionment() should raise a ZeroDivisionError when passed a system hazard rate=0.0."""
    with pytest.raises(ZeroDivisionError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, 0.0, 0.0000482, 0.0000088)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_arinc_apportionment_string_input():
    """_calculate_arinc_apportionment() should raise a TypeError when passed a string for any argument."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            '100.0', 0.000342, 0.0000482, 0.0000088)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, '0.000342', 0.0000482, 0.0000088)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, 0.000342, '0.0000482', 0.0000088)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_arinc_apportionment(
            100.0, 0.000342, 0.0000482, '0.0000088')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_apportionment():
    """_calculate_equal_apportionment() should return a tuple of allocated measures on success."""
    _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
        100.0, 3, 0.999)

    assert _mtbf_alloc == pytest.approx(299849.9749875)
    assert _hazard_rate_alloc == pytest.approx(0.000003335)
    assert _reliability_alloc == pytest.approx(0.9996665)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_zero_children():
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed n_children=0."""
    with pytest.raises(ZeroDivisionError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            100.0, 0, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_zero_mission_time():
    """_calculate_equal_apportionment() should raise a ZeroDivisionError if passed mission_time=0.0."""
    with pytest.raises(ZeroDivisionError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            0.0, 3, 0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_negative_goal():
    """_calculate_equal_apportionment() should raise a TypeError if passed a negative value for the parent goal."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            100.0, 3, -0.999)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_equal_string_input():
    """_calculate_equal_apportionment() should raise a TypeError if passed a string for any input."""
    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            '100.0', 3, 0.999)

    with pytest.raises(TypeError):
        _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc = Allocation._calculate_equal_apportionment(
            100.0, 3, '0.999')


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
def test_calculate_equal_zero_cum_weight():
    """_calculate_foo_apportionment() should raise a ZeroDivisionError if passed a cumulative weight=0."""
    with pytest.raises(ZeroDivisionError):
        (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc, _weight_factor,
         _percent_weight_factor) = Allocation._calculate_foo_apportionment(
             {
                 'intricacy': 4,
                 'state_of_art': 6,
                 'operating_time': 9,
                 'environment': 2
             }, 100.0, 0, 0.0000482)


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
@pytest.mark.parametrize("method_id", [1, 2, 3, 4])
def test_calculate_allocation(method_id):
    """calculate_allocation() should return the Allocation attributes dict with updated values on success."""
    ATTRIBUTES['method_id'] = method_id
    ATTRIBUTES['system_hr'] = 0.003418
    ATTRIBUTES['hazard_rate'] = 0.00004328
    _attributes = Allocation.do_calculate_allocation(0.999, 3528, **ATTRIBUTES)

    assert isinstance(_attributes, dict)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("goal_measure_id", [1, 2, 3])
def test_calculate_goals(goal_measure_id):
    """calculate_goals() should return the Allocation attributes dict with updated values on success."""
    ATTRIBUTES['goal_measure_id'] = goal_measure_id
    if goal_measure_id == 1:
        ATTRIBUTES['reliability_goal'] = 0.99975
    elif goal_measure_id == 2:
        ATTRIBUTES['hazard_rate_goal'] = 2.5003126e-06
    elif goal_measure_id == 3:
        ATTRIBUTES['mtbf_goal'] = 400000
    _attributes = Allocation.do_calculate_goals(**ATTRIBUTES)

    assert isinstance(_attributes, dict)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_negative_reliability():
    """calulate_goals() should raise a ValueError when passed a negative reliability goal."""
    ATTRIBUTES['goal_measure_id'] = 1
    ATTRIBUTES['reliability_goal'] = -0.99975
    with pytest.raises(ValueError):
        _attributes = Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_zero_hazard_rate_goal():
    """calulate_goals() should raise a ZeroDivisionError when passed a hazard rate goal=0.0."""
    ATTRIBUTES['goal_measure_id'] = 2
    ATTRIBUTES['hazard_rate_goal'] = 0.0
    with pytest.raises(ZeroDivisionError):
        _attributes = Allocation.do_calculate_goals(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_goals_zero_mtbf_goal():
    """calulate_goals() should raise a ZeroDivisionError when passed a mtbf goal=0.0."""
    ATTRIBUTES['goal_measure_id'] = 3
    ATTRIBUTES['mtbf_goal'] = 0.0
    with pytest.raises(ZeroDivisionError):
        _attributes = Allocation.do_calculate_goals(**ATTRIBUTES)
