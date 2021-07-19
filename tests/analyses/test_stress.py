# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_stress.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the electrical stress module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import stress


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio():
    """calculate_stress_ratio() should return a float stress ratio on success."""
    _stress_ratio = stress.calculate_stress_ratio(0.625, 1.25)

    assert pytest.approx(_stress_ratio, 0.5)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_string_input():
    """calculate_stress_ratio() should raise a TypeError if passed a string as a stress value."""
    with pytest.raises(TypeError):
        _stress_ratio = stress.calculate_stress_ratio(0.625, "1.25")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_stress_ratio_zero_rated():
    """calculate_stress_ratio() should raise a ZeroDivisionError if passed a rated stress of zero."""
    with pytest.raises(ZeroDivisionError):
        _stress_ratio = stress.calculate_stress_ratio(0.625, 0.0)
