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
    """Return a float stress ratio on success."""
    _stress_ratio = stress.calculate_stress_ratio(0.625, 1.25)

    assert pytest.approx(_stress_ratio) == 0.5


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
