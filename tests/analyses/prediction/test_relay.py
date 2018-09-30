#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_relay.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the relay module."""

import pytest

from ramstk.analyses.data import HARDWARE_ATTRIBUTES
from ramstk.analyses.prediction import Relay, Component

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Doyle "weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 6
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: [[
        0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5, 10.0,
        0.0
    ], [
        0.43, 0.89, 6.9, 3.6, 12.0, 3.4, 4.4, 6.2, 6.7, 22.0, 0.21, 11.0, 32.0,
        0.0
    ], [
        0.13, 0.26, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5, 10.0,
        0.0
    ], [
        0.11, 0.23, 1.8, 0.92, 3.3, 0.96, 1.2, 2.1, 2.3, 6.5, 0.54, 3.0, 9.0,
        0.0
    ], [
        0.29, 0.60, 4.8, 2.4, 8.2, 2.3, 2.9, 4.1, 4.5, 15.0, 0.14, 7.6, 22.0,
        0.0
    ], [
        0.88, 1.8, 14.0, 7.4, 26.0, 7.1, 9.1, 13.0, 14.0, 46.0, 0.44, 24.0,
        67.0, 0.0
    ]],
    2: [[
        0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2, 0.16, 4.8, 13.0,
        240.0
    ], [
        0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0, 12.0, 0.20, 5.0, 17.0,
        300.0
    ]]
}

PART_COUNT_PIQ = {1: [0.6, 3.0, 9.0], 2: [0.0, 1.0, 4.0]}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("quality_id", [1, 2, 3])
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

    try:
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][type_id - 1][
            environment_active_id - 1]
    except (KeyError, IndexError):
        lambda_b = 0.0

    try:
        piQ = PART_COUNT_PIQ[subcategory_id][quality_id - 1]
    except (KeyError, IndexError):
        piQ = 0.0

    _attributes, _msg = Relay.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0 and piQ > 0.0:
        assert _msg == ('RAMSTK WARNING: Base hazard rate is 0.0 when '
                        'calculating relay, hardware ID: 6, subcategory '
                        'ID: {0:d}, type ID: {1:d}, and active '
                        'environment ID: {2:d}.\n').format(
                            subcategory_id, type_id, environment_active_id)
    elif piQ == 0.0:
        assert _msg == ('RAMSTK WARNING: piQ is 0.0 when calculating relay, '
                        'hardware ID: 6, subcategory ID: {0:d}, and quality '
                        'ID: {1:d}.').format(subcategory_id, quality_id)
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
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['family_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Relay.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: piQ is 0.0 when calculating relay, '
                    'hardware ID: 6, subcategory ID: 0, and quality ID: 1.')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_type():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the type ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 10
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Relay.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating relay, '
        'hardware ID: 6, subcategory ID: 1, type ID: 10, and active '
        'environment ID: 1.\n')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Relay.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'relay, hardware ID: 6, subcategory ID: 1, type ID: 1, and '
        'active environment ID: 100.\n')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.6
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['contact_rating_id'] = 2
    ATTRIBUTES['application_id'] = 4
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['contact_form_id'] = 2
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5

    _attributes, _msg = Relay.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['current_ratio'], 0.3)
    assert pytest.approx(_attributes['lambda_b'], 0.006166831)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 6.0
    assert _attributes['piC'] == 0.0
    assert _attributes['piCYC'] == 0.0
    assert _attributes['piL'] == 0.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0037000986)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the quality ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 10
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['contact_rating_id'] = 2
    ATTRIBUTES['application_id'] = 4
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['contact_form_id'] = 2
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5

    _attributes, _msg = Relay.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: piQ is 0.0 when calculating relay, hardware '
                    'ID: 6')
    assert pytest.approx(_attributes['current_ratio'], 0.3)
    assert pytest.approx(_attributes['lambda_b'], 0.006166831)
    assert _attributes['piQ'] == 0.0
    assert _attributes['piE'] == 24.0
    assert _attributes['piC'] == 1.5
    assert _attributes['piCYC'] == 1.0
    assert pytest.approx(_attributes['piL'], 0.14062499)
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the active environment ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 40
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['insulation_id'] = 3
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['contact_rating_id'] = 2
    ATTRIBUTES['application_id'] = 4
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['contact_form_id'] = 2
    ATTRIBUTES['current_rated'] = 5.0
    ATTRIBUTES['current_operating'] = 1.5
    ATTRIBUTES['n_cycles'] = 5

    _attributes, _msg = Relay.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RAMSTK WARNING: piE is 0.0 when calculating relay, hardware '
                    'ID: 6')
    assert pytest.approx(_attributes['current_ratio'], 0.3)
    assert pytest.approx(_attributes['lambda_b'], 0.006166831)
    assert _attributes['piQ'] == 0.1
    assert _attributes['piE'] == 0.0
    assert _attributes['piC'] == 1.5
    assert _attributes['piCYC'] == 1.0
    assert pytest.approx(_attributes['piL'], 0.14062499)
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [0.5, 0.2])
@pytest.mark.parametrize("environment_active_id",
                         [3, 5, 6, 7, 8, 9, 10, 12, 13, 14])
def test_current_overstress_harsh_environment(current_rated,
                                              environment_active_id):
    """overstressed() should return True when current ratio > 0.75 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.18
    ATTRIBUTES['current_rated'] = current_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(**_attributes)

    assert isinstance(_attributes, dict)
    if current_rated == 0.5:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif current_rated == 0.2:
        assert _attributes['overstress']
        assert _attributes['reason'] == ('1. Operating current > 75% rated '
                                         'current in harsh environment.\n')


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("current_rated", [1.0, 0.5])
@pytest.mark.parametrize("environment_active_id", [1, 2, 4, 11])
def test_current_overstress_mild_environment(current_rated,
                                             environment_active_id):
    """overstressed() should return True when current ratio > 0.9 in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.48
    ATTRIBUTES['current_rated'] = current_rated
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
