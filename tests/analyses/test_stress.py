# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_stress.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the electrical stress module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import stress


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio():
    """Return a float stress ratio on success."""
    _stress_ratio = stress.calculate_stress_ratio(0.625, 1.25)

    assert _stress_ratio == pytest.approx(0.5)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_string_input():
    """Raise a TypeError if passed a string as a stress value."""
    with pytest.raises(TypeError):
        stress.calculate_stress_ratio(0.625, "1.25")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_zero_rated():
    """Raise a ZeroDivisionError if passed a rated stress of zero."""
    with pytest.raises(ZeroDivisionError):
        stress.calculate_stress_ratio(0.625, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_negative_operating():
    """Raise a ValueError if passed a negative operating stress."""
    with pytest.raises(ValueError):
        stress.calculate_stress_ratio(-0.625, 1.25)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_negative_rated():
    """Raise a ValueError if passed a negative rated stress."""
    with pytest.raises(ValueError):
        stress.calculate_stress_ratio(0.625, -1.25)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_zero_operating():
    """Return 0.0 when operating stress is zero."""
    _stress_ratio = stress.calculate_stress_ratio(0.0, 1.25)
    assert _stress_ratio == pytest.approx(0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_both_zero():
    """Raise a ZeroDivisionError if both operating and rated stresses are zero."""
    with pytest.raises(ZeroDivisionError):
        stress.calculate_stress_ratio(0.0, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_near_zero_operating():
    """Return near 0.0 when operating stress is very small."""
    _stress_ratio = stress.calculate_stress_ratio(1e-10, 1.25)
    assert _stress_ratio == pytest.approx(8.0e-11)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "operating, rated", [(0.625, -1.25), (-0.625, 1.25), (-0.625, -1.25)]
)
def test_calculate_stress_ratio_invalid_inputs(operating, rated):
    """Raise a ValueError if passed invalid stress values."""
    with pytest.raises(ValueError):
        stress.calculate_stress_ratio(operating, rated)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_non_numerical():
    """Raise a TypeError if passed non-numerical inputs."""
    with pytest.raises(TypeError):
        stress.calculate_stress_ratio("string", 1.25)
    with pytest.raises(TypeError):
        stress.calculate_stress_ratio(0.625, "string")
    with pytest.raises(TypeError):
        stress.calculate_stress_ratio(None, 1.25)
