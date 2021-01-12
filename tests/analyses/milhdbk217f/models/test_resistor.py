# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk271f.models.test_resistor.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import resistor

ATTRIBUTES = {
    'category_id': 3,
    'subcategory_id': 1,
    'environment_active_id': 3,
    'specification_id': 1,
    'family_id': 2,
    'construction_id': 1,
    'type_id': 2,
    'resistance': 22000,
    'n_elements': 3,
    'power_ratio': 0.45,
    'voltage_ratio': 0.86,
    'temperature_active': 37.6,
    'piQ': 2.0,
    'piE': 1.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_get_part_count_lambda_b(subcategory_id, environment_active_id):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['environment_active_id'] = environment_active_id
    _attributes['specification_id'] = 1
    _lambda_b = resistor.get_part_count_lambda_b(_attributes)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == [
            0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016,
            0.025, 0.025, 0.00025, 0.0098, 0.035, 0.36
        ][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 28
    _attributes['environment_active_id'] = 2
    _attributes['specification_id'] = 1
    with pytest.raises(KeyError):
        _attributes = resistor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_specification():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown specification ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['environment_active_id'] = 1
    _attributes['specification_id'] = 24
    with pytest.raises(KeyError):
        _attributes = resistor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active environment ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['environment_active_id'] = 24
    _attributes['specification_id'] = 1
    with pytest.raises(IndexError):
        _attributes = resistor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float value for the parts count base hazard rate on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _lambda_b = resistor.calculate_part_count(**_attributes)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.0071


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 8])
def test_calculate_part_stress_lambda_b(subcategory_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard rate on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['specification_id'] = 1
    _attributes['type_id'] = 1
    _attributes['temperature_active'] = 39.5
    _attributes['power_ratio'] = 0.45
    _attributes = resistor.calculate_part_stress_lambda_b(_attributes)

    assert isinstance(_attributes['lambda_b'], float)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == pytest.approx(0.00059453715)
    elif subcategory_id == 2:
        assert _attributes['lambda_b'] == pytest.approx(0.0083680087)
    elif subcategory_id == 4:
        assert _attributes['lambda_b'] == 6e-05
    elif subcategory_id == 8:
        assert _attributes['lambda_b'] == 0.021


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 4, 6])
def test_get_resistance_factor(subcategory_id):
    """calculate_resistance_factor() should return a float value for piR on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['specification_id'] = 1
    _attributes['family_id'] = 2
    _attributes['resistance'] = 3300
    _attributes = resistor.get_resistance_factor(_attributes)

    assert isinstance(_attributes['piR'], float)
    if subcategory_id == 1:
        assert _attributes['piR'] == 1.1
    elif subcategory_id == 4:
        assert _attributes['piR'] == 0.0
    elif subcategory_id == 6:
        assert _attributes['piR'] == 1.2


@pytest.mark.unit
@pytest.mark.calculation
def test_get_resistance_factor_no_specification():
    """calculate_resistance_factor() should raise an IndexError when passed an unknown specification ID."""
    ATTRIBUTES['subcategory_id'] = 6
    ATTRIBUTES['specification_id'] = 71
    ATTRIBUTES['family_id'] = 2
    ATTRIBUTES['resistance'] = 3300
    with pytest.raises(IndexError):
        _attributes = resistor.get_resistance_factor(ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_resistance_factor_no_family():
    """calculate_resistance_factor() should raise an IndexError when passed an unknown family ID."""
    ATTRIBUTES['subcategory_id'] = 6
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['family_id'] = 21
    ATTRIBUTES['resistance'] = 3300
    with pytest.raises(IndexError):
        _attributes = resistor.get_resistance_factor(ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_resistance_factor_no_subcategory():
    """calculate_resistance_factor() should raise a KeyError when passed an unknown subcategory ID."""
    ATTRIBUTES['subcategory_id'] = 61
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['family_id'] = 2
    ATTRIBUTES['resistance'] = 3300
    with pytest.raises(KeyError):
        _attributes = resistor.get_resistance_factor(ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor():
    """calculate_temperature_factor() should return a tuple of two float values for case temperature and piT on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_active'] = 38.2
    _attributes['power_ratio'] = 0.45
    _attributes = resistor.calculate_temperature_factor(_attributes)

    assert isinstance(_attributes['temperature_case'], float)
    assert isinstance(_attributes['piT'], float)
    assert _attributes['temperature_case'] == 62.95
    assert _attributes['piT'] == pytest.approx(4.653004187)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [9, 13])
def test_get_voltage_factor(subcategory_id):
    """get_voltage_factor() should return a float value for piV on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['voltage_ratio'] = 0.85
    _attributes = resistor.get_voltage_factor(_attributes)

    assert isinstance(_attributes['piV'], float)
    assert _attributes['piV'] == {9: 1.4, 13: 1.05}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_voltage_factor_no_subcategory():
    """get_voltage_factor() should raise a KeyError if passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 71
    _attributes['voltage_ratio'] = 0.85
    with pytest.raises(KeyError):
        _attributes = resistor.get_voltage_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 4, 9, 10])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return the attributes dict with updated values on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes = resistor.calculate_part_stress(**_attributes)

    assert isinstance(_attributes, dict)
    assert _attributes['hazard_rate_active'] == {
        1: 0.001217492244190985,
        4: 0.0016392858777726734,
        9: 4.434316747334665,
        10: 31.262128725050236
    }[subcategory_id]
    if subcategory_id == 10:
        assert _attributes['piTAPS'] == 0.9998460969082653
        assert _attributes['piC'] == 2.0
