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
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """Should determine the relay is not execeeding any limit."""
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
def test_do_derating_analysis_active_temperature(test_stress_limits):
    """Should determine the relay is exceeding the active ambient temperature limit."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.2,
        temperature_active=76.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 76.3C exceeds the derated maximum temperature of "
        "20.0C less than maximum rated temperature of 85.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """Should determine the relay is execeeding the current limit."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.8,
        temperature_active=46.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.8 exceeds the allowable limit of 0.6.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """Should determine the relay is execeeding both limits."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.8,
        temperature_active=66.3,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 1
    assert (
        _reason == "Current ratio of 0.8 exceeds the allowable limit of 0.6.\n"
        "Temperature of 66.3C exceeds the derated maximum temperature of "
        "20.0C less than maximum rated temperature of 85.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """Should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        relay.do_derating_analysis(
            5,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_type(test_stress_limits):
    """Should raise am KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=11,
        )


@pytest.mark.unit
@pytest.mark.parametrize("active_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    active_temperature,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=0.2,
            temperature_active=active_temperature,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            current_ratio=current_ratio,
            temperature_active=46.3,
            temperature_rated_max=85.0,
            type_id=1,
        )


@pytest.mark.unit
def test_do_derating_analysis_borderline_current(test_stress_limits):
    """Should determine the relay is not exceeding the current limit on the boundary."""
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
def test_do_derating_analysis_borderline_temperature(test_stress_limits):
    """Should determine the relay is not exceeding the temperature limit on the
    boundary."""
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
def test_do_derating_analysis_valid_limits(test_stress_limits):
    """Should determine the relay is not exceeding any limit under valid conditions."""
    _overstress, _reason = relay.do_derating_analysis(
        1,
        test_stress_limits["relay"],
        current_ratio=0.5,
        temperature_active=50.0,
        temperature_rated_max=85.0,
        type_id=1,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_missing_required_args(test_stress_limits):
    """Should raise KeyError when missing required arguments."""
    with pytest.raises(KeyError):
        relay.do_derating_analysis(
            1,
            test_stress_limits["relay"],
            temperature_active=46.3,  # Missing current_ratio
            temperature_rated_max=85.0,
            type_id=1,
        )
