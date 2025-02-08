# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.crystal_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the crystal module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import crystal
from tests.analyses.milhdbk217f.models.conftest import test_attributes_crystal


@pytest.mark.unit
def test_set_default_values(
    test_attributes_crystal,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_crystal["frequency_operating"] = -50.0
    _attributes = crystal.set_default_values(test_attributes_crystal)

    assert isinstance(_attributes, dict)
    assert test_attributes_crystal["frequency_operating"] == pytest.approx(50.0)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_crystal")
def test_set_default_values_none_needed(
    test_attributes_crystal,
):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_crystal["frequency_operating"] = 10.6
    _attributes = crystal.set_default_values(test_attributes_crystal)

    assert isinstance(_attributes, dict)
    assert _attributes["frequency_operating"] == 10.6


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
def test_get_part_count_lambda_b(
    environment_active_id,
    test_attributes_crystal,
):
    """Returns a float value for the base hazard rate."""
    test_attributes_crystal["environment_active_id"] = environment_active_id
    _lambda_b = crystal.get_part_count_lambda_b(test_attributes_crystal)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: 0.032,
            2: 0.096,
            3: 0.32,
            4: 0.19,
            5: 0.51,
            6: 0.38,
            7: 0.54,
            8: 0.70,
            9: 0.90,
            10: 0.74,
            11: 0.016,
            12: 0.42,
            13: 1.0,
            14: 16.0,
        }[environment_active_id]
    )


@pytest.mark.unit
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_crystal,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_crystal["environment_active_id"] = 200
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid crystal environment ID 200.",
    ):
        crystal.get_part_count_lambda_b(test_attributes_crystal)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
def test_get_part_count_quality_factor(
    quality_id,
    test_attributes_crystal,
):
    """Returns the quality factor (piQ) for the selected quality ID."""
    test_attributes_crystal["quality_id"] = quality_id
    _pi_q = crystal.get_part_count_quality_factor(test_attributes_crystal)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 1.0, 2: 3.4}[quality_id]


@pytest.mark.unit
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_crystal,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_crystal["quality_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid crystal quality ID 22.",
    ):
        crystal.get_part_count_quality_factor(test_attributes_crystal)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5])
def test_get_part_stress_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_crystal,
):
    """Returns the quality factor (piQ) for the selected quality ID."""
    test_attributes_crystal["quality_id"] = quality_id
    test_attributes_crystal["subcategory_id"] = subcategory_id
    _pi_q = crystal.get_part_stress_quality_factor(test_attributes_crystal)

    assert isinstance(_pi_q, float)
    assert (
        _pi_q
        == {
            1: {1: 1.0, 2: 1.0},
            2: {1: 1.0, 2: 1.0},
            3: {1: 1.0, 2: 1.0},
            4: {1: 1.0, 2: 2.1},
            5: {1: 1.0, 2: 2.1},
        }[subcategory_id][quality_id]
    )


@pytest.mark.unit
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_crystal,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_crystal["quality_id"] = 22
    test_attributes_crystal["subcategory_id"] = 4
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid crystal quality ID 22.",
    ):
        crystal.get_part_stress_quality_factor(test_attributes_crystal)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b(
    test_attributes_crystal,
):
    """Returns a float value for the base hazard rate."""
    test_attributes_crystal["frequency_operating"] = 10.0
    _lambda_b = crystal.calculate_part_stress_lambda_b(test_attributes_crystal)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(0.02207717)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_negative_frequency(
    test_attributes_crystal,
):
    """Returns a 0.0 for the base hazard rate when passed a negative frequency."""
    test_attributes_crystal["frequency_operating"] = -10.0
    _lambda_b = crystal.calculate_part_stress_lambda_b(test_attributes_crystal)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(0.0)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
def test_get_environment_factor(
    environment_active_id,
    test_attributes_crystal,
):
    """Returns a float value associated with the environment ID."""
    test_attributes_crystal["environment_active_id"] = environment_active_id
    _pi_e = crystal.get_environment_factor(test_attributes_crystal)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            1: 1.0,
            2: 3.0,
            3: 10.0,
            4: 6.0,
            5: 16.0,
            6: 12.0,
            7: 17.0,
            8: 22.0,
            9: 28.0,
            10: 23.0,
            11: 0.5,
            12: 13.0,
            13: 32.0,
            14: 500.0,
        }[environment_active_id]
    )


@pytest.mark.unit
def test_get_environment_factor_invalid_environment_id(
    test_attributes_crystal,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_crystal["environment_active_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid crystal environment ID 22.",
    ):
        crystal.get_environment_factor(test_attributes_crystal)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_crystal")
def test_calculate_part_stress(
    test_attributes_crystal,
):
    """Returns a dict of updated values."""
    test_attributes_crystal["hazard_rate_active"] = 0.022077167
    test_attributes_crystal["piE"] = 6.0
    test_attributes_crystal["piQ"] = 2.1
    _attributes = crystal.calculate_part_stress(test_attributes_crystal)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.2781723)
