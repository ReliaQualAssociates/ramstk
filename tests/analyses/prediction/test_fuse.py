#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_fuse.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the fuse module."""

import pytest

from rtk.analyses.data import HARDWARE_ATTRIBUTES
from rtk.analyses.prediction import Fuse

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 10
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = [
    0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15, 0.18, 0.18, 0.009, 0.1,
    0.21, 2.3
]

PART_STRESS_PIE = [
    1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0, 0.9, 10.0, 21.0,
    230.0
]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
def test_calculate_mil_hdbk_217f_part_count(environment_active_id):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['environment_active_id'] = environment_active_id

    lambda_b = PART_COUNT_LAMBDA_B[environment_active_id - 1]

    _attributes, _msg = Fuse.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['hazard_rate_active'] == lambda_b


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['environment_active_id'] = 100

    _attributes, _msg = Fuse.calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: Base hazard rate is 0.0 when calculating '
                    'fuse, hardware ID: 6, active environment ID: 100')
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4

    _attributes, _msg = Fuse.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert _attributes['piE'] == 5.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.05)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and a non-empty message when the environment ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 40

    _attributes, _msg = Fuse.calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ('RTK WARNING: piE is 0.0 when calculating fuse, hardware '
                    'ID: 6')
    assert _attributes['piE'] == 0.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)
