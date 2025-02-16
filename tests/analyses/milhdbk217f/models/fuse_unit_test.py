# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.fuse_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the fuse module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import fuse


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_set_default_values(
    test_attributes_fuse,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_fuse["lambda_b"] = 0.0
    _attributes = fuse.set_default_values(test_attributes_fuse)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == 0.01


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_set_default_values_none_needed(
    test_attributes_fuse,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_fuse["lambda_b"] = 0.005
    _attributes = fuse.set_default_values(test_attributes_fuse)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == 0.005


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(
    environment_active_id,
    test_attributes_fuse,
):
    """Return a float value for the parts count base hazard rate."""
    test_attributes_fuse["environment_active_id"] = environment_active_id

    _lambda_b = fuse.get_part_count_lambda_b(test_attributes_fuse)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == [
            0.01,
            0.02,
            0.06,
            0.05,
            0.11,
            0.09,
            0.12,
            0.15,
            0.18,
            0.18,
            0.009,
            0.1,
            0.21,
            2.3,
        ][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_fuse,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_fuse["environment_active_id"] = 1200
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid fuse environment ID 1200.",
    ):
        fuse.get_part_count_lambda_b(test_attributes_fuse)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_part_stress_lambda_b(
    test_attributes_fuse,
):
    """Returns a float value for the base hazard rate."""
    _lambda_b = fuse.get_part_stress_lambda_b(test_attributes_fuse)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.010


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_environment_factor(
    environment_active_id,
    test_attributes_fuse,
):
    """Return a float value for the environment factor."""
    test_attributes_fuse["environment_active_id"] = environment_active_id
    _pi_e = fuse.get_environment_factor(test_attributes_fuse)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            1: 1.0,
            2: 2.0,
            3: 8.0,
            4: 5.0,
            5: 11.0,
            6: 9.0,
            7: 12.0,
            8: 15.0,
            9: 18.0,
            10: 16.0,
            11: 0.9,
            12: 10.0,
            13: 21.0,
            14: 230.0,
        }[environment_active_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_fuse,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_fuse["environment_active_id"] = 62
    with pytest.raises(
        IndexError, match=r"get_environment_factor: Invalid fuse environment ID 62."
    ):
        fuse.get_environment_factor(test_attributes_fuse)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_fuse")
def test_calculate_part_stress(
    test_attributes_fuse,
):
    """Returns a dict of updated values on success."""
    test_attributes_fuse["hazard_rate_active"] = 0.01
    _attributes = fuse.calculate_part_stress(test_attributes_fuse)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == 0.01
