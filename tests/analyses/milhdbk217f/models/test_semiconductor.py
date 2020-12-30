# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_semiconductor.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import semiconductor

ATTRIBUTES = {
    'category_id': 2,
    'subcategory_id': 1,
    'environment_active_id': 3,
    'type_id': 1,
    'quality_id': 1,
    'application_id': 1,
    'package_id': 2,
    'construction_id': 1,
    'matching_id': 2,
    'duty_cycle': 65.0,
    'voltage_ratio': 0.45,
    'temperature_case': 38.2,
    'theta_jc': 15.0,
    'power_operating': 0.5,
    'frequency_operating': 2.5,
    'n_elements': 8,
    'power_rated': 1.0,
    'current_rated': 0.25,
    'current_operating': 0.038,
    'power_ratio': 0.28,
    'piE': 1.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 5])
def test_get_part_count_quality_factor(subcategory_id, type_id):
    """get_part_count_quality_factor() should return a float value for piQ on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['quality_id'] = 3
    _attributes['type_id'] = type_id
    _attributes = semiconductor.get_part_count_quality_factor(_attributes)

    assert isinstance(_attributes['piQ'], float)
    if subcategory_id == 1:
        assert _attributes['piQ'] == 2.4
    elif subcategory_id == 2 and type_id == 1:
        assert _attributes['piQ'] == 5.0
    elif subcategory_id == 2 and type_id == 5:
        assert _attributes['piQ'] == 1.8


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_quality_factor_no_quality():
    """get_part_count_quality_factor() should raise an IndexError when passed an unknown quality ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['quality_id'] = 33
    _attributes['type_id'] = 1
    with pytest.raises(IndexError):
        _attributes = semiconductor.get_part_count_quality_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_quality_factor_no_subcategory():
    """get_part_count_quality_factor() should raise a KeyError when passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 21
    _attributes['quality_id'] = 1
    _attributes['type_id'] = 1
    with pytest.raises(KeyError):
        _attributes = semiconductor.get_part_count_quality_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 4])
def test_get_part_count_lambda_b(subcategory_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['environment_active_id'] = 3
    _attributes['type_id'] = 1
    _lambda_b = semiconductor.get_part_count_lambda_b(_attributes)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.049, 4: 0.16}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active environment ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 1
    _attributes['environment_active_id'] = 32
    _attributes['type_id'] = 1
    with pytest.raises(IndexError):
        _lambda_b = semiconductor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 47
    _attributes['environment_active_id'] = 3
    _attributes['type_id'] = 1
    with pytest.raises(KeyError):
        _lambda_b = semiconductor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown type ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 1
    _attributes['environment_active_id'] = 3
    _attributes['type_id'] = 31
    with pytest.raises(KeyError):
        _lambda_b = semiconductor.get_part_count_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 4])
@pytest.mark.parametrize("type_id", [1, 5])
def test_calculate_part_count(subcategory_id, type_id):
    """calculate_part_count() should return the semiconductor attributes dict with updated values."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['type_id'] = type_id
    _attributes = semiconductor.calculate_part_count(**_attributes)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1 and type_id == 1:
        assert _attributes['lambda_b'] == 0.049
    elif subcategory_id == 1 and type_id == 5:
        assert _attributes['lambda_b'] == 0.04
    elif subcategory_id == 2 and type_id == 1:
        assert _attributes['lambda_b'] == 8.9
    elif subcategory_id == 2 and type_id == 5:
        assert _attributes['lambda_b'] == 0.31
    elif subcategory_id == 4:
        assert _attributes['lambda_b'] == 0.16


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_stress_quality_factor(subcategory_id):
    """get_part_stress_quality_factor() should return a float value for piQ on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['quality_id'] = 3
    _attributes['type_id'] = 1
    _attributes = semiconductor.get_part_stress_quality_factor(_attributes)

    assert isinstance(_attributes['piQ'], float)
    assert _attributes['piQ'] == {1: 2.4, 2: 5.0}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_quality():
    """get_part_stress_quality_factor() should raise an IndexError when passed an unknown quality ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['quality_id'] = 31
    _attributes['type_id'] = 1
    with pytest.raises(IndexError):
        _attributes = semiconductor.get_part_stress_quality_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_subcategory():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 21
    _attributes['quality_id'] = 1
    _attributes['type_id'] = 1
    with pytest.raises(KeyError):
        _attributes = semiconductor.get_part_stress_quality_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_type():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown type ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['quality_id'] = 1
    _attributes['type_id'] = 21
    with pytest.raises(KeyError):
        _attributes = semiconductor.get_part_stress_quality_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 7, 8, 12])
@pytest.mark.parametrize("frequency_operating", [0.5, 5.0])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_part_stress_lambda_b(subcategory_id, frequency_operating,
                                        application_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard rate on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['application_id'] = application_id
    _attributes['type_id'] = 1
    _attributes['frequency_operating'] = frequency_operating
    _attributes['power_operating'] = 0.05
    _attributes['n_elements'] = 8
    _attributes = semiconductor.calculate_part_stress_lambda_b(_attributes)

    assert isinstance(_attributes['lambda_b'], float)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == 0.0038
    elif subcategory_id == 3:
        assert _attributes['lambda_b'] == 0.00074
    elif subcategory_id == 7 and frequency_operating == 0.5:
        assert _attributes['lambda_b'] == pytest.approx(0.038206853)
    elif subcategory_id == 8 and frequency_operating == 0.5:
        assert _attributes['lambda_b'] == pytest.approx(0.011808438)
    elif subcategory_id == 8 and frequency_operating == 5.0:
        assert _attributes['lambda_b'] == 0.052
    elif subcategory_id == 12 and application_id == 1:
        assert _attributes['lambda_b'] == 0.003483
    elif subcategory_id == 12 and application_id == 2:
        assert _attributes['lambda_b'] == 0.00344


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_type():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown type ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 1
    _attributes['application_id'] = 1
    _attributes['type_id'] = 11
    _attributes['frequency_operating'] = 1.5
    _attributes['power_operating'] = 0.05
    _attributes['n_elements'] = 8
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_part_stress_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_subcategory():
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2300
    _attributes['application_id'] = 1
    _attributes['type_id'] = 1
    _attributes['frequency_operating'] = 1.5
    _attributes['power_operating'] = 0.05
    _attributes['n_elements'] = 8
    with pytest.raises(KeyError):
        _attributes = semiconductor.calculate_part_stress_lambda_b(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature():
    """calculate_junction_temperature() should return a float value for the junction temperature on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_case'] = 38.2
    _attributes['environment_active_id'] = 1
    _attributes['package_id'] = 2
    _attributes['theta_jc'] = 105.0
    _attributes['power_operating'] = 0.05
    _attributes = semiconductor.calculate_junction_temperature(_attributes)

    assert isinstance(_attributes['temperature_junction'], float)
    assert _attributes['temperature_junction'] == 43.45


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_case_temp():
    """calculate_junction_temperature() should return a float value for the case temperature and the junction temperature when passed a case temperature <=0.0."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_case'] = -38.2
    _attributes['environment_active_id'] = 1
    _attributes['package_id'] = 2
    _attributes['theta_jc'] = 105.0
    _attributes['power_operating'] = 0.05
    _attributes = semiconductor.calculate_junction_temperature(_attributes)

    assert isinstance(_attributes['temperature_case'], float)
    assert isinstance(_attributes['temperature_junction'], float)
    assert _attributes['temperature_case'] == 35.0
    assert _attributes['temperature_junction'] == 40.25


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_theta_jc():
    """calculate_junction_temperature() should return a float value for the thetaJC and the junction temperature when passed a theta_jc <=0.0."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_case'] = 38.2
    _attributes['environment_active_id'] = 1
    _attributes['package_id'] = 2
    _attributes['theta_jc'] = 0.0
    _attributes['power_operating'] = 0.05
    _attributes = semiconductor.calculate_junction_temperature(_attributes)

    assert isinstance(_attributes['theta_jc'], float)
    assert isinstance(_attributes['temperature_junction'], float)
    assert _attributes['theta_jc'] == 10.0
    assert _attributes['temperature_junction'] == 38.7


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_case_temp_no_environment():
    """calculate_junction_temperature() should raise an IndexError when passed a case temperature <=0.0 and an unknown active environment_id."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_case'] = 0.0
    _attributes['environment_active_id'] = 31
    _attributes['package_id'] = 1
    _attributes['theta_jc'] = 105.0
    _attributes['power_operating'] = 0.05
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_junction_temperature(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_theta_jc_no_package():
    """calculate_junction_temperature() should raise an IndexError when passed a theta_jc <=0.0 and an unknown package ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['temperature_case'] = 38.2
    _attributes['environment_active_id'] = 1
    _attributes['package_id'] = 128
    _attributes['theta_jc'] = -10.0
    _attributes['power_operating'] = 0.05
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_junction_temperature(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 7])
@pytest.mark.parametrize("voltage_ratio", [0.4, 0.8])
def test_calculate_temperature_factor(subcategory_id, voltage_ratio):
    """calculate_temperature_factor() should return a float value for piT on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['type_id'] = 1
    _attributes['voltage_ratio'] = voltage_ratio
    _attributes['temperature_junction'] = 52.8
    _attributes = semiconductor.calculate_temperature_factor(_attributes)

    assert isinstance(_attributes['piT'], float)
    if subcategory_id == 1:
        assert _attributes['piT'] == pytest.approx(2.42314826)
    elif subcategory_id == 3:
        assert _attributes['piT'] == pytest.approx(1.83183169)
    elif subcategory_id == 7 and voltage_ratio == 0.4:
        assert _attributes['piT'] == pytest.approx(0.229615567)
    elif subcategory_id == 7 and voltage_ratio == 0.8:
        assert _attributes['piT'] == pytest.approx(2.06654010)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_subcategory():
    """calculate_temperature_factor() should raise a KeyError if passed an unknown subcategory ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 27
    _attributes['type_id'] = 1
    _attributes['voltage_ratio'] = 0.5
    _attributes['temperature_junction'] = 52.8
    with pytest.raises(KeyError):
        _attributes = semiconductor.calculate_temperature_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_type():
    """calculate_temperature_factor() should raise an IndexError if passed an unknown type ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['type_id'] = 17
    _attributes['voltage_ratio'] = 0.5
    _attributes['temperature_junction'] = 52.8
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_temperature_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 7, 13])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_application_factor(subcategory_id, application_id):
    """calculate_application_factor() should return a float value on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['application_id'] = application_id
    _attributes['duty_cycle'] = 65.0
    _attributes = semiconductor.calculate_application_factor(_attributes)

    assert isinstance(_attributes['piA'], float)
    if subcategory_id == 1:
        assert _attributes['piA'] == 0.0
    elif subcategory_id == 2 and application_id == 1:
        assert _attributes['piA'] == 0.5
    elif subcategory_id == 2 and application_id == 2:
        assert _attributes['piA'] == 2.5
    elif subcategory_id == 7 and application_id == 1:
        assert _attributes['piA'] == 7.6
    elif subcategory_id == 7 and application_id == 2:
        assert _attributes['piA'] == 0.439
    elif subcategory_id == 13 and application_id == 1:
        assert _attributes['piA'] == 4.4
    elif subcategory_id == 13 and application_id == 2:
        assert _attributes['piA'] == pytest.approx(0.80622577)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_application_factor_no_application():
    """calculate_application_factor() should raise an IndexError when passed an unknown application ID."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 3
    _attributes['application_id'] = 11
    _attributes['duty_cycle'] = 65.0
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_application_factor_negative_duty_cycle():
    """calculate_application_factor() should raise a ValueError when passed a negative value for the duty cycle."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 13
    _attributes['application_id'] = 2
    _attributes['duty_cycle'] = -65.0
    with pytest.raises(ValueError):
        _attributes = semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 4])
@pytest.mark.parametrize("power_rated", [0.075, 10.0])
def test_calculate_power_rating_factor(subcategory_id, type_id, power_rated):
    """calculate_power_rating_factor() should return a float value for piR on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['type_id'] = type_id
    _attributes['power_rated'] = power_rated
    _attributes['current_rated'] = 0.125
    _attributes = semiconductor.calculate_power_rating_factor(_attributes)

    assert isinstance(_attributes['piR'], float)
    if subcategory_id == 2 and type_id == 1:
        assert _attributes['piR'] == 1.0
    elif subcategory_id == 2 and type_id == 4 and power_rated == 10.0:
        assert _attributes['piR'] == pytest.approx(0.50064274)
    elif subcategory_id == 3 and power_rated == 0.075:
        assert _attributes['piR'] == 0.43
    elif subcategory_id == 3 and power_rated == 10.0:
        assert _attributes['piR'] == pytest.approx(2.34422882)
    elif subcategory_id == 10:
        assert _attributes['piR'] == pytest.approx(0.435275282)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_power_rating_factor_negative_input():
    """calculate_power_rating_factor() should raise a ValueError when passed a negative value for rated power."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = 2
    _attributes['type_id'] = 4
    _attributes['power_rated'] = -10.0
    _attributes['current_rated'] = 0.125
    with pytest.raises(ValueError):
        _attributes = semiconductor.calculate_power_rating_factor(_attributes)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 6])
@pytest.mark.parametrize("voltage_ratio", [0.25, 0.75])
def test_calculate_electrical_stress_factor(subcategory_id, type_id,
                                            voltage_ratio):
    """calculate_electrical_stress_factor() should return a float value on success."""
    _attributes = copy.deepcopy(ATTRIBUTES)
    _attributes['subcategory_id'] = subcategory_id
    _attributes['type_id'] = type_id
    _attributes['voltage_ratio'] = voltage_ratio
    _attributes = semiconductor.calculate_electrical_stress_factor(_attributes)

    assert isinstance(_attributes['piS'], float)
    if subcategory_id == 1 and type_id == 6:
        assert _attributes['piS'] == 1.0
    elif subcategory_id == 1 and voltage_ratio == 0.25:
        assert _attributes['piS'] == 0.054
    elif subcategory_id == 1 and voltage_ratio == 0.75:
        assert _attributes['piS'] == pytest.approx(0.49704862)
    elif subcategory_id == 3 and voltage_ratio == 0.25:
        assert _attributes['piS'] == pytest.approx(0.097676646)
    elif subcategory_id == 10 and voltage_ratio == 0.25:
        assert _attributes['piS'] == 0.1
    elif subcategory_id == 10 and voltage_ratio == 0.75:
        assert _attributes['piS'] == pytest.approx(0.57891713)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 6, 7, 13])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return the semiconductor attributes dict with updated values on success."""
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['type_id'] = 1
    _attributes = semiconductor.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == 0.0038
        assert _attributes['temperature_junction'] == 45.7
        assert _attributes['piC'] == 1.0
        assert _attributes['piQ'] == 0.7
        assert _attributes['piS'] == pytest.approx(0.14365026)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0007495062)
    elif subcategory_id == 2:
        assert _attributes['piA'] == 0.5
        assert _attributes['piR'] == 1.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.1730863)
    elif subcategory_id == 6:
        assert _attributes['piR'] == 1.0
        assert _attributes['piS'] == pytest.approx(0.18157386)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.02590612)
    elif subcategory_id == 7:
        assert _attributes['piM'] == 2.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.2225089)
    elif subcategory_id == 13:
        assert _attributes['piI'] == pytest.approx(0.10820637)
        assert _attributes['piP'] == pytest.approx(0.69444444)
        assert _attributes['hazard_rate_active'] == pytest.approx(2.9328130)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_no_construction():
    """calculate_part_stress() should raise an IndexError if passed an unknown construction ID."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['construction_id'] = 5
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_part_stress(**ATTRIBUTES)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_no_matching():
    """calculate_part_stress() should raise an IndexError if passed an unknown matching ID."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['matching_id'] = 6
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_part_stress(**ATTRIBUTES)
