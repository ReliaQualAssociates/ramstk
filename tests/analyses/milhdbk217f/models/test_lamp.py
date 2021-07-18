# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_lamp.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the lamp module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import lamp

ATTRIBUTES = {
    "category_id": 10,
    "subcategory_id": 4,
    "environment_active_id": 3,
    "application_id": 1,
    "duty_cycle": 75.0,
    "voltage_rated": 12.0,
    "piE": 1.0,
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(
    application_id,
    environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = lamp.get_part_count_lambda_b(application_id, environment_active_id)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
                3.9,
                7.8,
                12.0,
                12.0,
                16.0,
                16.0,
                16.0,
                19.0,
                23.0,
                19.0,
                2.7,
                16.0,
                23.0,
                100.0,
            ],
            2: [
                13.0,
                26.0,
                38.0,
                38.0,
                51.0,
                51.0,
                51.0,
                64.0,
                77.0,
                64.0,
                9.0,
                51.0,
                77.0,
                350.0,
            ],
        }[application_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_application():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown application ID."""
    with pytest.raises(KeyError):
        _lambda_b = lamp.get_part_count_lambda_b(5, 2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = lamp.get_part_count_lambda_b(1, 21)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float for the base hazard rate on success."""
    _lst_lambda_b = lamp.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lst_lambda_b, float)
    assert _lst_lambda_b == 12.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("duty_cycle", [5.0, 50.0, 95.0])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_part_stress(duty_cycle, application_id):
    """calculate_part_stress() should return the attributes dict updated with the calculated values."""
    ATTRIBUTES["duty_cycle"] = duty_cycle
    ATTRIBUTES["application_id"] = application_id
    _attributes = lamp.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(1.82547348)
    assert _attributes["piU"] == {5.0: 0.1, 50.0: 0.72, 95.0: 1.0}[duty_cycle]
    assert _attributes["piA"] == {1: 1.0, 2: 3.3}[application_id]
    if duty_cycle == 5.0 and application_id == 1:
        assert _attributes["hazard_rate_active"] == pytest.approx(0.18254735)
