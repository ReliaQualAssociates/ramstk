# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.switch_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the switch derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import switch


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Return 0 and an empty reason string when not exceeding any limit."""
    _overstress, _reason = switch.do_derating_analysis(
        environment_id,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.3,
        power_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_current_ratio(
    test_stress_limits,
):
    """Return 0 and an empty reason string when the current ratio is at the boundary."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.4,  # Exactly at the limit
        power_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_power_ratio(
    test_stress_limits,
):
    """Return 0 and an empty reason string when the power ratio limit is at the
    boundary."""
    _overstress, _reason = switch.do_derating_analysis(
        1,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.3,
        power_ratio=0.6,  # Exactly at the limit
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_current_ratio(
    environment_id,
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding the current ratio limit."""
    _overstress, _reason = switch.do_derating_analysis(
        environment_id,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.86,
        power_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.86 exceeds the allowable limit of 0.5.\n",
            1: "Current ratio of 0.86 exceeds the allowable limit of 0.4.\n",
            2: "Current ratio of 0.86 exceeds the allowable limit of 0.3.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_power_ratio(
    environment_id,
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding the power ratio limit."""
    _overstress, _reason = switch.do_derating_analysis(
        environment_id,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.1,
        power_ratio=0.92,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Power ratio of 0.92 exceeds the allowable limit of 0.7.\n",
            1: "Power ratio of 0.92 exceeds the allowable limit of 0.6.\n",
            2: "Power ratio of 0.92 exceeds the allowable limit of 0.5.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    environment_id,
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding both limits."""
    _overstress, _reason = switch.do_derating_analysis(
        environment_id,
        test_stress_limits["switch"],
        application_id=2,
        current_ratio=0.86,
        power_ratio=0.92,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.86 exceeds the allowable limit of 0.5.\nPower "
            "ratio of 0.92 exceeds the allowable limit of 0.7.\n",
            1: "Current ratio of 0.86 exceeds the allowable limit of 0.4.\nPower "
            "ratio of 0.92 exceeds the allowable limit of 0.6.\n",
            2: "Current ratio of 0.86 exceeds the allowable limit of 0.3.\nPower "
            "ratio of 0.92 exceeds the allowable limit of 0.5.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises an IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match=r"do_derating_analysis: Invalid switch environment ID 5."
    ):
        switch.do_derating_analysis(
            5,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=0.1,
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_application_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid application ID."""
    with pytest.raises(
        KeyError, match=r"do_derating_analysis: Invalid switch application ID 21."
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=21,
            current_ratio=0.1,
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid switch current ratio type "
        r"<class 'str'> or power ratio type <class 'float'>.  Both should be "
        r"<type 'float'>.",
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio="0.9",
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid switch current ratio type "
        r"<class 'NoneType'> or power ratio type <class 'float'>.  Both should be "
        r"<type 'float'>.",
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=None,
            power_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_power_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string power ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid switch current ratio type "
        r"<class 'float'> or power ratio type <class 'str'>.  Both should be "
        r"<type 'float'>.",
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=0.1,
            power_ratio="0.9",
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_power_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the power ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid switch current ratio type "
        r"<class 'float'> or power ratio type <class 'NoneType'>.  Both should be "
        r"<type 'float'>.",
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            current_ratio=0.1,
            power_ratio=None,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_missing_required_args(
    test_stress_limits,
):
    """Should raise KeyError when required arguments are missing."""
    with pytest.raises(
        TypeError, match=r"missing 1 required keyword-only argument: 'current_ratio'"
    ):
        switch.do_derating_analysis(
            1,
            test_stress_limits["switch"],
            application_id=2,
            # Missing current_ratio
            power_ratio=0.2,
        )
