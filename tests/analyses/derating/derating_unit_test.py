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
def test_do_check_stress_limits_no_overstress():
    """Returns 0 and an empty reason string when no overstress condition exists."""
    _overstress, _reason = derating_utils.do_update_overstress_status(
        0,
        "",
        (0, ""),
    )
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_stress_limits_with_overstress():
    """Returns updated overstress and reason when overstress condition exists."""
    _overstress, _reason = derating_utils.do_update_overstress_status(
        0, "", (1, "Current overstress.\n")
    )
    assert _overstress == 1
    assert _reason == "Current overstress.\n"


@pytest.mark.unit
def test_do_check_current_limit_below_limit():
    """Return 0 and empty reason string when current ratio is within limit."""
    _overstress, _reason = derating_utils.do_check_current_limit(
        0.3,
        0.4,
    )
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_current_limit_exceeds_limit():
    """Return 1 and the reason string when current ratio exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_current_limit(
        0.5,
        0.4,
    )
    assert _overstress == 1
    assert _reason == "Current ratio of 0.5 exceeds the allowable limit of 0.4.\n"


@pytest.mark.unit
def test_do_check_temperature_limit_within_limit():
    """Return 0 and empty reason string when temperature is within limit."""
    _overstress, _reason = derating_utils.do_check_temperature_limit(
        50.0,
        100.0,
        20.0,
    )
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_temperature_limit_exceeds_limit():
    """Return 1 and the reason string when temperature exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_temperature_limit(
        90.0,
        100.0,
        15.0,
    )
    assert _overstress == 1
    assert _reason == (
        "Temperature of 90.0C exceeds the derated maximum temperature of "
        "15.0C less than maximum rated temperature of 100.0C.\n"
    )


@pytest.mark.unit
def test_do_check_voltage_limit_below_limit():
    """Return 0 and empty reason string when voltage ratio is within limit."""
    _overstress, _reason = derating_utils.do_check_voltage_limit(
        0.2,
        0.5,
    )
    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_check_voltage_limit_exceeds_limit():
    """Return 1 and the reason string when voltage ratio exceeds the limit."""
    _overstress, _reason = derating_utils.do_check_voltage_limit(
        0.6,
        0.5,
    )
    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.6 exceeds the allowable limit of 0.5.\n"


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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress(
    category,
    test_stress_limits,
):
    """Return 0 and an empty reason string when not exceeding any limit."""
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_on_limit(
    test_stress_limits,
):
    """Returns 0 and an empty reason string when limit is exactly at boundary."""
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


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_over_limit_protected_env(
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding a limit in a protected
    environment."""
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_over_limit_normal_env(
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding a limit in a normal environment."""
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_over_limit_harsh_env(
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding a limit in a harsh environment."""
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_invalid_environment_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid environment ID."""
    with pytest.raises(
        KeyError,
        match=r"do_check_overstress: Invalid capacitor environment ID 15 or "
        r"subcategory ID 10.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"do_check_overstress: Invalid capacitor environment ID 5 or "
        r"subcategory ID 20.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_check_overstress_invalid_category_name(
    test_stress_limits,
):
    """Returns 0 and an empty reason string when passed an invalid component
    category."""
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
