# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_filter.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the filter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES
from ramstk.analyses.prediction import Component, Filter

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 10
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1
ATTRIBUTES['subcategory_id'] = 2

PART_COUNT_LAMBDA_B = {
    1: [
        0.022, 0.044, 0.13, 0.088, 0.20, 0.15, 0.20, 0.24, 0.29, 0.24, 0.018,
        0.15, 0.33, 2.6,
    ],
    2: [
        0.12, 0.24, 0.72, 0.48, 1.1, 0.84, 1.1, 1.3, 1.6, 1.3, 0.096, 0.84,
        1.8, 1.4,
    ],
    3:
    [0.27, 0.54, 1.6, 1.1, 2.4, 1.9, 2.4, 3.0, 3.5, 3.0, 0.22, 1.9, 4.1, 32.0],
}

PART_COUNT_PIQ = [1.0, 2.9]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        type_id, quality_id,
        environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['type_id'] = type_id
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    lambda_b = PART_COUNT_LAMBDA_B[type_id][environment_active_id - 1]
    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating filter, hardware ID: 6.\n'
        )
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_type():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the type ID is missing."""
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 9

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'filter, hardware ID: 6, type ID: 9, active environment '
        'ID: 1.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'filter, hardware ID: 6, type ID: 1, active environment '
        'ID: 100.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['environment_active_id'] = 1
    ATTRIBUTES['quality_id'] = 4
    ATTRIBUTES['type_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert _attributes['lambda_b'] == 0.022
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.022


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 2

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.12)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 4.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.48)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_type():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and non-empty message when the type ID is not in the dictionary."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 6

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
                   'calculating filter, hardware ID: 6, type ID: 6, active ' \
                   'environment ID: 4.\n'
    assert pytest.approx(_attributes['lambda_b'], 0.0)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 4.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_quality():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and non-empty message when the quality ID is not an index in the list."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 10
    ATTRIBUTES['type_id'] = 2

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.012)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 4.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.048)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_missing_environment():
    """calculate_mil_hdbk_217f_part_stress() should return a zero active hazard rate and non-empty message when the environment ID is not an index in the list."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 40
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['type_id'] = 2

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 0.012)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 1.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.012)


@pytest.mark.unit
def test_check_variable_zero():
    """do_check_variables() should return a warning message when variables <= zero."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['hardware_id'] = 100
    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piQ'] = 1.0

    ATTRIBUTES['lambda_b'] = -1.3
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating filter, ' \
        'hardware ID: 100, type ID: 2, active environment ID: 40.\n'
    )

    ATTRIBUTES['lambda_b'] = 0.0
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating filter, ' \
        'hardware ID: 100, type ID: 2, active environment ID: 40.\n'
    )

    ATTRIBUTES['lambda_b'] = 1.0
    ATTRIBUTES['piQ'] = -1.3
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating filter, hardware ' \
        'ID: 100, quality ID: 1.\n'
    )

    ATTRIBUTES['piQ'] = 0.0
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating filter, hardware ' \
        'ID: 100, quality ID: 1.\n'
    )

    ATTRIBUTES['piQ'] = 1.0
    ATTRIBUTES['piE'] = -1.3
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating filter, hardware ' \
        'ID: 100.\n'
    )

    ATTRIBUTES['piE'] = 0.0
    _msg = Filter.do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating filter, hardware ' \
        'ID: 100.\n'
    )
