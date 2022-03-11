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


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(environment_active_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
    _lambda_b = crystal.get_part_count_lambda_b(environment_active_id)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == [
            0.032,
            0.096,
            0.32,
            0.19,
            0.51,
            0.38,
            0.54,
            0.70,
            0.90,
            0.74,
            0.016,
            0.42,
            1.0,
            16.0,
        ][environment_active_id - 1]
    )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unkown
    active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = crystal.get_part_count_lambda_b(200)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_crystal")
@pytest.mark.parametrize(
    "environment_active_id",
    [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
    ],
)
def test_calculate_part_count(environment_active_id, test_attributes_crystal):
    """calculate_part_count() should return a float value for the base hazard rate on
    success."""
    test_attributes_crystal["environment_active_id"] = environment_active_id
    _lambda_b = crystal.calculate_part_count(**test_attributes_crystal)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == [
            0.032,
            0.096,
            0.32,
            0.19,
            0.51,
            0.38,
            0.54,
            0.70,
            0.90,
            0.74,
            0.016,
            0.42,
            1.0,
            16.0,
        ][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_crystal")
def test_calculate_part_stress(test_attributes_crystal):
    """calculate_part_stress() should return a dictionary of updated values on
    success."""
    test_attributes_crystal["piE"] = 6.0
    test_attributes_crystal["piQ"] = 2.0
    _attributes = crystal.calculate_part_stress(**test_attributes_crystal)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(0.022077167)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.26492601)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_crystal")
def test_calculate_mil_hdbk_217f_part_stress_missing_frequency(test_attributes_crystal):
    """calculate_part_stress() should return a base and active hazard rate = 0.0 when
    passed an operating frequency = 0.0, but won't raise an exception."""
    test_attributes_crystal["frequency_operating"] = 0.0
    _attributes = crystal.calculate_part_stress(**test_attributes_crystal)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == 0.0
    assert _attributes["hazard_rate_active"] == 0.0
