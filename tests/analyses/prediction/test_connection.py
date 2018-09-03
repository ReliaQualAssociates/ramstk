#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_connection.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the connection module."""

import pytest

from rtk.analyses.data import HARDWARE_ATTRIBUTES
from rtk.analyses.prediction import Component, Connection

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014, 2018 Andrew "weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 8
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23, 0.34, 0.37,
            0.0054, 0.16, 0.42, 6.8
        ],
        2: [
            0.012, 0.015, 0.13, 0.075, 0.21, 0.06, 0.1, 0.22, 0.32, 0.38,
            0.0061, 0.18, 0.54, 7.3
        ]
    },
    2: [
        0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
        0.0027, 0.078, 0.21, 3.4
    ],
    3: [
        0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021, 0.025, 0.048,
        0.00097, 0.027, 0.070, 1.3
    ],
    4: [
        0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 0.43, 0.85, 1.5, 1.0, 0.027, 0.53,
        1.4, 27.0
    ],
    5: {
        1: [
            0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016, 0.016, 0.021,
            0.042, 0.0013, 0.023, 0.062, 1.1
        ],
        2: [
            0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056, 0.00084,
            0.00084, 0.0011, 0.0022, 0.00007, 0.0013, 0.0034, 0.059
        ],
        3: [
            0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010, 0.0016, 0.0016,
            0.0021, 0.0042, 0.00013, 0.0023, 0.0062, 0.11
        ],
        4: [
            0.000050, 0.000100, 0.000350, 0.000200, 0.000550, 0.000200,
            0.000300, 0.000300, 0.000400, 0.000800, 0.000025, 0.000450,
            0.001200, 0.021000
        ],
        5: [
            0.0000035, 0.000007, 0.000025, 0.000014, 0.000039, 0.000014,
            0.000021, 0.000021, 0.000028, 0.000056, 0.0000018, 0.000031,
            0.000084, 0.0015
        ],
        6: [
            0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048, 0.00072,
            0.00072, 0.00096, 0.0019, 0.00005, 0.0011, 0.0029, 0.050
        ],
        7: [
            0.000069, 0.000138, 0.000483, 0.000276, 0.000759, 0.000276,
            0.000414, 0.000414, 0.000552, 0.001104, 0.000035, 0.000621,
            0.001656, 0.02898
        ]
    }
}

PART_COUNT_PIQ = [1.0, 2.0]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(subcategory_id, type_id,
                                            quality_id, environment_active_id):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['type_id'] = type_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    if subcategory_id in [1, 5]:
        try:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][type_id][
                environment_active_id - 1]
        except KeyError:
            lambda_b = 0.0
    else:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id -
                                                       1]

    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == ('RAMSTK WARNING: Base hazard rate is 0.0 when '
                        'calculating connection, hardware ID: 6')
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
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_type():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the type ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 0
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.030
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Connection.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
                    'connection, hardware ID: 6')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 3
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['specification_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['insert_id'] = 1
    ATTRIBUTES['contact_gauge'] = 20
    ATTRIBUTES['current_operating'] = 2
    ATTRIBUTES['n_cycles'] = 2
    ATTRIBUTES['n_active_pins'] = 20

    _attributes, _msg = Connection.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['voltage_ratio'], 0.67)
    assert pytest.approx(_attributes['lambda_b'], 0.07944039)
    assert pytest.approx(_attributes['piCV'], 0.3617763)
    assert _attributes['piQ'] == 10.0
    assert pytest.approx(_attributes['hazard_rate_active'], 1.005887691)
    assert pytest.approx(_attributes['temperature_rise'], 2.3072012)
    assert pytest.approx(_attributes['lambda_b'], 0.0006338549)
    assert _attributes['piK'] == 2.0
    assert pytest.approx(_attributes['piP'], 4.0062301)
    assert _attributes['piE'] == 21.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.1066535)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_insert_temperature():
    """Test the calculate_insert_temperature() function."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['current_operating'] = 2.65
    ATTRIBUTES['contact_gauge'] = 20

    _attributes = Connection.do_calculate_insert_temperature(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert pytest.approx(_attributes['temperature_rise'], 3.88315602448)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [40.0, 20.0])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_voltage_overstress_harsh_environment(voltage_rated,
                                              environment_active_id):
    """overstressed() should return True when voltage ratio > 0.6 in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 15.0
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 40.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 20.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating voltage > 70% rated '
                                         'voltage in harsh environment.\n')


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_active", [48.7, 118.2])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_temperature_overstress_harsh_environment(temperature_active,
                                                  environment_active_id):
    """overstressed() should return True when active temperature is within 10C of rated temperature in a harsh environment and False otherwise."""
    ATTRIBUTES['voltage_rated'] = 40.0
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
                                         '25.0C of maximum rated '
                                         'temperature.\n')


@pytest.mark.unit
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
