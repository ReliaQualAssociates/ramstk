# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_improvementfactor.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the improvement factor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor():
    """calculate_improvement() should return a tuple of improvement factor and
    weight."""
    _improvement, _weight = improvementfactor.calculate_improvement(
        3, 2, 4, user_float_1=2.6
    )

    assert _improvement == pytest.approx(1.2)
    assert _weight == pytest.approx(12.48)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_default_user_floats():
    """calculate_improvement() should use default user_float_X values if not
    provided."""
    _improvement, _weight = improvementfactor.calculate_improvement(3, 2, 4)

    assert _improvement == pytest.approx(1.2)
    assert _weight == pytest.approx(4.8)  # 4 * 1.2 * (1.0 for each user_float)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_negative_ranks():
    """calculate_improvement() should raise a ValueError if ranks are negative."""
    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(-1, 2, 4)

    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(3, -2, 4)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_negative_priority():
    """calculate_improvement() should raise a ValueError if priority is zero or
    negative."""
    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(3, 2, 0)  # Zero priority

    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(3, 2, -1)  # Negative priority


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_invalid_user_float():
    """calculate_improvement() should raise a ValueError if user_float_X is non-
    numeric."""
    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(3, 2, 4, user_float_1="invalid")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_equal_ranks():
    """calculate_improvement() should return an improvement factor of 1.0 when ranks are
    equal."""
    _improvement, _weight = improvementfactor.calculate_improvement(3, 3, 4)

    assert _improvement == pytest.approx(1.0)
    assert _weight == pytest.approx(4.0)  # priority * improvement factor * default
    # user_float_X


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_max_rank_difference():
    """calculate_improvement() shoul correctly handle large differences between
    ranks."""
    _improvement, _weight = improvementfactor.calculate_improvement(
        10, 1, 3, user_float_1=2.0
    )

    assert _improvement == pytest.approx(2.8)  # 1.0 + 0.2 * (10 - 1)
    assert _weight == pytest.approx(16.8)  # 3 * 2.8 * 2.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_zero_user_float():
    """calculate_improvement() should raise a ValueError if any user_float_X is zero."""
    with pytest.raises(ValueError):
        improvementfactor.calculate_improvement(3, 2, 4, user_float_1=0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvementfactor_all_user_floats_one():
    """calculate_improvement() should calculate weight properly with user_float_X =
    1.0."""
    _improvement, _weight = improvementfactor.calculate_improvement(
        5, 3, 6, user_float_1=1.0, user_float_2=1.0
    )

    assert _improvement == pytest.approx(1.4)
    assert _weight == pytest.approx(8.4)  # 6 * 1.4 * (user_float defaults to 1.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_improvement_dynamic_user_floats():
    """calculate_improvement() should dynamically handle any number of user floats."""
    # Case with 2 user floats
    _improvement, _weight = improvementfactor.calculate_improvement(
        3, 2, 5, user_float_1=1.2, user_float_2=1.3
    )
    assert _improvement == pytest.approx(1.2)
    assert _weight == pytest.approx(9.36)  # 5 * 1.2 * (1.2 * 1.3)

    # Case with no user floats (defaults to 1.0)
    _improvement, _weight = improvementfactor.calculate_improvement(3, 2, 5)
    assert _improvement == pytest.approx(1.2)
    assert _weight == pytest.approx(6.0)  # 5 * 1.2 * 1.0

    # Case with 5 user floats
    _improvement, _weight = improvementfactor.calculate_improvement(
        3,
        2,
        5,
        user_float_1=1.2,
        user_float_2=1.3,
        user_float_3=1.4,
        user_float_4=1.5,
        user_float_5=1.6,
    )
    assert _improvement == pytest.approx(1.2)
    assert _weight == pytest.approx(31.4496)  # 5 * 1.2 * (1.2 * 1.3 * 1.4 * 1.5 * 1.6)
