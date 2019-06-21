# pylint: disable=invalid-name
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
from ramstk.analyses.data import HARDWARE_ATTRIBUTES, RAMSTK_STRESS_LIMITS
from ramstk.analyses.prediction import Component, Inductor

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 5
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
            0.11, 0.0018, 0.053, 0.16, 2.3,
        ],
        2: [
            0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
            0.035, 0.11, 0.31, 4.7,
        ],
        3: [
            0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
            0.37, 1.2, 16.0,
        ],
        4: [
            0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
            0.42, 1.2, 19.0,
        ],
    },
    2: {
        1: [
            0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
            0.052, 0.00083, 0.25, 0.073, 1.1,
        ],
        2: [
            0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
            0.10, 0.0017, 0.05, 0.15, 2.2,
        ],
    },
}

PART_COUNT_PIQ = [0.25, 1.0, 10.0]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize("quality_id", [1, 2, 3])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        subcategory_id, family_id,
        quality_id, environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['family_id'] = family_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][family_id][
            environment_active_id - 1
        ]
    except (KeyError, IndexError):
        lambda_b = 0.0
    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating inductor, hardware ID: 6, subcategory '
            'ID: {0:d}, family ID: {1:d}, and active '
            'environment ID: {2:d}.'
        ).format(
            subcategory_id, family_id, environment_active_id,
        )
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_subcategory():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
    ATTRIBUTES['subcategory_id'] = 0
    ATTRIBUTES['family_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'inductor, hardware ID: 6, subcategory ID: 0, family '
        'ID: 1, and active environment ID: 1.'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.25
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_family():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the family ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['family_id'] = 0
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'inductor, hardware ID: 6, subcategory ID: 1, family ID: 0, and '
        'active environment ID: 1.'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['family_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'inductor, hardware ID: 6, subcategory ID: 1, family ID: 1, and '
        'active environment ID: 100.'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.25
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['family_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 11

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating inductor, '
        'hardware ID: 6, quality ID: 11.'
    )
    assert _attributes['lambda_b'] == 0.0035
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Inductor.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.0003462094)
    assert _attributes['piQ'] == 0.1
    assert _attributes['piE'] == 5.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0003462094)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the quality ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 20
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Inductor.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating inductor, '
        'hardware ID: 6'
    )
    assert pytest.approx(_attributes['lambda_b'], 0.0003462094)
    assert _attributes['piQ'] == 0.0
    assert _attributes['piE'] == 5.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the active environment ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 40
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Inductor.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating inductor, '
        'hardware ID: 6'
    )
    assert pytest.approx(_attributes['lambda_b'], 0.0003462094)
    assert _attributes['piQ'] == 0.1
    assert _attributes['piE'] == 0.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_insulation():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the insulation ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['insulation_id'] = 30
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Inductor.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'inductor, hardware ID: 6'
    )
    assert pytest.approx(_attributes['lambda_b'], 0.0)
    assert _attributes['piQ'] == 0.1
    assert _attributes['piE'] == 5.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [20.0, 10.0])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_voltage_overstress_harsh_environment(
        voltage_rated,
        environment_active_id,
):
    """overstressed() should return True when voltage ratio > 0.5 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.18
    ATTRIBUTES['current_rated'] = 0.5
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Inductor.calculate_hot_spot_temperature(**_attributes)
    _attributes['temperature_hot_spot'] = 65.0
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 20.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 10.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating voltage > 50.0% rated '
            'voltage in harsh environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [1.0, 0.5])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_current_overstress_harsh_environment(
        current_rated,
        environment_active_id,
):
    """overstressed() should return True when current ratio > 0.6 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.48
    ATTRIBUTES['current_rated'] = current_rated
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = 15.0
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Inductor.calculate_hot_spot_temperature(**_attributes)
    _attributes['temperature_hot_spot'] = 65.0
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if current_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif current_rated == 0.5:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating current > 60.0% rated '
            'current in harsh environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_active", [28.7, 118.2])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_temperature_overstress_harsh_environment(
        temperature_active,
        environment_active_id,
):
    """overstressed() should return True when hot spot temperature is within 15C of rated temperature in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.18
    ATTRIBUTES['current_rated'] = 0.5
    ATTRIBUTES['voltage_rated'] = 20.0
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['temperature_active'] = temperature_active
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Inductor.calculate_hot_spot_temperature(**_attributes)
    _attributes['temperature_hot_spot'] = 65.0
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if temperature_active == 28.7:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif temperature_active == 118.2:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating temperature within '
            '15.0C of Hot Spot temperature in '
            'harsh environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [20.0, 10.0])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_voltage_overstress_mild_environment(
        voltage_rated,
        environment_active_id,
):
    """overstressed() should return True when voltage ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 9.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Inductor.calculate_hot_spot_temperature(**_attributes)
    _attributes['temperature_hot_spot'] = 65.0
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 20.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 10.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating voltage > 90.0% rated '
            'voltage in mild environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [1.0, 0.5])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_current_overstress_mild_environment(
        current_rated,
        environment_active_id,
):
    """overstressed() should return True when current ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.48
    ATTRIBUTES['current_rated'] = current_rated
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = 15.0
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Inductor.calculate_hot_spot_temperature(**_attributes)
    _attributes['temperature_hot_spot'] = 65.0
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if current_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif current_rated == 0.5:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating current > 90.0% rated '
            'current in mild environment.\n'
        )
