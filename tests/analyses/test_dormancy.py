# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_dormancy.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the dormancy analysis module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.dormancy import (
    do_calculate_dormant_hazard_rate,
    get_dormant_hr_multiplier,
    get_environment_type,
)


@pytest.mark.unit
@pytest.mark.parametrize("active_env", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
def test_get_environment_type_active(active_env):
    """get_environment_type() should return a string value for the active environment
    type."""
    _active_env = get_environment_type(active_env, True)

    assert isinstance(_active_env, str)
    assert (
        _active_env
        == [
            "ground",
            "ground",
            "ground",
            "naval",
            "naval",
            "airborne",
            "airborne",
            "airborne",
            "airborne",
            "airborne",
            "space",
            "missile",
            "missile",
        ][active_env - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("dormant_env", [1, 2, 3, 4])
def test_get_environment_type_dormant(dormant_env):
    """get_environment_type() should return a string value for the dormant environment
    type."""
    _dormant_env = get_environment_type(dormant_env, False)

    assert isinstance(_dormant_env, str)
    assert (
        _dormant_env
        == [
            "ground",
            "naval",
            "airborne",
            "space",
        ][dormant_env - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8])
def test_get_dormant_hr_multiplier_ground(category_id):
    """get_dormant_hr_multiplier() should return a float value for the multiplier with
    active ground environment."""
    _hr_multiplier = get_dormant_hr_multiplier(
        [category_id, 1, 0.0], "ground", "ground"
    )

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.08, [0.04, 0.05], 0.2, 0.1, 0.2, 0.2, 0.4, 0.005][category_id - 1][0]
        )
    else:
        assert (
            _hr_multiplier
            == [0.08, [0.04, 0.05], 0.2, 0.1, 0.2, 0.2, 0.4, 0.005][category_id - 1]
        )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8])
def test_get_dormant_hr_multiplier_airborne(category_id):
    """get_dormant_hr_multiplier() should return a float value for the multiplier with
    active airborne environment."""
    _hr_multiplier = get_dormant_hr_multiplier(
        [category_id, 1, 0.0], "airborne", "airborne"
    )

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.06, [0.05, 0.06], 0.06, 0.1, 0.2, 0.2, 0.2, 0.005][category_id - 1][0]
        )

    else:
        assert (
            _hr_multiplier
            == [0.06, [0.05, 0.06], 0.06, 0.1, 0.2, 0.2, 0.2, 0.005][category_id - 1]
        )

    _hr_multiplier = get_dormant_hr_multiplier(
        [category_id, 1, 0.0], "airborne", "ground"
    )

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.04, [0.01, 0.02], 0.03, 0.03, 0.2, 0.04, 0.1, 0.003][category_id - 1][
                0
            ]
        )

    else:
        assert (
            _hr_multiplier
            == [0.04, [0.01, 0.02], 0.03, 0.03, 0.2, 0.04, 0.1, 0.003][category_id - 1]
        )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8])
def test_get_dormant_hr_multiplier_naval(category_id):
    """get_dormant_hr_multiplier() should return a float value for the multiplier with
    active naval environment."""
    _hr_multiplier = get_dormant_hr_multiplier([category_id, 1, 0.0], "naval", "naval")

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.06, [0.04, 0.05], 0.1, 0.1, 0.3, 0.3, 0.4, 0.008][category_id - 1][0]
        )

    else:
        assert (
            _hr_multiplier
            == [0.06, [0.04, 0.05], 0.1, 0.1, 0.3, 0.3, 0.4, 0.008][category_id - 1]
        )

    _hr_multiplier = get_dormant_hr_multiplier([category_id, 1, 0.0], "naval", "ground")

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.05, [0.03, 0.03], 0.06, 0.04, 0.3, 0.08, 0.2, 0.003][category_id - 1][
                0
            ]
        )

    else:
        assert (
            _hr_multiplier
            == [0.05, [0.03, 0.03], 0.06, 0.04, 0.3, 0.08, 0.2, 0.003][category_id - 1]
        )


@pytest.mark.unit
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8])
def test_get_dormant_hr_multiplier_space(category_id):
    """get_dormant_hr_multiplier() should return a float value for the multiplier with
    active space environment."""
    _hr_multiplier = get_dormant_hr_multiplier([category_id, 1, 0.0], "space", "space")

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.1, [0.2, 0.2], 0.5, 0.2, 0.5, 0.4, 0.8, 0.02][category_id - 1][0]
        )

    else:
        assert (
            _hr_multiplier
            == [0.1, [0.2, 0.2], 0.5, 0.2, 0.5, 0.4, 0.8, 0.02][category_id - 1]
        )

    _hr_multiplier = get_dormant_hr_multiplier([category_id, 1, 0.0], "space", "ground")

    assert isinstance(_hr_multiplier, float)
    if category_id == 2:
        assert (
            _hr_multiplier
            == [0.3, [0.8, 1.0], 1.0, 0.4, 1.0, 0.9, 1.0, 0.03][category_id - 1][0]
        )

    else:
        assert (
            _hr_multiplier
            == [0.3, [0.8, 1.0], 1.0, 0.4, 1.0, 0.9, 1.0, 0.03][category_id - 1]
        )


@pytest.mark.unit
def test_get_dormant_hr_multiplier_no_category():
    """get_dormant_hr_multiplier() should return 0.0 if the category ID is not in
    1-8."""
    assert get_dormant_hr_multiplier([10, 1, 0.0], "ground", "ground") == 0.0


@pytest.mark.unit
def test_get_dormant_hr_multiplier_no_environment():
    """get_dormant_hr_multiplier() should return 0.0 if the active/dormant environments
    combination is not valid."""
    assert get_dormant_hr_multiplier([1, 1, 0.0], "missile", "ground") == 0.0
    assert get_dormant_hr_multiplier([1, 1, 0.0], "ground", "airborne") == 0.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "category_id, subcategory_id, expected",
    [
        (1, 1, 0.00069138992),
        (2, 1, 0.00034569496),
        (1, 3, 0.00069138992),
        (2, 3, 0.0),
    ],
)
def test_dormant_hazard_rate(category_id, subcategory_id, expected):
    """do_calculate_dormant_hazard_rate() should return a float value for the dormant
    hazard rate on success."""
    _hr_dormant = do_calculate_dormant_hazard_rate(
        hw_info=[category_id, subcategory_id, 0.008642374], env_info=[3, 1]
    )

    assert isinstance(_hr_dormant, float)
    assert _hr_dormant == pytest.approx(expected)


@pytest.mark.unit
@pytest.mark.calculation
def test_dormant_hazard_rate_bad_index():
    """do_calculate_dormant_hazard_rate() should raise an IndexError when a bad index
    value is passed."""
    with pytest.raises(IndexError):
        _hr_dormant = do_calculate_dormant_hazard_rate(
            hw_info=[4, 5, 0.008642374], env_info=[3, 12]
        )
