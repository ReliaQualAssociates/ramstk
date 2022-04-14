# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.lamp_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the lamp derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import lamp


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """should determine the lamp is not execeeding any limit."""
    _overstress, _reason = lamp.do_derating_analysis(
        1,
        4,
        test_stress_limits["miscellaneous"],
        current_ratio=0.05,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """should determine the lamp is execeeding the current limit."""
    _overstress, _reason = lamp.do_derating_analysis(
        1,
        4,
        test_stress_limits["miscellaneous"],
        current_ratio=0.95,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.95 exceeds the allowable limit of 0.1.\n"


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        lamp.do_derating_analysis(
            5,
            4,
            test_stress_limits["miscellaneous"],
            current_ratio=0.02,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
        lamp.do_derating_analysis(
            1,
            21,
            test_stress_limits["miscellaneous"],
            current_ratio=0.025,
        )


@pytest.mark.unit
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        lamp.do_derating_analysis(
            1,
            4,
            test_stress_limits["miscellaneous"],
            current_ratio=current_ratio,
        )
