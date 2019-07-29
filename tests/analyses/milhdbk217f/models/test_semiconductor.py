# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_semiconductor.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor module."""

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
    _pi_q = semiconductor.get_part_count_quality_factor(
        subcategory_id, 3, type_id)

    assert isinstance(_pi_q, float)
    if subcategory_id == 1:
        assert _pi_q == 2.4
    elif subcategory_id == 2 and type_id == 1:
        assert _pi_q == 5.0
    elif subcategory_id == 2 and type_id == 5:
        assert _pi_q == 1.8


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_quality_factor_no_quality():
    """get_part_count_quality_factor() should raise an IndexError when passed an unknown quality ID."""
    with pytest.raises(IndexError):
        _pi_q = semiconductor.get_part_count_quality_factor(2, 31, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_quality_factor_no_subcategory():
    """get_part_count_quality_factor() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _pi_q = semiconductor.get_part_count_quality_factor(21, 1, 1)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 4])
def test_get_part_count_lambda_b(subcategory_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = semiconductor.get_part_count_lambda_b(subcategory_id, 3, 1)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.049, 4: 0.16}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = semiconductor.get_part_count_lambda_b(1, 32, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = semiconductor.get_part_count_lambda_b(47, 3, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = semiconductor.get_part_count_lambda_b(1, 2, 31)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 4])
@pytest.mark.parametrize("type_id", [1, 5])
def test_calculate_part_count(subcategory_id, type_id):
    """calculate_part_count() should return the semiconductor attributes dict with updated values."""
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['type_id'] = type_id
    _attributes = semiconductor.calculate_part_count(**ATTRIBUTES)

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
    _pi_q = semiconductor.get_part_stress_quality_factor(subcategory_id, 3, 1)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 2.4, 2: 5.0}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_quality():
    """get_part_stress_quality_factor() should raise an IndexError when passed an unknown quality ID."""
    with pytest.raises(IndexError):
        _pi_q = semiconductor.get_part_stress_quality_factor(2, 31, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_subcategory():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _pi_q = semiconductor.get_part_stress_quality_factor(21, 1, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_quality_factor_no_type():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _pi_q = semiconductor.get_part_stress_quality_factor(2, 1, 21)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 7, 8, 12])
@pytest.mark.parametrize("frequency_operating", [0.5, 5.0])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_part_stress_lambda_b(subcategory_id, frequency_operating,
                                        application_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = semiconductor.calculate_part_stress_lambda_b(
        subcategory_id, frequency_operating, 0.05, application_id, 8, 1)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == 0.0038
    elif subcategory_id == 3:
        assert _lambda_b == 0.00074
    elif subcategory_id == 7 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.038206853)
    elif subcategory_id == 8 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.011808438)
    elif subcategory_id == 8 and frequency_operating == 5.0:
        assert _lambda_b == 0.052
    elif subcategory_id == 12 and application_id == 1:
        assert _lambda_b == 0.003483
    elif subcategory_id == 12 and application_id == 2:
        assert _lambda_b == 0.00344


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_type():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown type ID."""
    with pytest.raises(IndexError):
        _lambda_b = semiconductor.calculate_part_stress_lambda_b(
            1, 1.5, 0.05, 1, 8, 11)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_subcategory():
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = semiconductor.calculate_part_stress_lambda_b(
            2300, 1.5, 0.05, 1, 8, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature():
    """calculate_junction_temperature() should return a float value for the junction temperature on success."""
    __, __, _temperature_junction = semiconductor.calculate_junction_temperature(
        38.2, 1, 105.0, 2, 0.05)

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 43.45


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_case_temp():
    """calculate_junction_temperature() should return a float value for the case temperature and the junction temperature when passed a case temperature <=0.0."""
    _temperature_case, __, _temperature_junction = semiconductor.calculate_junction_temperature(
        -38.2, 1, 105.0, 2, 0.05)

    assert isinstance(_temperature_case, float)
    assert isinstance(_temperature_junction, float)
    assert _temperature_case == 35.0
    assert _temperature_junction == 40.25


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_theta_jc():
    """calculate_junction_temperature() should return a float value for the thetaJC and the junction temperature when passed a theta_jc <=0.0."""
    __, _theta_jc, _temperature_junction = semiconductor.calculate_junction_temperature(
        38.2, 1, 0.0, 2, 0.05)

    assert isinstance(_theta_jc, float)
    assert isinstance(_temperature_junction, float)
    assert _theta_jc == 10.0
    assert _temperature_junction == 38.7


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_case_temp_no_environment():
    """calculate_junction_temperature() should raise an IndexError when passed a case temperature <=0.0 and an unknown active environment_id."""
    with pytest.raises(IndexError):
        _temperature_case, __, _temperature_junction = semiconductor.calculate_junction_temperature(
            0.0, 31, 105.0, 2, 0.05)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature_zero_theta_jc_no_package():
    """calculate_junction_temperature() should raise an IndexError when passed a theta_jc <=0.0 and an unknown package ID."""
    with pytest.raises(IndexError):
        __, _theta_jc, _temperature_junction = semiconductor.calculate_junction_temperature(
            38.2, 1, -10.0, 128, 0.05)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 7])
@pytest.mark.parametrize("voltage_ratio", [0.4, 0.8])
def test_calculate_temperature_factor(subcategory_id, voltage_ratio):
    """calculate_temperature_factor() should return a float value for piT on success."""
    _pi_t = semiconductor.calculate_temperature_factor(subcategory_id, 1,
                                                       voltage_ratio, 52.8)

    assert isinstance(_pi_t, float)
    if subcategory_id == 1:
        assert _pi_t == pytest.approx(2.42314826)
    elif subcategory_id == 3:
        assert _pi_t == pytest.approx(1.83183169)
    elif subcategory_id == 7 and voltage_ratio == 0.4:
        assert _pi_t == pytest.approx(0.229615567)
    elif subcategory_id == 7 and voltage_ratio == 0.8:
        assert _pi_t == pytest.approx(2.06654010)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_subcategory():
    """calculate_temperature_factor() should raise a KeyError if passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _pi_t = semiconductor.calculate_temperature_factor(27, 1, 0.5, 52.8)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_type():
    """calculate_temperature_factor() should raise an IndexError if passed an unknown type ID."""
    with pytest.raises(IndexError):
        _pi_t = semiconductor.calculate_temperature_factor(2, 17, 0.5, 52.8)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 7, 13])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_application_factor(subcategory_id, application_id):
    """calculate_application_factor() should return a float value on success."""
    _pi_a = semiconductor.calculate_application_factor(subcategory_id,
                                                       application_id, 65.0)

    assert isinstance(_pi_a, float)
    if subcategory_id == 1:
        assert _pi_a == 0.0
    elif subcategory_id == 2 and application_id == 1:
        assert _pi_a == 0.5
    elif subcategory_id == 2 and application_id == 2:
        assert _pi_a == 2.5
    elif subcategory_id == 7 and application_id == 1:
        assert _pi_a == 7.6
    elif subcategory_id == 7 and application_id == 2:
        assert _pi_a == 0.439
    elif subcategory_id == 13 and application_id == 1:
        assert _pi_a == 4.4
    elif subcategory_id == 13 and application_id == 2:
        assert _pi_a == pytest.approx(0.80622577)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_application_factor_no_application():
    """calculate_application_factor() should raise an IndexError when passed an unknown application ID."""
    with pytest.raises(IndexError):
        _pi_a = semiconductor.calculate_application_factor(3, 11, 65.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_application_factor_negative_duty_cycle():
    """calculate_application_factor() should raise a ValueError when passed a negative value for the duty cycle."""
    with pytest.raises(ValueError):
        _pi_a = semiconductor.calculate_application_factor(13, 2, -65.0)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 4])
@pytest.mark.parametrize("power_rated", [0.075, 10.0])
def test_calculate_power_rating_factor(subcategory_id, type_id, power_rated):
    """calculate_power_rating_factor() should return a float value for piR on success."""
    _pi_r = semiconductor.calculate_power_rating_factor(
        subcategory_id, type_id, power_rated, 0.125)

    assert isinstance(_pi_r, float)
    if subcategory_id == 2 and type_id == 1:
        assert _pi_r == 1.0
    elif subcategory_id == 2 and type_id == 4 and power_rated == 10.0:
        assert _pi_r == pytest.approx(0.50064274)
    elif subcategory_id == 3 and power_rated == 0.075:
        assert _pi_r == 0.43
    elif subcategory_id == 3 and power_rated == 10.0:
        assert _pi_r == pytest.approx(2.34422882)
    elif subcategory_id == 10:
        assert _pi_r == pytest.approx(0.435275282)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_power_rating_factor_string_input():
    """calculate_power_rating_factor() should raise a TypeError when passed a string value for rated power or rated current."""
    with pytest.raises(TypeError):
        _pi_r = semiconductor.calculate_power_rating_factor(
            2, 4, '10.0', 0.125)

    with pytest.raises(TypeError):
        _pi_r = semiconductor.calculate_power_rating_factor(
            10, 4, 10.0, '0.125')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_power_rating_factor_negative_input():
    """calculate_power_rating_factor() should raise a ValueError when passed a negative value for rated power."""
    with pytest.raises(ValueError):
        _pi_r = semiconductor.calculate_power_rating_factor(2, 4, -10.0, 0.125)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 6])
@pytest.mark.parametrize("voltage_ratio", [0.25, 0.75])
def test_calculate_electrical_stress_factor(subcategory_id, type_id,
                                            voltage_ratio):
    """calculate_electrical_stress_factor() should return a float value on success."""
    _pi_s = semiconductor.calculate_electrical_stress_factor(
        subcategory_id, type_id, voltage_ratio)

    assert isinstance(_pi_s, float)
    if subcategory_id == 1 and type_id == 6:
        assert _pi_s == 1.0
    elif subcategory_id == 1 and voltage_ratio == 0.25:
        assert _pi_s == 0.054
    elif subcategory_id == 1 and voltage_ratio == 0.75:
        assert _pi_s == pytest.approx(0.49704862)
    elif subcategory_id == 3 and voltage_ratio == 0.25:
        assert _pi_s == pytest.approx(0.097676646)
    elif subcategory_id == 10 and voltage_ratio == 0.25:
        assert _pi_s == 0.1
    elif subcategory_id == 10 and voltage_ratio == 0.75:
        assert _pi_s == pytest.approx(0.57891713)


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
        assert _attributes['hazard_rate_active'] == pytest.approx(
            0.00074950624)
    elif subcategory_id == 2:
        assert _attributes['piA'] == 0.5
        assert _attributes['piR'] == 1.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.17308627)
    elif subcategory_id == 6:
        assert _attributes['piR'] == 1.0
        assert _attributes['piS'] == pytest.approx(0.18157386)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.02590612)
    elif subcategory_id == 7:
        assert _attributes['piM'] == 2.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.22250891)
    elif subcategory_id == 13:
        assert _attributes['piI'] == pytest.approx(0.10820637)
        assert _attributes['piP'] == pytest.approx(0.69444444)
        assert _attributes['hazard_rate_active'] == pytest.approx(2.93281303)


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
