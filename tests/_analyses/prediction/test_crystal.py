#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_crystal.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the crystal module."""

import pytest
from tests.data import HARDWARE_ATTRIBUTES

from rtk.analyses.prediction import Crystal

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 10
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1
ATTRIBUTES['subcategory_id'] = 1

PART_COUNT_LAMBDA_B = [
    0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70, 0.90, 0.74, 0.016, 0.42,
    1.0, 16.0
]

PART_COUNT_PIQ = [1.0, 2.1]


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(quality_id, environment_active_id):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    lambda_b = PART_COUNT_LAMBDA_B[environment_active_id - 1]
    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when '
                        'calculating crystal, hardware ID: 6')
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'crystal, hardware ID: 6, subcategory ID: 1, active '
                    'environment ID: 100')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 100

    _attributes, _msg = Crystal.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating crystal, '
                    'hardware ID: 6 and quality ID: 100')
    assert _attributes['lambda_b'] == 0.032
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.1324630)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_frequency():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 0.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'crystal, hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.0)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 100
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piQ is 0.0 when calculating crystal, '
                    'hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 0.0
    assert _attributes['piE'] == 6.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """(TestConnectionModule) calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['frequency_operating'] = 10.0

    _attributes, _msg = Crystal.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piE is 0.0 when calculating crystal, '
                    'hardware ID: 6')
    assert pytest.approx(_attributes['lambda_b'], 0.02207717)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 0.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)
