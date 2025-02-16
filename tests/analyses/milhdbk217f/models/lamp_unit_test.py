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
@pytest.mark.usefixtures("test_attributes_lamp")
def test_set_default_values(
    test_attributes_lamp,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_lamp["rated_voltage"] = 0.0
    test_attributes_lamp["duty_cycle"] = -1.0
    _attributes = lamp.set_default_values(test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_voltage"] == 28.0
    assert _attributes["duty_cycle"] == 50.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_set_default_values_none_needed(
    test_attributes_lamp,
):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_lamp["rated_voltage"] = 12.0
    test_attributes_lamp["duty_cycle"] = 10.5
    _attributes = lamp.set_default_values(test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_voltage"] == 12.0
    assert _attributes["duty_cycle"] == 10.5


@pytest.mark.unit
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.usefixtures("test_attributes_lamp")
def test_get_part_count_lambda_b(
    application_id,
    environment_active_id,
    test_attributes_lamp,
):
    """Returns a float value for the base hazard rate on success."""
    test_attributes_lamp["application_id"] = application_id
    test_attributes_lamp["environment_active_id"] = environment_active_id
    _lambda_b = lamp.get_part_count_lambda_b(test_attributes_lamp)

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
@pytest.mark.usefixtures("test_attributes_lamp")
def test_get_part_count_lambda_b_invalid_application_id(
    test_attributes_lamp,
):
    """Raises a KeyError when passed an invalid application ID."""
    test_attributes_lamp["application_id"] = 5
    with pytest.raises(
        KeyError, match=r"get_part_count_lambda_b: Invalid lamp application ID 5."
    ):
        lamp.get_part_count_lambda_b(test_attributes_lamp)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_lamp,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_lamp["environment_active_id"] = 21
    with pytest.raises(
        IndexError, match=r"get_part_count_lambda_b: Invalid lamp environment ID 21."
    ):
        lamp.get_part_count_lambda_b(test_attributes_lamp)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_calculate_part_stress_lambda_b(
    test_attributes_lamp,
):
    """Returns a float value for the base hazard rate on success."""
    test_attributes_lamp["voltage_rated"] = 12.0
    _lambda_b = lamp.calculate_part_stress_lambda_b(test_attributes_lamp)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(1.8254735)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes_lamp")
def test_get_environment_factor(
    environment_id,
    test_attributes_lamp,
):
    """Returns the environment factor (piE) for the passed environment ID."""
    test_attributes_lamp["environment_active_id"] = environment_id
    _pi_e = lamp.get_environment_factor(test_attributes_lamp)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == [
            1.0,
            2.0,
            3.0,
            3.0,
            4.0,
            4.0,
            4.0,
            5.0,
            6.0,
            5.0,
            0.7,
            4.0,
            6.0,
            27.0,
        ][environment_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_lamp")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_lamp,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_lamp["environment_active_id"] = 27
    with pytest.raises(
        IndexError, match=r"get_environment_factor: Invalid lamp environment ID 27."
    ):
        lamp.get_environment_factor(test_attributes_lamp)


@pytest.mark.unit
@pytest.mark.parametrize("duty_cycle", [5.0, 50.0, 95.0])
@pytest.mark.parametrize("application_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_lamp")
def test_calculate_part_stress(
    duty_cycle,
    application_id,
    test_attributes_lamp,
):
    """calculate_part_stress() should return the attributes dict updated with the
    calculated values."""
    test_attributes_lamp["application_id"] = application_id
    test_attributes_lamp["duty_cycle"] = duty_cycle
    test_attributes_lamp["hazard_rate_active"] = 1.82547348
    _attributes = lamp.calculate_part_stress(test_attributes_lamp)

    assert isinstance(_attributes, dict)
    assert _attributes["piU"] == {5.0: 0.1, 50.0: 0.72, 95.0: 1.0}[duty_cycle]
    assert _attributes["piA"] == {1: 1.0, 2: 3.3}[application_id]
    if duty_cycle == 5.0 and application_id == 1:
        assert _attributes["hazard_rate_active"] == pytest.approx(0.18254735)
