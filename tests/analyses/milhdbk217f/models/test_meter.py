# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_meter.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the meter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import meter

ATTRIBUTES = {
    'category_id': 9,
    'subcategory_id': 1,
    'environment_active_id': 4,
    'type_id': 2,
    'application_id': 2,
    'temperature_active': 32.0,
    'temperature_rated_max': 85.0,
    'power_operating': 4.2,
    'piQ': 1.0,
    'piE': 7.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_get_part_count_lambda_b(subcategory_id, type_id,
                                 environment_active_id):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = meter.get_part_count_lambda_b(subcategory_id, type_id,
                                              environment_active_id)

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = meter.get_part_count_lambda_b(47, 1, 4)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = meter.get_part_count_lambda_b(1, 12, 4)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown subcategory ID."""
    with pytest.raises(IndexError):
        _lambda_b = meter.get_part_count_lambda_b(1, 1, 24)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = meter.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 105.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2, 3])
def test_get_part_stress_lambda_b(subcategory_id, type_id):
    """get_part_stress_lambda_b() should return a float value for the part stress base hazard rate on success."""
    _lambda_b = meter.get_part_stress_lambda_b(subcategory_id, type_id)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == [20.0, 30.0, 80.0][type_id - 1]
    elif subcategory_id == 2:
        assert _lambda_b == 0.09


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_lambda_b_no_type():
    """get_part_stress_lambda_b() should raise an IndexError when passed an unknown type ID."""
    with pytest.raises(IndexError):
        _lambda_b = meter.get_part_stress_lambda_b(1, 4)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_stress_lambda_b_no_subcategory():
    """get_part_stress_lambda_b() should return 0.0 when passed an unknown subcategory ID."""
    _lambda_b = meter.get_part_stress_lambda_b(10, 1)

    assert _lambda_b == 0.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_active", [25.0, 40.0, 55.0, 70.0])
def test_get_temperature_stress_factor(temperature_active):
    """get_temperature_stress_factor() should return a float value for piT on success."""
    _pi_t = meter.get_temperature_stress_factor(temperature_active, 75.0)

    assert isinstance(_pi_t, float)
    assert _pi_t == {
        25.0: 0.5,
        40.0: 0.6,
        55.0: 0.8,
        70.0: 1.0
    }[temperature_active]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_temperature_stress_factor_zero_max_rated():
    """get_temperature_stress_factor() should raise a ZeroDivisionError when passed a maximum rated temperature of 0.0."""
    with pytest.raises(ZeroDivisionError):
        _pi_t = meter.get_temperature_stress_factor(35.0, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_temperature_stress_factor_wrong_type():
    """get_temperature_stress_factor() should raise a TypeError when passed a string for either temperature."""
    with pytest.raises(TypeError):
        _pi_t = meter.get_temperature_stress_factor('35.0', 75.0)

    with pytest.raises(TypeError):
        _pi_t = meter.get_temperature_stress_factor(35.0, '75.0')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_elapsed_time_meter():
    """calculate_part_stress() should return a dictionary of updated values on success."""
    _attributes = meter.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == 30.0
    assert _attributes['hazard_rate_active'] == 105.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_panel_meter():
    """calculate_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['subcategory_id'] = 2
    _attributes = meter.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx(0.09)
    assert _attributes['piA'] == 1.7
    assert _attributes['piF'] == 1.0
    assert _attributes['hazard_rate_active'] == pytest.approx(1.071)
