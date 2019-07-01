# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_inductor.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the inductor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import Inductor

ATTRIBUTES = {
    'category_id': 5,
    'subcategory_id': 1,
    'environment_active_id': 3,
    'insulation_id': 3,
    'family_id': 1,
    'construction_id': 1,
    'specification_id': 1,
    'quality_id': 1,
    'page_number': 3,
    'area': 12.5,
    'weight': 0.612,
    'power_operating': 0.875,
    'voltage_dc_operating': 3.3,
    'current_operating': 0.00108778877888,
    'temperature_active': 43.2,
    'piE': 5.0,
    'lambda_b': 0.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b_xfmr(
        family_id,
        environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = Inductor.get_part_count_lambda_b(1, family_id,
                                                 environment_active_id)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {
        1: [
            0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
            0.11, 0.0018, 0.053, 0.16, 2.3
        ],
        2: [
            0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
            0.035, 0.11, 0.31, 4.7
        ],
        3: [
            0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
            0.37, 1.2, 16.0
        ],
        4: [
            0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
            0.42, 1.2, 19.0
        ]
    }[family_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("family_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b_inductor(
        family_id,
        environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = Inductor.get_part_count_lambda_b(2, family_id,
                                                 environment_active_id)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {
        1: [
            0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
            0.052, 0.00083, 0.25, 0.073, 1.1
        ],
        2: [
            0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
            0.10, 0.0017, 0.05, 0.15, 2.2
        ]
    }[family_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = Inductor.get_part_count_lambda_b(20, 1, 3)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_family():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown family ID."""
    with pytest.raises(KeyError):
        _lambda_b = Inductor.get_part_count_lambda_b(2, 12, 3)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = Inductor.get_part_count_lambda_b(2, 1, 31)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("family_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_part_count_inductor(
        family_id,
        environment_active_id,
):
    """calculate_part_count() should return a float value for the base hazard rate on success."""
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['family_id'] = family_id
    ATTRIBUTES['environment_active_id'] = environment_active_id
    _lambda_b = Inductor.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {
        1: [
            0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
            0.052, 0.00083, 0.25, 0.073, 1.1
        ],
        2: [
            0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
            0.10, 0.0017, 0.05, 0.15, 2.2
        ]
    }[family_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_part_count_xfmr(
        family_id,
        environment_active_id,
):
    """calculate_part_count() should return a float value for the base hazard rate on success."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['family_id'] = family_id
    ATTRIBUTES['environment_active_id'] = environment_active_id
    _lambda_b = Inductor.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {
        1: [
            0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
            0.11, 0.0018, 0.053, 0.16, 2.3
        ],
        2: [
            0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
            0.035, 0.11, 0.31, 4.7
        ],
        3: [
            0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
            0.37, 1.2, 16.0
        ],
        4: [
            0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
            0.42, 1.2, 19.0
        ]
    }[family_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "page_number",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_temperature_rise_spec_sheet(page_number):
    """get_temperature_rise_spec_sheet() should return a float value for the temperature_rise on success."""
    _temperature_rise = Inductor.get_temperature_rise_spec_sheet(page_number)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == {
        1: 15.0,
        2: 15.0,
        3: 15.0,
        4: 35.0,
        5: 15.0,
        6: 35.0,
        7: 15.0,
        8: 35.0,
        9: 15.0,
        10: 15.0,
        11: 35.0,
        12: 35.0,
        13: 15.0,
        14: 15.0
    }[page_number]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_temperature_rise_no_spec_sheet():
    """get_temperature_rise_spec_sheet() should raise a KeyError when passed an unkown page number."""
    with pytest.raises(KeyError):
        _temperature_rise = Inductor.get_temperature_rise_spec_sheet(22)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_input_power_weight():
    """calculate_temperature_rise_input_power_weight() should return a float value on success."""
    _temperature_rise = Inductor.calculate_temperature_rise_input_power_weight(
        0.387, .015)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == pytest.approx(13.93114825)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_input_power_weight_zero_weight():
    """calculate_temperature_rise_input_power_weight() should raise a ZeroDivisionError when passed a weight=0.0."""
    with pytest.raises(ZeroDivisionError):
        _temperature_rise = Inductor.calculate_temperature_rise_input_power_weight(
            0.387, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_power_loss_surface():
    """calculate_temperature_rise_power_loss_surface() should return a float value on success."""
    _temperature_rise = Inductor.calculate_temperature_rise_power_loss_surface(
        0.387, 12.5)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == 3.87


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_power_loss_surface_zero_area():
    """calculate_temperature_rise_power_loss_surface() should raise a ZeroDivisionError when passed an area=0.0."""
    with pytest.raises(ZeroDivisionError):
        _temperature_rise = Inductor.calculate_temperature_rise_power_loss_surface(
            0.387, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_power_loss_weight():
    """calculate_temperature_rise_power_loss_radiating_surface() should return a float value on success."""
    _temperature_rise = Inductor.calculate_temperature_rise_power_loss_weight(
        0.387, 2.5)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == pytest.approx(2.394211958)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_rise_power_loss_weight_zero_weight():
    """calculate_temperature_rise_power_loss_weight() should raise a ZeroDivisionError when passed a weight=0.0."""
    with pytest.raises(ZeroDivisionError):
        _temperature_rise = Inductor.calculate_temperature_rise_power_loss_weight(
            0.387, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_hot_spot_temperature():
    """calculate_hot_spot_temperature() should return a float value on success."""
    _temperature_hot_spot = Inductor.calculate_hot_spot_temperature(43.2, 38.7)

    assert isinstance(_temperature_hot_spot, float)
    assert _temperature_hot_spot == pytest.approx(85.77)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b():
    """calculate_part_stress_lambda_b() should return a float value on success."""
    _lambda_b = Inductor.calculate_part_stress_lambda_b(1, 4, 85.77)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(0.00280133)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_subcategory():
    """calculate_part_stress_lambda_b() should raise an KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = Inductor.calculate_part_stress_lambda_b(101, 4, 85.77)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_no_insulation():
    """calculate_part_stress_lambda_b() should raise an KeyError when passed an unknown insulation ID."""
    with pytest.raises(KeyError):
        _lambda_b = Inductor.calculate_part_stress_lambda_b(1, 41, 85.77)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_stress_quality_factor(subcategory_id):
    """get_part_stress_quality_factor() should return a float value for piQ on success."""
    _pi_q = Inductor.get_part_stress_quality_factor(subcategory_id, 1, 1)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 1.5, 2: 0.03}[subcategory_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_inductor():
    """calculate_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['construction_id'] = 2
    _attributes = Inductor.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx(0.00046712295)
    assert _attributes['piC'] == 2.0
    assert _attributes['hazard_rate_active'] == pytest.approx(0.00014013688)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_xfmr():
    """calculate_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['construction_id'] = 1
    _attributes = Inductor.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambda_b'] == pytest.approx(0.0026358035)
    assert _attributes['piC'] == 1.0
    assert _attributes['hazard_rate_active'] == pytest.approx(0.15814821)
