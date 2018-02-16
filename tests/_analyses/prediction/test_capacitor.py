#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_capacitor.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor module."""

import pytest
from tests.data import HARDWARE_ATTRIBUTES, DORMANT_MULT

from rtk.analyses.prediction import Capacitor, Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.0036, 0.0072, 0.330, 0.016, 0.055, 0.023, 0.030, 0.07, 0.13,
            0.083, 0.0018, 0.044, 0.12, 2.1
        ],
        2: [
            0.0039, 0.0087, 0.042, 0.022, 0.070, 0.035, 0.047, 0.19, 0.35,
            0.130, 0.0020, 0.056, 0.19, 2.5
        ]
    },
    2: [
        0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030, 0.040, 0.094, 0.15, 0.11,
        0.0024, 0.058, 0.18, 2.7
    ],
    3: [
        0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068, 0.013, 0.026, 0.048,
        0.044, 0.0010, 0.023, 0.063, 1.1
    ],
    4: [
        0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012, 0.018, 0.037, 0.066, 0.060,
        0.0014, 0.032, 0.088, 1.5
    ],
    5: [
        0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026, 0.048, 0.086, 0.14, 0.10,
        0.0020, 0.054, 0.15, 2.5
    ],
    6: [
        0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096, 0.014, 0.034, 0.053,
        0.048, 0.0011, 0.026, 0.07, 1.2
    ],
    7: [
        0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095, 0.054, 0.069,
        0.031, 0.00025, 0.012, 0.046, 0.45
    ],
    8: [
        0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60, 0.48, 0.0091,
        0.25, 0.68, 11.0
    ],
    9: [
        0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062, 0.035, 0.045,
        0.020, 0.00016, 0.0076, 0.030, 0.29
    ],
    10: [
        0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015, 0.015, 0.032, 0.048, 0.077,
        0.0014, 0.049, 0.13, 2.3
    ],
    11: [
        0.00078, 0.0022, 0.013, 0.0056, 0.023, 0.0077, 0.015, 0.053, 0.12,
        0.048, 0.00039, 0.017, 0.065, 0.68
    ],
    12: [
        0.0018, 0.0039, 0.016, 0.0097, 0.028, 0.0091, 0.011, 0.034, 0.057,
        0.055, 0.00072, 0.022, 0.066, 1.0
    ],
    13: [
        0.0061, 0.013, 0.069, 0.039, 0.11, 0.031, 0.061, 0.13, 0.29, 0.18,
        0.0030, 0.069, 0.26, 4.0
    ],
    14: [
        0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6, 1.2, .012, 0.49,
        1.7, 21.0
    ],
    15: [
        0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4, 2.0, 0.015, 0.68,
        2.8, 28.0
    ],
    16: [
        0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9, 5.9,
        85.0
    ],
    17: [
        0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16, 0.93,
        3.2, 37.0
    ],
    18: [
        0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5, 8.9,
        100.0
    ],
    19: [
        0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0, 0.0,
        0.0
    ]
}

PART_COUNT_PIQ = [0.030, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0]

ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
@pytest.mark.parametrize("specification_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(subcategory_id, specification_id,
                                            quality_id, environment_active_id):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['specification_id'] = specification_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    if subcategory_id == 1:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][specification_id][
            environment_active_id - 1]
    else:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id
                                                       - 1]

    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Capacitor.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when '
                        'calculating capacitor, hardware ID: 6')
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_subcategory():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
    ATTRIBUTES['subcategory_id'] = 0
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Capacitor.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'capacitor, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_specification():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the specification ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['specification_id'] = 0
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Capacitor.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'capacitor, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Capacitor.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'capacitor, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['capacitance'] = 0.0000033
    ATTRIBUTES['voltage_rated'] = 5.0
    ATTRIBUTES['voltage_ac_operating'] = 0.05
    ATTRIBUTES['voltage_dc_operating'] = 3.3

    _attributes, _msg = Capacitor.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert pytest.approx(_attributes['lambda_b'], 0.07944039)
    assert pytest.approx(_attributes['piCV'], 0.3617763)
    assert _attributes['piQ'] == 7.0
    assert _attributes['piE'] == 5.0
    assert pytest.approx(_attributes['hazard_rate_active'], 1.005887691)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
@pytest.mark.parametrize("environment_dormant_id", [1, 2, 3, 4])
def test_calculate_dormant_hazard_rate(environment_active_id,
                                       environment_dormant_id):
    """calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_active'] = 1.005887691
    ATTRIBUTES['environment_active_id'] = environment_active_id
    ATTRIBUTES['environment_dormant_id'] = environment_dormant_id

    try:
        dormant_mult = DORMANT_MULT[environment_active_id][ATTRIBUTES[
            'environment_dormant_id']]
    except KeyError:
        dormant_mult = 0.0

    _attributes, _msg = Component.do_calculate_dormant_hazard_rate(
        **ATTRIBUTES)

    assert isinstance(_attributes, dict)
    try:
        assert _msg == ''
    except AssertionError:
        assert _msg == ('RTK ERROR: Unknown active and/or dormant environment '
                        'ID.  Active ID: {0:d}, '
                        'Dormant ID: {1:d}').format(environment_active_id,
                                                    environment_dormant_id)

    assert pytest.approx(_attributes['hazard_rate_dormant'],
                         ATTRIBUTES['hazard_rate_active'] * dormant_mult)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [20.0, 12.0])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_voltage_overstress_harsh_environment(voltage_rated,
                                              environment_active_id):
    """overstressed() should return True when voltage ratio > 0.6 in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 10.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 20.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 12.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating voltage > 60% rated '
                                         'voltage in harsh environment.\n')


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_active", [48.7, 118.2])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_temperature_overstress_harsh_environment(temperature_active,
                                                  environment_active_id):
    """overstressed() should return True when active temperature is within 10C of rated temperature in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_rated'] = 20.0
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 10.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = temperature_active
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if temperature_active == 48.7:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif temperature_active == 118.2:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating temperature within '
                                         '10.0C of maximum rated '
                                         'temperature.\n')


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [20.0, 12.0])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_voltage_overstress_mild_environment(voltage_rated,
                                             environment_active_id):
    """overstressed() should return True when voltage ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 11.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 20.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 12.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating voltage > 90% rated '
                                         'voltage in mild environment.\n')
