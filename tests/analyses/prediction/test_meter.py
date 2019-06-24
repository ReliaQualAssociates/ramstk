# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_meter.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the meter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES
from ramstk.analyses.prediction import Component, Meter

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 9
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: [
        [
            10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0, 160.0, 250.0, 260.0, 5.0,
            140.0, 380.0, 0.0,
        ], [
            15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0, 240.0, 375.0, 390.0, 7.5,
            210.0, 570.0, 0.0,
        ], [
            40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0, 640.0, 1000.0, 1040.0,
            20.0, 560.0, 1520.0, 0.0,
        ],
    ],
    2: [
        [
            0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6, 5.4, 0.099, 5.4, 0.0,
            0.0,
        ], [
            0.15, 0.61, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0, 9.2, 0.17, 9.2, 0.0,
            0.0,
        ],
    ],
}

PART_COUNT_PIQ = {2: [1.0, 3.4]}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.parametrize("quality_id", [1, 2])
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
        lambda_b = PART_COUNT_LAMBDA_B[subcategory_id][type_id - 1][
            environment_active_id - 1
        ]
    except (KeyError, IndexError):
        lambda_b = 0.0

    try:
        piQ = PART_COUNT_PIQ[subcategory_id][quality_id - 1]
    except (KeyError, IndexError):
        piQ = 1.0

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, '
            'hardware ID: 6, subcategory ID: {0:d}, type ID: {2:d}, and '
            'active environment ID: {1:d}.\n'
        ).format(
            subcategory_id,
            environment_active_id, type_id,
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
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        "RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, "
        "hardware ID: 6, subcategory ID: 0, type ID: 1, and active "
        "environment ID: 1.\n"
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_type():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the family ID is missing and needed."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 10
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        "RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, "
        "hardware ID: 6, subcategory ID: 1, type ID: 10, and active "
        "environment ID: 1.\n"
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'], 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['environment_active_id'] = 100
    ATTRIBUTES['quality_id'] = 1

    _attributes, _msg = Component.do_calculate_217f_part_count(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == (
        "RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, "
        "hardware ID: 6, subcategory ID: 1, type ID: 1, and active "
        "environment ID: 100.\n"
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 1.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_elapsed_time_meter():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['application_id'] = 2
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == 'RAMSTK WARNING: piA is 0.0 when calculating meter, ' \
                    'hardware ID: 6, type ID: 2.\n' \
                    'RAMSTK WARNING: piF is 0.0 when calculating meter, ' \
                    'hardware ID: 6, application ID: 2.\n'
    assert pytest.approx(_attributes['lambda_b'], 0.09)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 7.0
    assert pytest.approx(_attributes['hazard_rate_active'], 1.836)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_panel_meter():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['application_id'] = 2
    ATTRIBUTES['construction_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['power_operating'] = 4.2
    ATTRIBUTES['weight'] = 0.75

    _attributes, _msg = Component.do_calculate_217f_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == 'RAMSTK WARNING: piF is 0.0 when calculating meter, ' \
                   'hardware ID: 6, active temperature: 32.000000, and max '\
                   'rated temperature: 85.000000.\n'
    assert pytest.approx(_attributes['lambda_b'], 0.09)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 12.0
    assert _attributes['piA'] == 1.7
    assert _attributes['piF'] == 1.0
    assert pytest.approx(_attributes['hazard_rate_active'], 1.836)


@pytest.mark.unit
def test_check_variable_zero():
    """_do_check_variables() should return a warning message when variables <= zero."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['hardware_id'] = 100
    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piA'] = 1.0
    ATTRIBUTES['piF'] = 1.0
    ATTRIBUTES['piQ'] = 1.0
    ATTRIBUTES['piT'] = 1.0

    ATTRIBUTES['lambda_b'] = -1.3
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, ' \
        'hardware ID: 100, subcategory ID: 2, type ID: 2, and active ' \
        'environment ID: 4.\n'
    )

    ATTRIBUTES['lambda_b'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating meter, ' \
        'hardware ID: 100, subcategory ID: 2, type ID: 2, and active ' \
        'environment ID: 4.\n'
    )

    ATTRIBUTES['lambda_b'] = 1.0
    ATTRIBUTES['piE'] = -1.3
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating meter, hardware ID: ' \
        '100, active environment ID: 4.\n'
    )

    ATTRIBUTES['piE'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piE is 0.0 when calculating meter, hardware ID: ' \
        '100, active environment ID: 4.\n'
    )

    ATTRIBUTES['piE'] = 1.0
    ATTRIBUTES['piA'] = -1.3
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piA is 0.0 when calculating meter, hardware ID: ' \
        '100, type ID: 2.\n'
    )

    ATTRIBUTES['piA'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piA is 0.0 when calculating meter, hardware ID: ' \
        '100, type ID: 2.\n'
    )

    ATTRIBUTES['piA'] = 1.0
    ATTRIBUTES['piF'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piF is 0.0 when calculating meter, hardware ID: ' \
        '100, application ID: 2.\n'
    )

    ATTRIBUTES['piF'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piF is 0.0 when calculating meter, hardware ID: ' \
        '100, application ID: 2.\n'
    )

    ATTRIBUTES['piF'] = 1.0
    ATTRIBUTES['piQ'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating meter, hardware ID: ' \
        '100, quality ID: 1.\n'
    )

    ATTRIBUTES['piQ'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating meter, hardware ID: ' \
        '100, quality ID: 1.\n'
    )

    ATTRIBUTES['piQ'] = 1.0
    ATTRIBUTES['piT'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piF is 0.0 when calculating meter, hardware ID: ' \
        '100, active temperature: 32.000000, and max rated ' \
        'temperature: 85.000000.\n'
    )

    ATTRIBUTES['piT'] = 0.0
    _msg = Meter._do_check_variables(ATTRIBUTES)
    assert _msg == (
        'RAMSTK WARNING: piF is 0.0 when calculating meter, hardware ID: ' \
        '100, active temperature: 32.000000, and max rated ' \
        'temperature: 85.000000.\n'
    )
