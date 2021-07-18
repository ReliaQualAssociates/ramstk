# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_fuse.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the fuse module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import fuse

ATTRIBUTES = {
    "category_id": 10,
    "subcategory_id": 3,
    "environment_active_id": 1,
    "piE": 1.0,
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(environment_active_id):
    """get_part_count_lambda_b() should return a dictionary of updated values
    on success."""
    ATTRIBUTES["environment_active_id"] = environment_active_id

    _lambda_b = fuse.get_part_count_lambda_b(environment_active_id)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == [
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


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an
    unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = fuse.get_part_count_lambda_b(1200)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float base hazard rates on
    success."""
    _lambda_b = fuse.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 2.3


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress():
    """calculate_part_stress() should return a dictionary of updated values on
    success."""
    _attributes = fuse.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == 0.01
