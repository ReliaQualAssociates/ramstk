# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.filter_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the filter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import efilter

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
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(
    type_id,
    environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
    _lambda_b = efilter.get_part_count_lambda_b(type_id, environment_active_id)

    assert isinstance(_lambda_b, float)
    if type_id == 1:
        assert (
            _lambda_b
            == [
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
        )
    elif type_id == 2:
        assert (
            _lambda_b
            == [
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
        )
    elif type_id == 3:
        assert (
            _lambda_b
            == [
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
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown
    active environment ID."""
    with pytest.raises(IndexError):
        efilter.get_part_count_lambda_b(1, 28)


@pytest.mark.unit
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type
    ID."""
    with pytest.raises(KeyError):
        efilter.get_part_count_lambda_b(14, 8)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_part_count(environment_active_id, test_attributes_filter):
    """calculate_part_count() should return a float value for the base hazard rate on
    success."""
    test_attributes_filter["type_id"] = 1
    test_attributes_filter["environment_active_id"] = environment_active_id
    _lambda_b = efilter.calculate_part_count(**test_attributes_filter)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == [
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
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
@pytest.mark.parametrize("type_id", [1, 2, 3])
def test_calculate_part_stress(type_id, test_attributes_filter):
    """calculate_part_stress() should return a dictionary of updated values on
    success."""
    test_attributes_filter["type_id"] = type_id

    _attributes = efilter.calculate_part_stress(**test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert (
        _attributes["lambda_b"]
        == {
            1: 0.022,
            2: 0.12,
            3: 0.12,
            4: 0.27,
        }[type_id]
    )
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
@pytest.mark.usefixtures("test_attributes_filter")
def test_calculate_part_stress_missing_type(test_attributes_filter):
    """calculate_part_stress() should raise a KeyError if passed an unknown type ID."""
    test_attributes_filter["type_id"] = 6
    with pytest.raises(KeyError):
        efilter.calculate_part_stress(**test_attributes_filter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_set_default_values(test_attributes_filter):
    """should set default values for each parameter <= 0.0."""
    test_attributes_filter["quality_id"] = 0
    _attributes = efilter.set_default_values(**test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert _attributes["quality_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_set_default_values_none_needed(test_attributes_filter):
    """should set default values for each parameter <= 0.0."""
    test_attributes_filter["quality_id"] = 2
    _attributes = efilter.set_default_values(**test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert _attributes["quality_id"] == 2
