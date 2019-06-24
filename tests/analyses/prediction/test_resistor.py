# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_resistor.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES, RAMSTK_STRESS_LIMITS
from ramstk.analyses.prediction import Component, Resistor

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 3
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: [
        0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016, 0.025,
        0.025, 0.00025, 0.0098, 0.035, 0.36,
    ],
    2: {
        1: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033,
            0.030, 0.00025, 0.014, 0.044, 0.69,
        ],
        2: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033,
            0.030, 0.00025, 0.014, 0.044, 0.69,
        ],
        3: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038,
            0.034, 0.00028, 0.016, 0.050, 0.78,
        ],
        4: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038,
            0.034, 0.00028, 0.016, 0.050, 0.78,
        ],
    },
    3: [
        0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19, 0.24, 0.32, 0.0060,
        0.18, 0.47, 8.2,
    ],
    4: [
        0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043, 0.077, 0.15, 0.10,
        0.0011, 0.055, 0.15, 1.7,
    ],
    5: [
        0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30, 0.38, 0.26, 0.0068,
        0.13, 0.37, 5.4,
    ],
    6: {
        1: [
            0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19, 0.39, 0.42,
            0.0042, 0.21, 0.62, 9.4,
        ],
        2: [
            0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18, 0.35, 0.38,
            0.0038, 0.19, 0.56, 8.6,
        ],
    },
    7: [
        0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12, 0.24, 0.25, 0.004,
        0.13, 0.37, 5.5,
    ],
    8: [
        0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7, 2.4, 0.032, 1.3, 3.4,
        62.0,
    ],
    9: [
        0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35, 0.58, 1.1, 0.013,
        0.52, 1.6, 24.0,
    ],
    10: [
        0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0, 0.16, 11.0, 33.0,
        510.0,
    ],
    11:
    [0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0, 0.075, 0.0, 0.0, 0.0],
    12:
    [0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6, 0.076, 0.0, 0.0, 0.0],
    13: [
        0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8, 2.8, 2.5, 0.21, 1.2,
        3.7, 49.0,
    ],
    14: [
        0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5, 3.3, 0.025, 1.5, 4.7,
        67.0,
    ],
    15: [
        0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2, 2.3, 0.024, 1.2,
        3.4, 52.0,
    ],
}

PART_COUNT_PIQ = [0.030, 0.10, 0.30, 1.0, 3.0, 10.0]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
)
@pytest.mark.parametrize("specification_id", [1, 2, 3, 4])
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        subcategory_id, specification_id,
        quality_id, environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['specification_id'] = specification_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        if subcategory_id in [2, 6]:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][specification_id][
                environment_active_id - 1
            ]
        else:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][
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
            'calculating resistor, hardware ID: 6, subcategory '
            'ID: {0:d}, specification ID: {1:d}, active '
            'environment ID: {2:d}, and quality ID: '
            '{3:d}.\n'
        ).format(
            subcategory_id, specification_id,
            environment_active_id, quality_id,
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
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'resistor, hardware ID: 6, subcategory ID: 0, '
        'specification ID: 1, active environment ID: 1, and '
        'quality ID: 1.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.03
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_specification():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the specification ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['specification_id'] = 10
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'resistor, hardware ID: 6, subcategory ID: 2, specification ID: 10, '
        'active environment ID: 1, and quality ID: 1.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'resistor, hardware ID: 6, subcategory ID: 1, specification ID: 1, '
        'active environment ID: 100, and quality ID: 1.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.03
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 11

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert _attributes['lambda_b'] == 0.0005
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0005


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 10
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['power_rated'] = 5.0
    ATTRIBUTES['power_operating'] = 1.5
    ATTRIBUTES['voltage_rated'] = 250.0
    ATTRIBUTES['voltage_ac_operating'] = 0.05
    ATTRIBUTES['voltage_dc_operating'] = 15.0
    ATTRIBUTES['resistance'] = 3.3E4
    ATTRIBUTES['n_elements'] = 4

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes, _msg = Component.do_calculate_217f_part_stress(**_attributes)

    assert isinstance(_attributes, dict)
    assert _msg == 'RAMSTK WARNING: piT is 0.0 when calculating resistor, ' \
                   'hardware ID: 6, subcategory ID: 10, case temperature: ' \
                   '0.000000, ambient temperature: 32.000000, power ' \
                   'ratio: 0.300000.\n'
    assert _attributes['power_ratio'] == 0.3
    assert pytest.approx(_attributes['voltage_ratio'], 0.8901438)
    assert pytest.approx(_attributes['lambda_b'], 4.2888845)
    assert _attributes['piQ'] == 5.0
    assert _attributes['piE'] == 8.0
    assert _attributes['piC'] == 1.0
    assert _attributes['piV'] == 1.1
    assert _attributes['piR'] == 1.1
    assert _attributes['piTAPS'] == 1.112
    assert pytest.approx(_attributes['hazard_rate_active'], 293.7851584)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("power_rated", [0.5, 0.25])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_power_overstress_harsh_environment(
        power_rated,
        environment_active_id,
):
    """overstressed() should return True when power ratio > 0.5 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.0
    ATTRIBUTES['current_rated'] = 0.1
    ATTRIBUTES['voltage_rated'] = 25.0
    ATTRIBUTES['power_operating'] = 0.18
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['power_rated'] = power_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if power_rated == 0.5:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif power_rated == 0.25:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating power > 50.0% rated '
            'power in harsh environment.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("power_rated", [0.5, 0.25])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_power_overstress_mild_environment(
        power_rated,
        environment_active_id,
):
    """overstressed() should return True when power ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.0
    ATTRIBUTES['current_rated'] = 0.1
    ATTRIBUTES['voltage_rated'] = 25.0
    ATTRIBUTES['power_operating'] = 0.235
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['power_rated'] = power_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if power_rated == 0.5:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif power_rated == 0.25:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating power > 90.0% rated '
            'power in mild environment.\n'
        )


@pytest.mark.unit
def test_check_variable_zero():
    """_do_check_variables() should return a warning message when variables <= zero."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['hardware_id'] = 100
    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piQ'] = 1.0
    ATTRIBUTES['piC'] = 1.0
    ATTRIBUTES['piR'] = 1.0
    ATTRIBUTES['piT'] = 1.0
    ATTRIBUTES['piV'] = 1.0

    ATTRIBUTES['lambda_b'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating resistor, '
        'hardware ID: 100, subcategory ID: 10, specification ID: 1, active '
        'environment ID: 11, and quality ID: 2.\n'
    )

    ATTRIBUTES['lambda_b'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating resistor, '
        'hardware ID: 100, subcategory ID: 10, specification ID: 1, active '
        'environment ID: 11, and quality ID: 2.\n'
    )

    ATTRIBUTES['lambda_b'] = 1.0
    ATTRIBUTES['piQ'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating resistor, hardware ID: '
        '100, quality ID: 2.\n'
    )

    ATTRIBUTES['piQ'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating resistor, hardware ID: '
        '100, quality ID: 2.\n'
    )

    ATTRIBUTES['piQ'] = 1.0
    ATTRIBUTES['piE'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating resistor, hardware ID: '
        '100, active environment ID: 11.\n'
    )

    ATTRIBUTES['piE'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating resistor, hardware ID: '
        '100, active environment ID: 11.\n'
    )

    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piC'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piC is 0.0 when calculating resistor, hardware ID: '
        '100, construction ID: 2.\n'
    )

    ATTRIBUTES['piC'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piC is 0.0 when calculating resistor, hardware ID: '
        '100, construction ID: 2.\n'
    )

    ATTRIBUTES['piC'] = 1.0
    ATTRIBUTES['piR'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piR is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, specification ID: 1, family ID: 0, # of '
        'elements: 4.\n'
    )

    ATTRIBUTES['piR'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piR is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, specification ID: 1, family ID: 0, # of '
        'elements: 4.\n'
    )

    ATTRIBUTES['piR'] = 1.0
    ATTRIBUTES['piT'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piT is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, case temperature: 0.000000, ambient '
        'temperature: 48.700000, power ratio: 0.000000.\n'
    )

    ATTRIBUTES['piT'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piT is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, case temperature: 0.000000, ambient '
        'temperature: 48.700000, power ratio: 0.000000.\n'
    )

    ATTRIBUTES['piT'] = 1.0
    ATTRIBUTES['piV'] = -1.3
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piV is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, voltage ratio: 0.000000.\n'
    )

    ATTRIBUTES['piV'] = 0.0
    _msg = Resistor._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piV is 0.0 when calculating resistor, hardware ID: '
        '100, subcategory ID: 10, voltage ratio: 0.000000.\n'
    )
