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
from ramstk.analyses.derating import derating, derating_utils


@pytest.mark.unit
@pytest.mark.parametrize(
    "category",
    [
        "capacitor",
        "connection",
        "inductor",
        "integrated_circuit",
        "miscellaneous",
        "relay",
        "resistor",
        "semiconductor",
        "switch",
    ],
)
def test_check_overstress(test_stress_limits, category):
    """Should determine the component is not execeeding any limit."""
    if category == "miscellaneous":
        _subcategory_id = 4
    else:
        _subcategory_id = 1

    _overstress, _reason = derating.do_check_overstress(
        category,
        3,
        _subcategory_id,
        test_stress_limits[category],
        application_id=1,
        current_ratio=0.05,
        family_id=1,
        package_id=2,
        power_rated=0.125,
        power_ratio=0.15,
        quality_id=1,
        specification_id=1,
        technology_id=1,
        temperature_active=30.0,
        temperature_case=38.4,
        temperature_hot_spot=48.2,
        temperature_junction=70.0,
        temperature_knee=70.0,
        temperature_rated_max=85.0,
        type_id=1,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_check_overstress_over_limit_protected(test_stress_limits):
    """Should determine a component is exceeding a limit in a protected environment."""
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
        _reason == "Temperature of 78.4C exceeds the derated maximum temperature of "
        "15.0C less than maximum rated temperature of 85.0C.\nVoltage ratio "
        "of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_over_limit_normal(test_stress_limits):
    """Should determine a component is exceeding a limit in a normal environment."""
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
        _reason == "Temperature of 78.4C exceeds the derated maximum temperature of "
        "15.0C less than maximum rated temperature of 85.0C.\nVoltage ratio "
        "of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_over_limit_harsh(test_stress_limits):
    """Should determine a component is exceeding a limit in a harsh environment."""
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
        _reason == "Temperature of 78.4C exceeds the derated maximum temperature of "
        "15.0C less than maximum rated temperature of 85.0C.\nVoltage ratio "
        "of 0.7 exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_check_overstress_unknown_environment(test_stress_limits):
    """Should raise an KeyError when passed an unknown environment."""
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
    """Should raise an KeyError when passed an unknown subcategory."""
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
    """Should return (0, "") when passed an unknown component category."""
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
    """Should raise am TypeError when passed a non-numeric value."""
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


@pytest.mark.unit
def test_do_check_stress_limits_no_overstress():
    """Should return no overstress and empty reason when result is (0, "")."""
    _overstress, _reason = derating_utils.do_update_overstress_status(0, "", (0, ""))
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_stress_limits_with_overstress():
    """Should return updated overstress and reason when result is (1, "reason")."""
    _overstress, _reason = derating_utils.do_update_overstress_status(
        0, "", (1, "Current overstress.\n")
    )
    assert _overstress == 1
    assert _reason == "Current overstress.\n"


@pytest.mark.unit
def test_do_check_current_limit_below_limit():
    """Should return no overstress when current ratio is within limit."""
    _overstress, _reason = derating_utils.do_check_current_limit(0.3, 0.4)
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_current_limit_exceeds_limit():
    """Should return overstress when current ratio exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_current_limit(0.5, 0.4)
    assert _overstress == 1
    assert _reason == "Current ratio of 0.5 exceeds the allowable limit of 0.4.\n"


@pytest.mark.unit
def test_do_check_temperature_limit_within_limit():
    """Should return no overstress when temperature is within limit."""
    _overstress, _reason = derating_utils.do_check_temperature_limit(50.0, 100.0, 20.0)
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_temperature_limit_exceeds_limit():
    """Should return overstress when temperature exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_temperature_limit(90.0, 100.0, 15.0)
    assert _overstress == 1
    assert _reason == (
        "Temperature of 90.0C exceeds the derated maximum temperature of "
        "15.0C less than maximum rated temperature of 100.0C.\n"
    )


@pytest.mark.unit
def test_do_check_voltage_limit_below_limit():
    """Should return no overstress when voltage ratio is within limit."""
    _overstress, _reason = derating_utils.do_check_voltage_limit(0.2, 0.5)
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_voltage_limit_exceeds_limit():
    """Should return overstress when voltage ratio exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_voltage_limit(0.6, 0.5)
    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.6 exceeds the allowable limit of 0.5.\n"


@pytest.mark.unit
def test_check_overstress_on_limit(test_stress_limits):
    """Should determine the component is not exceeding limits exactly at boundary."""
    _overstress, _reason = derating.do_check_overstress(
        "capacitor",
        1,
        10,
        test_stress_limits["capacitor"],
        specification_id=1,
        temperature_case=70.0,  # Exactly at the boundary
        temperature_rated_max=85.0,
        voltage_ratio=0.6,  # Exactly at the boundary
    )

    assert _overstress == 0
    assert _reason == ""
