# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.connection_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the connection derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import connection


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """should determine the connection is not execeeding any limit."""
    _overstress, _reason = connection.do_derating_analysis(
        1,
        test_stress_limits["connection"],
        current_ratio=0.5,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """should determine the connection is execeeding the voltage limit."""
    _overstress, _reason = connection.do_derating_analysis(
        1,
        test_stress_limits["connection"],
        current_ratio=1.5,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 1.5 exceeds the allowable limit of 1.0.\n"


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        connection.do_derating_analysis(
            5,
            test_stress_limits["connection"],
            current_ratio=0.9,
        )


@pytest.mark.unit
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric voltage ratio."""
    with pytest.raises(TypeError):
        connection.do_derating_analysis(
            1,
            test_stress_limits["connection"],
            current_ratio=current_ratio,
        )
