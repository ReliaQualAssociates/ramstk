# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.derating_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the stress derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import derating


@pytest.mark.unit
def test_check_overstress(test_stress_limits):
    """should determine the component is not execeeding any limit."""
    _overstress, _reason = derating.do_check_overstress(
        "capacitor",
        3,
        10,
        test_stress_limits["capacitor"],
        specification_id=1,
        temperature_case=38.4,
        temperature_rated_max=85.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_check_overstress_over_limit_protected(test_stress_limits):
    """should determine a component is exceeding a limit in a protected environment."""
    _overstress, _reason = derating.do_check_overstress(
        "capacitor",
        1,
        10,
        test_stress_limits["capacitor"],
        specification_id=1,
        temperature_case=78.4,
        temperature_rated_max=85.0,
        voltage_ratio=0.7,
    )

    assert _overstress == 1
    assert (
        _reason == "Case temperature of 78.4C exceeds the derated maximum "
        "temperature of 15.0C less than maximum rated temperature of 85.0C.\nVoltage "
        "ratio of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_over_limit_normal(test_stress_limits):
    """should determine a component is exceeding a limit in a normal environment."""
    _overstress, _reason = derating.do_check_overstress(
        "capacitor",
        2,
        10,
        test_stress_limits["capacitor"],
        specification_id=1,
        temperature_case=78.4,
        temperature_rated_max=85.0,
        voltage_ratio=0.7,
    )

    assert _overstress == 1
    assert (
        _reason == "Case temperature of 78.4C exceeds the derated maximum "
        "temperature of 15.0C less than maximum rated temperature of 85.0C.\nVoltage "
        "ratio of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_over_limit_harsh(test_stress_limits):
    """should determine a component is exceeding a limit in a harsh environment."""
    _overstress, _reason = derating.do_check_overstress(
        "capacitor",
        3,
        10,
        test_stress_limits["capacitor"],
        specification_id=1,
        temperature_case=78.4,
        temperature_rated_max=85.0,
        voltage_ratio=0.7,
    )

    assert _overstress == 1
    assert (
        _reason == "Case temperature of 78.4C exceeds the derated maximum "
        "temperature of 15.0C less than maximum rated temperature of 85.0C.\nVoltage "
        "ratio of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_unknown_environment(test_stress_limits):
    """should raise an KeyError when passed an unknown environment."""
    with pytest.raises(KeyError):
        derating.do_check_overstress(
            "capacitor",
            15,
            10,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
def test_check_overstress_unknown_subcategory(test_stress_limits):
    """should raise an KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
        derating.do_check_overstress(
            "capacitor",
            5,
            20,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
def test_check_overstress_unknown_category(test_stress_limits):
    """should return (0, "") when passed an unknown component category."""
    _overstress, _reason = derating.do_check_overstress(
        "meter",
        5,
        10,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=46.3,
        temperature_rated_max=70.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("case_temperature", ["128.3", None])
def test_check_overstress_non_numeric_input(
    case_temperature,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric value."""
    with pytest.raises(TypeError):
        derating.do_check_overstress(
            "capacitor",
            1,
            1,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=case_temperature,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )
