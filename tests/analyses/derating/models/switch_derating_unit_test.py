# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.switch_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the switch derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import switch


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """should determine the switch is not execeeding any limit."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.3,
        power_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """should determine the switch is execeeding the current limit."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.86,
        power_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.86 exceeds the allowable limit of 0.4.\n"


@pytest.mark.unit
def test_do_derating_analysis_power(test_stress_limits):
    """should determine the switch is execeeding the power limit."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.1,
        power_ratio=0.92,
    )

    assert _overstress == 1
    assert _reason == "Power ratio of 0.92 exceeds the allowable limit of 0.6.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """should determine the switch is execeeding both limits."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.86,
        power_ratio=0.92,
    )

    assert _overstress == 1
    assert (
        _reason == "Current ratio of 0.86 exceeds the allowable limit of 0.4.\nPower "
        "ratio of 0.92 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        switch.do_derating_analysis(
            5,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=0.1,
            power_ratio=0.2,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_application(test_stress_limits):
    """should raise am KeyError when passed an unknown application ID."""
    with pytest.raises(KeyError):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=21,
            current_ratio=0.1,
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=current_ratio,
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("power_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_power_ratio(
    power_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric power ratio."""
    with pytest.raises(TypeError):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=0.1,
            power_ratio=power_ratio,
        )
