# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_filter.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the filter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import efilter

ATTRIBUTES = {
    "category_id": 10,
    "subcategory_id": 2,
    "environment_active_id": 1,
    "type_id": 1,
    "piQ": 1.0,
    "piE": 4.0,
}

PART_COUNT_LAMBDA_B = {
    1: [
        0.022,
        0.044,
        0.13,
        0.088,
        0.20,
        0.15,
        0.20,
        0.24,
        0.29,
        0.24,
        0.018,
        0.15,
        0.33,
        2.6,
    ],
    2: [
        0.12,
        0.24,
        0.72,
        0.48,
        1.1,
        0.84,
        1.1,
        1.3,
        1.6,
        1.3,
        0.096,
        0.84,
        1.8,
        1.4,
    ],
    3: [
        0.27,
        0.54,
        1.6,
        1.1,
        2.4,
        1.9,
        2.4,
        3.0,
        3.5,
        3.0,
        0.22,
        1.9,
        4.1,
        32.0,
    ],
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(
    type_id,
    environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base
    hazard rate on success."""
    _lambda_b = efilter.get_part_count_lambda_b(type_id, environment_active_id)

    assert isinstance(_lambda_b, float)
    if type_id == 1:
        assert _lambda_b == [
            0.022,
            0.044,
            0.13,
            0.088,
            0.20,
            0.15,
            0.20,
            0.24,
            0.29,
            0.24,
            0.018,
            0.15,
            0.33,
            2.6,
        ][environment_active_id - 1]
    elif type_id == 2:
        assert _lambda_b == [
            0.12,
            0.24,
            0.72,
            0.48,
            1.1,
            0.84,
            1.1,
            1.3,
            1.6,
            1.3,
            0.096,
            0.84,
            1.8,
            1.4,
        ][environment_active_id - 1]
    elif type_id == 3:
        assert _lambda_b == [
            0.27,
            0.54,
            1.6,
            1.1,
            2.4,
            1.9,
            2.4,
            3.0,
            3.5,
            3.0,
            0.22,
            1.9,
            4.1,
            32.0,
        ][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an
    unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = efilter.get_part_count_lambda_b(1, 28)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown
    type ID."""
    with pytest.raises(KeyError):
        _lambda_b = efilter.get_part_count_lambda_b(14, 8)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_part_count(
    environment_active_id,
):
    """calculate_part_count() should return a float value for the base hazard
    rate on success."""
    ATTRIBUTES["type_id"] = 1
    ATTRIBUTES["environment_active_id"] = environment_active_id
    _lambda_b = efilter.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == [
        0.022,
        0.044,
        0.13,
        0.088,
        0.20,
        0.15,
        0.20,
        0.24,
        0.29,
        0.24,
        0.018,
        0.15,
        0.33,
        2.6,
    ][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("type_id", [1, 2, 3])
def test_calculate_part_stress(type_id):
    """calculate_part_stress() should return a dictionary of updated values on
    success."""
    ATTRIBUTES["type_id"] = type_id

    _attributes = efilter.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == {
        1: 0.022,
        2: 0.12,
        3: 0.12,
        4: 0.27,
    }[type_id]
    assert (
        _attributes["hazard_rate_active"]
        == {
            1: 0.022,
            2: 0.12,
            3: 0.12,
            4: 0.27,
        }[type_id]
        * 4.0
    )


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_missing_type():
    """calculate_part_stress() should raise a KeyError if passed an unknown
    type ID."""
    ATTRIBUTES["type_id"] = 6
    with pytest.raises(KeyError):
        _attributes = efilter.calculate_part_stress(**ATTRIBUTES)
