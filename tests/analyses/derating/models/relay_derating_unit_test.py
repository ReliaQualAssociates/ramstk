# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.relay_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the relay derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import relay


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    test_stress_limits,
):
    """Returns 0 and an empty string when the relay is not exceeding any limit."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.2,
        temperature_active=46.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_current(
    test_stress_limits,
):
    """Returns 0 and an empty string when the current limit is on the boundary."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.6,  # Exactly at the current limit
        temperature_active=46.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_temperature(
    test_stress_limits,
):
    """Returns 0 and an empty string when the temperature is on the boundary."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.5,
        temperature_active=65.0,  # Exactly at the temperature limit
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_active_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the ambient temperature limit."""
    _overstress, _reason = relay.do_derating_analysis(
        environment_id,
        test_stress_limits["relay"],
        current_ratio=0.2,
        temperature_active=76.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Temperature of 76.3C exceeds the derated maximum temperature of "
            "10.0C less than maximum rated temperature of 85.0C.\n",
            1: "Temperature of 76.3C exceeds the derated maximum temperature of "
            "20.0C less than maximum rated temperature of 85.0C.\n",
            2: "Temperature of 76.3C exceeds the derated maximum temperature of "
            "30.0C less than maximum rated temperature of 85.0C.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_current(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the current ratio limit."""
    _overstress, _reason = relay.do_derating_analysis(
        environment_id,
        test_stress_limits["relay"],
        current_ratio=0.8,
        temperature_active=46.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.8 exceeds the allowable limit of 0.7.\n",
            1: "Current ratio of 0.8 exceeds the allowable limit of 0.6.\n",
            2: "Current ratio of 0.8 exceeds the allowable limit of 0.5.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding both limits."""
    _overstress, _reason = relay.do_derating_analysis(
        environment_id,
        test_stress_limits["relay"],
        current_ratio=0.8,
        temperature_active=96.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.8 exceeds the allowable limit of 0.7.\n"
            "Temperature of 96.3C exceeds the derated maximum temperature of "
            "10.0C less than maximum rated temperature of 85.0C.\n",
            1: "Current ratio of 0.8 exceeds the allowable limit of 0.6.\n"
            "Temperature of 96.3C exceeds the derated maximum temperature of "
            "20.0C less than maximum rated temperature of 85.0C.\n",
            2: "Current ratio of 0.8 exceeds the allowable limit of 0.5.\n"
            "Temperature of 96.3C exceeds the derated maximum temperature of "
            "30.0C less than maximum rated temperature of 85.0C.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises am IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match="do_derating_analysis: Invalid relay environment ID 5."
    ):
        relay.do_derating_analysis(
            5,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_type_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid load type ID."""
    with pytest.raises(
        KeyError, match=r"do_derating_analysis: Invalid relay load type ID 11."
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=11,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed a string active temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid relay current ratio type "
        r"<class 'float'> or ambient operating temperature <class 'str'>.  "
        r"Both should be <type 'float'>.",
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active="128.3",
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the active temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid relay current ratio type "
        r"<class 'float'> or ambient operating temperature <class 'NoneType'>.  "
        r"Both should be <type 'float'>.",
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=None,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid relay current ratio type "
        r"<class 'str'> or ambient operating temperature <class 'float'>.  "
        r"Both should be <type 'float'>.",
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio="0.9",
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid relay current ratio type "
        r"<class 'NoneType'> or ambient operating temperature <class 'float'>.  "
        r"Both should be <type 'float'>.",
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=None,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_missing_required_args(
    test_stress_limits,
):
    """Raises a TypeError when missing required arguments."""
    with pytest.raises(
        TypeError,
        match=r"missing 1 required keyword-only argument: 'current_ratio'",
    ):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            temperature_active=46.3,  # Missing current_ratio
            temperature_rated_max=85.0,
            type_id=1,
        )
