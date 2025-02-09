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


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_set_default_values(
    test_attributes_filter,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_filter["quality_id"] = 0
    _attributes = efilter.set_default_values(**test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert _attributes["quality_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_set_default_values_none_needed(
    test_attributes_filter,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_filter["quality_id"] = 2
    _attributes = efilter.set_default_values(**test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert _attributes["quality_id"] == 2


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_part_count_lambda_b(
    environment_active_id,
    type_id,
    test_attributes_filter,
):
    """Return a float value for the base hazard rate on success."""
    test_attributes_filter["environment_active_id"] = environment_active_id
    test_attributes_filter["type_id"] = type_id

    _lambda_b = efilter.get_part_count_lambda_b(test_attributes_filter)

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
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_filter,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_filter["environment_active_id"] = 28
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid electronic filter environment ID 28.",
    ):
        efilter.get_part_count_lambda_b(test_attributes_filter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_part_count_lambda_b_invalid_type_id(
    test_attributes_filter,
):
    """Raise a KeyError when passed an invalid type ID."""
    test_attributes_filter["type_id"] = 14
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid electronic filter type ID 14.",
    ):
        efilter.get_part_count_lambda_b(test_attributes_filter)


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4])
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_part_stress_lambda_b(
    type_id,
    test_attributes_filter,
):
    """Returns a float for the part stress base hazard rate."""
    test_attributes_filter["type_id"] = type_id
    _lambda_b = efilter.get_part_stress_lambda_b(test_attributes_filter)

    assert _lambda_b == {1: 0.022, 2: 0.12, 3: 0.12, 4: 0.27}[type_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_part_stress_lambda_b_invalid_type_id(
    test_attributes_filter,
):
    """Raises a KeyError when passed an invalid type ID."""
    test_attributes_filter["type_id"] = 14
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_lambda_b: Invalid electronic filter type ID 14.",
    ):
        efilter.get_part_stress_lambda_b(test_attributes_filter)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_quality_factor(
    quality_id,
    test_attributes_filter,
):
    """Returns a float value for the passed quality ID."""
    test_attributes_filter["quality_id"] = quality_id
    _pi_q = efilter.get_quality_factor(test_attributes_filter)

    assert isinstance(_pi_q, float)
    assert (
        _pi_q
        == {
            1: 1.0,
            2: 2.9,
        }[quality_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_quality_factor_invalid_quality_id(
    test_attributes_filter,
):
    """Returns a float value for the passed quality ID."""
    test_attributes_filter["quality_id"] = 13
    with pytest.raises(
        IndexError,
        match=r"get_quality_factor: Invalid electronic filter quality ID 13.",
    ):
        efilter.get_quality_factor(test_attributes_filter)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_environment_factor(
    environment_id,
    test_attributes_filter,
):
    """Returns a float value for the passed environment ID."""
    test_attributes_filter["environment_active_id"] = environment_id
    _pi_e = efilter.get_environment_factor(test_attributes_filter)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            1: 1.0,
            2: 2.0,
            3: 6.0,
            4: 4.0,
            5: 9.0,
            6: 7.0,
            7: 9.0,
            8: 11.0,
            9: 13.0,
            10: 11.0,
            11: 0.8,
            12: 7.0,
            13: 15.0,
            14: 120.0,
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_filter,
):
    """Returns a float value for the passed environment ID."""
    test_attributes_filter["environment_active_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid electronic filter environment ID 22.",
    ):
        efilter.get_environment_factor(test_attributes_filter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_calculate_part_stress(
    test_attributes_filter,
):
    """Returns a dict of updated values on success."""
    test_attributes_filter["hazard_rate_active"] = 0.022
    test_attributes_filter["piE"] = 4
    test_attributes_filter["piQ"] = 1

    _attributes = efilter.calculate_part_stress(test_attributes_filter)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.088)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_filter")
def test_calculate_part_stress_missing_type(
    test_attributes_filter,
):
    """Raises a KeyError if one or more inputs are missing."""
    test_attributes_filter["hazard_rate_active"] = 0.022
    test_attributes_filter["piQ"] = 1
    test_attributes_filter.pop("piE")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required electronic filter "
        r"attribute: \'piE\'.",
    ):
        efilter.calculate_part_stress(test_attributes_filter)
