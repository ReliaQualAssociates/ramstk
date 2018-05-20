#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_switch.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the switch module."""

import pytest

from rtk.analyses.data import HARDWARE_ATTRIBUTES
from rtk.analyses.prediction import Switch, Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 7
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: [
        0.0010, 0.0030, 0.018, 0.0080, 0.029, 0.010, 0.018, 0.013, 0.022,
        0.046, 0.0005, 0.025, 0.067, 1.2
    ],
    2: [
        0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3, 6.8, 0.74, 3.7, 9.9,
        180.0
    ],
    3: [
        0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2, 15.0, 0.16, 8.2, 22.0,
        390.0
    ],
    4: [
        0.56, 1.7, 10.0, 4.5, 16.0, 5.6, 10.0, 7.3, 12.0, 26.0, 0.26, 14.0,
        38.0, 670.0
    ],
    5: {
        1: [
            0.11, 0.23, 1.7, 0.91, 3.1, 0.8, 1.0, 1.3, 1.4, 5.2, 0.057, 2.8,
            7.5, 0.0
        ],
        2: [
            0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66, 0.72, 2.8, 0.030,
            1.5, 4.0, 0.0
        ]
    }
}

PART_COUNT_PIQ = {
    1: [1.0, 20.0],
    2: [1.0, 20.0],
    3: [1.0, 50.0],
    4: [1.0, 10.0],
    5: [1.0, 8.4]
}


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("construction_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(subcategory_id, construction_id,
                                            quality_id, environment_active_id):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['construction_id'] = construction_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][construction_id][
            environment_active_id - 1]
    except (KeyError, IndexError, TypeError):
        try:
            lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][
                environment_active_id - 1]
        except (KeyError, IndexError):
            lambda_b = 0.0
    piQ = PART_COUNT_PIQ[subcategory_id][quality_id - 1]

    _attributes, _msg = Switch.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0 and piQ > 0.0:
        assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when '
                        'calculating switch, hardware ID: 6, subcategory ID: '
                        '{0:d}, construction ID: {1:d}, and active '
                        'environment ID: {2:d}.\n').format(
                            subcategory_id, construction_id,
                            environment_active_id)
    elif piQ == 0.0:
        assert _msg == ('RTK WARNING: piQ is 0.0 when calculating switch, '
                        'hardware ID: 6, subcategory ID: {0:d}, and quality '
                        'ID: {1:d}.').format(_attributes['subcategory_id'],
                                             _attributes['quality_id'])
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
    ATTRIBUTES['subcategory_id'] = 10
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Switch.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating switch, '
                    'hardware ID: 6, subcategory ID: 10, and quality ID: 1.')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_construction():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the construction ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 5
    ATTRIBUTES['construction_id'] = 10
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Switch.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RTK WARNING: Base hazard rate is 0.0 when calculating '
        'switch, hardware ID: 6, subcategory ID: 5, construction ID: 10, '
        'and active environment ID: 1.\n')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Switch.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RTK WARNING: Base hazard rate is 0.0 when calculating '
        'switch, hardware ID: 6, subcategory ID: 1, construction ID: 1, and '
        'active environment ID: 100.\n')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 11

    _attributes, _msg = Switch.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating switch, '
                    'hardware ID: 6, subcategory ID: 1, and quality ID: 11.')
    assert _attributes['lambda_b'] == 0.001
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5
    ATTRIBUTES['n_elements'] = 4

    _attributes, _msg = Switch.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.1036000)
    assert _attributes['piQ'] == 10.0
    assert _attributes['piE'] == 8.0
    assert _attributes['piC'] == 0.0
    assert _attributes['piCYC'] == 5.0
    assert _attributes['piL'] == 1.0
    assert _attributes['piU'] == 0.0
    assert pytest.approx(_attributes['hazard_rate_active'], 4.1440000)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the quality ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 10
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5
    ATTRIBUTES['n_elements'] = 4

    _attributes, _msg = Switch.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'switch, hardware ID: 6.\n')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 10.0
    assert _attributes['piE'] == 8.0
    assert _attributes['piC'] == 0.0
    assert _attributes['piCYC'] == 5.0
    assert _attributes['piL'] == 1.0
    assert _attributes['piU'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the active environment ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 41
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['construction_id'] = 2
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5
    ATTRIBUTES['n_elements'] = 4

    _attributes, _msg = Switch.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piE is 0.0 when calculating switch, ' \
                    'hardware ID: 6.\n')
    assert pytest.approx(_attributes['lambda_b'], 0.1036000)
    assert _attributes['piQ'] == 10.0
    assert _attributes['piE'] == 0.0
    assert _attributes['piC'] == 0.0
    assert _attributes['piCYC'] == 5.0
    assert _attributes['piL'] == 1.0
    assert _attributes['piU'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [1.0, 0.5])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_current_overstress_harsh_environment(current_rated,
                                              environment_active_id):
    """overstressed() should return True when current ratio > 0.75 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.48
    ATTRIBUTES['current_rated'] = current_rated
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = 15.0
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if current_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif current_rated == 0.5:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating current > 75% rated '
                                         'current in harsh environment.\n')


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [1.0, 0.5])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_current_overstress_mild_environment(current_rated,
                                             environment_active_id):
    """overstressed() should return True when current ratio > 0.9 in a mild environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.48
    ATTRIBUTES['current_rated'] = current_rated
    ATTRIBUTES['voltage_ac_operating'] = 0.02
    ATTRIBUTES['voltage_dc_operating'] = 6.0
    ATTRIBUTES['temperature_rated_max'] = 150.0
    ATTRIBUTES['temperature_active'] = 48.7
    ATTRIBUTES['voltage_rated'] = 15.0
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if current_rated == 1.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif current_rated == 0.5:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating current > 90% rated '
                                         'current in mild environment.\n')
