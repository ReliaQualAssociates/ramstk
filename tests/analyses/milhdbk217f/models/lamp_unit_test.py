# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.lamp_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the lamp module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import lamp


@pytest.mark.unit
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(
    application_id,
    environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
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
def test_get_part_count_lambda_b_no_application():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown
    application ID."""
    with pytest.raises(KeyError):
        lamp.get_part_count_lambda_b(5, 2)


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown
    active environment ID."""
    with pytest.raises(IndexError):
        lamp.get_part_count_lambda_b(1, 21)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_calculate_part_count(test_attributes_lamp):
    """calculate_part_count() should return a float for the base hazard rate on
    success."""
    _lst_lambda_b = lamp.calculate_part_count(**test_attributes_lamp)

    assert isinstance(_lst_lambda_b, float)
    assert _lst_lambda_b == 12.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
@pytest.mark.parametrize("duty_cycle", [5.0, 50.0, 95.0])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_part_stress(
    duty_cycle,
    application_id,
    test_attributes_lamp,
):
    """calculate_part_stress() should return the attributes dict updated with the
    calculated values."""
    test_attributes_lamp["duty_cycle"] = duty_cycle
    test_attributes_lamp["application_id"] = application_id
    _attributes = lamp.calculate_part_stress(**test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(1.82547348)
    assert _attributes["piU"] == {5.0: 0.1, 50.0: 0.72, 95.0: 1.0}[duty_cycle]
    assert _attributes["piA"] == {1: 1.0, 2: 3.3}[application_id]
    if duty_cycle == 5.0 and application_id == 1:
        assert _attributes["hazard_rate_active"] == pytest.approx(0.18254735)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_set_default_values(test_attributes_lamp):
    """should set default values for each parameter <= 0.0."""
    test_attributes_lamp["rated_voltage"] = 0.0
    test_attributes_lamp["duty_cycle"] = -1.0
    _attributes = lamp.set_default_values(**test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_voltage"] == 28.0
    assert _attributes["duty_cycle"] == 50.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_set_default_values_none_needed(test_attributes_lamp):
    """should not set default values for each parameter > 0.0."""
    test_attributes_lamp["rated_voltage"] = 12.0
    test_attributes_lamp["duty_cycle"] = 10.5
    _attributes = lamp.set_default_values(**test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_voltage"] == 12.0
    assert _attributes["duty_cycle"] == 10.5
