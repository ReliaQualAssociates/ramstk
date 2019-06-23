# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_semiconductor.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES, RAMSTK_STRESS_LIMITS
from ramstk.analyses.prediction import Component

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 2
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210, 0.200, 0.44,
            0.170, 0.00180, 0.076, 0.23, 1.50,
        ],
        2: [
            0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054, 0.054, 0.12,
            0.045, 0.00047, 0.020, 0.06, 0.40,
        ],
        3: [
            0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700, 3.700, 8.00,
            3.100, 0.03200, 1.400, 4.10, 28.0,
        ],
        4: [
            0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160, 0.160, 0.35,
            0.130, 0.00140, 0.060, 0.18, 1.20,
        ],
        5: [
            0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170, 0.170, 0.36,
            0.140, 0.00150, 0.062, 0.18, 1.20,
        ],
        6: [
            0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150, 0.130, 0.27,
            0.120, 0.00160, 0.060, 0.16, 1.30,
        ],
        7: [
            0.00580, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250, 0.220, 0.460,
            0.21, 0.00280, 0.100, 0.28, 2.10,
        ],
    },
    2: {
        1: [
            0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0, 62.0, 44.0, 0.43,
            16.0, 67.0, 350.0,
        ],
        2: [
            0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50, 7.60, 7.90, 0.16,
            3.70, 12.0, 94.00,
        ],
        3: [
            0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032, 0.057, 0.097,
            0.10, 0.002, 0.048, 0.15, 1.2,
        ],
        4: [
            0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69, 0.71,
            0.014, 0.34, 1.1, 8.5,
        ],
        5: [
            0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2, 0.023,
            0.56, 1.8, 14.0,
        ],
        6: [
            0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062, 0.11,
            0.11, 0.0022, 0.052, 0.17, 1.3,
        ],
    },
    3: {
        1: [
            0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067, 0.0060,
            0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056,
        ],
        2: [
            0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23, 0.50, 0.22,
            0.0029, 0.11, 0.29, 1.1,
        ],
    },
    4: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51, 0.0069,
        0.25, 0.68, 5.3,
    ],
    5: [
        0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6, 0.66, 0.0079,
        0.31, 0.88, 6.4,
    ],
    6: [
        0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3, 2.4, 0.047, 1.1,
        3.6, 28.0,
    ],
    7: [
        0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52, 0.88, 0.037, 0.33,
        0.66, 1.8, 18.0,
    ],
    8: {
        1: [
            0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2, 0.083, 2.8,
            11.0, 63.0,
        ],
        2: [
            0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0, 0.21, 6.9,
            27.0, 160.0,
        ],
    },
    9: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51, 0.0069,
        0.25, 0.68, 5.3,
    ],
    10: [
        0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14, 0.14, 0.31, 0.12,
        0.0012, 0.053, 0.16, 1.1,
    ],
    11: {
        1: [
            0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100, 0.2100,
            0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70,
        ],
        2: [
            0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500, 0.4900,
            0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70,
        ],
        3: [
            0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044, 0.0086,
            0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15,
        ],
    },
    12: [
        0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11, 0.19, 0.18,
        0.0031, 0.082, 0.28, 2.0,
    ],
    13: {
        1: [
            5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0, 230.0, 2.6,
            87.0, 350.0, 2000.0,
        ],
        2: [
            8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0, 300.0, 400.0,
            4.5, 150.0, 600.0, 3500.0,
        ],
    },
}

PART_COUNT_PIQ = {
    1: [0.7, 1.0, 2.4, 5.5, 8.0],
    2: [[0.5, 1.0, 5.0, 25, 50], [0.5, 1.0, 1.8, 2.5]],
    3: [0.7, 1.0, 2.4, 5.5, 8.0],
    4: [0.7, 1.0, 2.4, 5.5, 8.0],
    5: [0.7, 1.0, 2.4, 5.5, 8.0],
    6: [0.7, 1.0, 2.4, 5.5, 8.0],
    7: [0.7, 1.0, 2.4, 5.5, 8.0],
    8: [0.7, 1.0, 2.4, 5.5, 8.0],
    9: [0.7, 1.0, 2.4, 5.5, 8.0],
    10: [0.7, 1.0, 2.4, 5.5, 8.0],
    11: [0.7, 1.0, 2.4, 5.5, 8.0],
    12: [0.7, 1.0, 2.4, 5.5, 8.0],
    13: [1.0, 1.0, 3.3],
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
)
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        subcategory_id, type_id,
        quality_id, environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['type_id'] = type_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        if subcategory_id in [1, 2, 3, 8, 11, 13]:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][type_id][
                environment_active_id - 1
            ]
        else:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][
                environment_active_id - 1
            ]
    except (KeyError, IndexError):
        lambda_b = 0.0

    try:
        if subcategory_id == 2:
            if type_id == 5:
                piQ = PART_COUNT_PIQ[subcategory_id][1][quality_id - 1]
            else:
                piQ = PART_COUNT_PIQ[subcategory_id][0][quality_id - 1]
        else:
            piQ = PART_COUNT_PIQ[subcategory_id][quality_id - 1]
    except (IndexError, KeyError):
        piQ = 0.0

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0 and piQ > 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating semiconductor, hardware ID: 6 and active '
            'environment ID: {0:d}.\n'
        ).format(environment_active_id)
    elif piQ == 0.0:
        assert _msg == (
            'RAMSTK WARNING: piQ is 0.0 when calculating '
            'semiconductor, hardware ID: 6 and quality '
            'ID: {0:d}.'
        ).format(quality_id)
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 0.15
    ATTRIBUTES['temperature_case'] = 45.0
    ATTRIBUTES['theta_jc'] = 70.0
    ATTRIBUTES['voltage_rated'] = 5.0
    ATTRIBUTES['voltage_ac_operating'] = 0.05
    ATTRIBUTES['voltage_dc_operating'] = 3.3

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes, _msg = Component.do_calculate_217f_part_stress(**_attributes)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert _attributes['temperature_junction'] == 55.5
    assert _attributes['lambda_b'] == 0.0034
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 9.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['piT'], 2.6196648)
    assert pytest.approx(_attributes['piS'], 0.3778868)
    assert pytest.approx(_attributes['hazard_rate_active'], 0.01781886)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the quality ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 22
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 0.15
    ATTRIBUTES['temperature_case'] = 45.0
    ATTRIBUTES['theta_jc'] = 70.0
    ATTRIBUTES['voltage_rated'] = 5.0
    ATTRIBUTES['voltage_ac_operating'] = 0.05
    ATTRIBUTES['voltage_dc_operating'] = 3.3

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes, _msg = Component.do_calculate_217f_part_stress(**_attributes)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating semiconductor, '
        'hardware ID: 6 and quality ID: 22.\n'
    )
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert _attributes['temperature_junction'] == 55.5
    assert _attributes['lambda_b'] == 0.0034
    assert _attributes['piQ'] == 0.0
    assert _attributes['piE'] == 9.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['piT'], 2.6196648)
    assert pytest.approx(_attributes['piS'], 0.3778868)
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 41
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 0.15
    ATTRIBUTES['temperature_case'] = 45.0
    ATTRIBUTES['theta_jc'] = 70.0
    ATTRIBUTES['voltage_rated'] = 5.0
    ATTRIBUTES['voltage_ac_operating'] = 0.05
    ATTRIBUTES['voltage_dc_operating'] = 3.3

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes, _msg = Component.do_calculate_217f_part_stress(**_attributes)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert _attributes['temperature_junction'] == 55.5
    assert _attributes['lambda_b'] == 0.0034
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 1.0
    assert _attributes['piC'] == 2.0
    assert pytest.approx(_attributes['piT'], 2.6196648)
    assert pytest.approx(_attributes['piS'], 0.3778868)
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0123875)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("power_rated", [1.0, 0.75])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_power_overstress_harsh_environment(
        power_rated,
        environment_active_id,
):
    """overstressed() should return True when power ratio > 0.70 in a harsh environment and False otherwise."""
    ATTRIBUTES['power_operating'] = 0.6
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 38.7
    ATTRIBUTES['temperature_junction'] = 48.7
    ATTRIBUTES['power_rated'] = power_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if power_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif power_rated == 0.75:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating power > 70.0% rated '
            'power in harsh environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_junction", [28.7, 128.2])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_temperature_overstress_harsh_environment(
        temperature_junction,
        environment_active_id,
):
    """overstressed() should return True when junction temperature is >125C in a harsh environment and False otherwise."""
    ATTRIBUTES['power_operating'] = 0.18
    ATTRIBUTES['power_rated'] = 0.5
    ATTRIBUTES['temperature_active'] = 18.7
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_junction'] = temperature_junction
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if temperature_junction == 128.2:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating temperature > 125.0C '
            'Junction temperature limit in harsh '
            'environment.\n'
        )
    elif temperature_junction == 28.7:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("power_rated", [1.0, 0.5])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_voltage_overstress_mild_environment(
        power_rated,
        environment_active_id,
):
    """overstressed() should return True when voltage ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['power_operating'] = 0.47
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 38.7
    ATTRIBUTES['temperature_junction'] = 48.7
    ATTRIBUTES['power_rated'] = power_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if power_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif power_rated == 0.5:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating power > 90.0% rated '
            'power in mild environment.\n'
        )
