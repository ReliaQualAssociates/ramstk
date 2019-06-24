# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_lamp.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the lamp module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES
from ramstk.analyses.prediction import Component, Lamp

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 10
ATTRIBUTES['subcategory_id'] = 4
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: [
        3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0, 23.0, 19.0, 2.7, 16.0,
        23.0, 100.0,
    ],
    2: [
        13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0, 77.0, 64.0, 9.0, 51.0,
        77.0, 350.0,
    ],
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        application_id,
        environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['application_id'] = application_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        lambda_b = PART_COUNT_LAMBDA_B[application_id][
            environment_active_id -
            1
        ]
    except (KeyError, IndexError):
        lambda_b = 0.0

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating lamp, hardware ID: 6, active environment '
            'ID: {0:d}.\n'
        ).format(environment_active_id)
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['hazard_rate_active'] == lambda_b


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating lamp, hardware '
        'ID: 6, active environment ID: 100.\n'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['voltage_rated'] = 12.0
    ATTRIBUTES['duty_cycle'] = 50.0

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['lambda_b'], 1.8254735)
    assert _attributes['piA'] == 1.0
    assert _attributes['piE'] == 3.0
    assert _attributes['piU'] == 0.72
    assert pytest.approx(_attributes['hazard_rate_active'], 3.9430227)


@pytest.mark.unit
def test_check_variable_zero():
    """_do_check_variables() should return a warning message when variables <= zero."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['hardware_id'] = 100
    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piA'] = 1.0
    ATTRIBUTES['piU'] = 1.0

    ATTRIBUTES['lambda_b'] = 0.0
    _msg = Lamp._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating lamp, ' \
        'hardware ID: 100, active environment ID: 4.\n'
    )

    ATTRIBUTES['lambda_b'] = 1.0
    ATTRIBUTES['piE'] = 0.0
    _msg = Lamp._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when ' \
            'calculating lamp, hardware ID: 100.\n'
    )

    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piA'] = 0.0
    _msg = Lamp._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piA is 0.0 when calculating lamp, hardware ID: ' \
        '100, application ID: 1.\n'
    )

    ATTRIBUTES['piA'] = 1.0
    ATTRIBUTES['piU'] = 0.0
    _msg = Lamp._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piU is 0.0 when calculating lamp, hardware ID: ' \
        '100, duty cycle: 50.000000.\n'
    )
