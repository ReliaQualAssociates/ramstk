# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.semiconductor_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import semiconductor


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and an empty reason string when not exceeding any limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.5,
        power_ratio=0.3,
        quality_id=3,
        type_id=3,
        temperature_junction=68.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_current(
    test_stress_limits,
):
    """Return 0 and an empty reason string when the current ratio is on the boundary."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.8,  # Exactly at the limit
        power_ratio=0.3,
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_power(
    test_stress_limits,
):
    """Return 0 and an empty reason string when the power ratio is on the boundary."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.7,
        power_ratio=0.8,  # Exactly at the limit
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.2,
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
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.92,
        power_ratio=0.3,
        quality_id=3,
        type_id=3,
        temperature_junction=68.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.92 exceeds the allowable limit of 0.9.\n",
            1: "Current ratio of 0.92 exceeds the allowable limit of 0.8.\n",
            2: "Current ratio of 0.92 exceeds the allowable limit of 0.6.\n",
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
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.52,
        power_ratio=0.92,
        quality_id=3,
        type_id=3,
        temperature_junction=68.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Power ratio of 0.92 exceeds the allowable limit of 0.9.\n",
            1: "Power ratio of 0.92 exceeds the allowable limit of 0.8.\n",
            2: "Power ratio of 0.92 exceeds the allowable limit of 0.6.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_junction_temperature(
    environment_id,
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding the junction temperature limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.52,
        power_ratio=0.53,
        quality_id=3,
        type_id=3,
        temperature_junction=118.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Temperature of 118.3C exceeds the derated maximum temperature of "
            "100.0C.\n",
            1: "Temperature of 118.3C exceeds the derated maximum temperature of "
            "85.0C.\n",
            2: "Temperature of 118.3C exceeds the derated maximum temperature of "
            "70.0C.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_voltage_ratio(
    environment_id,
    test_stress_limits,
):
    """Return 1 and reason string when exceeding the voltage ratio limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.42,
        power_ratio=0.53,
        quality_id=3,
        type_id=3,
        temperature_junction=68.3,
        voltage_ratio=0.92,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Voltage ratio of 0.92 exceeds the allowable limit of 0.8.\n",
            1: "Voltage ratio of 0.92 exceeds the allowable limit of 0.75.\n",
            2: "Voltage ratio of 0.92 exceeds the allowable limit of 0.3.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    environment_id,
    test_stress_limits,
):
    """Return 1 and the reason string when exceeding all limits."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        environment_id,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.92,
        power_ratio=0.93,
        quality_id=3,
        type_id=3,
        temperature_junction=128.3,
        voltage_ratio=0.92,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.92 exceeds the allowable limit of 0.9.\nPower "
            "ratio of 0.93 exceeds the allowable limit of 0.9.\nTemperature of 128.3C "
            "exceeds the derated maximum temperature of 100.0C.\nVoltage ratio of 0.92 "
            "exceeds the allowable limit of 0.8.\n",
            1: "Current ratio of 0.92 exceeds the allowable limit of 0.8.\nPower "
            "ratio of 0.93 exceeds the allowable limit of 0.8.\nTemperature of 128.3C "
            "exceeds the derated maximum temperature of 85.0C.\nVoltage ratio of 0.92 "
            "exceeds the allowable limit of 0.75.\n",
            2: "Current ratio of 0.92 exceeds the allowable limit of 0.6.\nPower "
            "ratio of 0.93 exceeds the allowable limit of 0.6.\nTemperature of 128.3C "
            "exceeds the derated maximum temperature of 70.0C.\nVoltage ratio of 0.92 "
            "exceeds the allowable limit of 0.3.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises an IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError,
        match=r"do_derating_analysis: Invalid semiconductor environment ID 5.",
    ):
        semiconductor.do_derating_analysis(
            5,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.2,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid semiconductor quality ID 3, "
        r"subcategory ID 21, or type ID 3.",
    ):
        semiconductor.do_derating_analysis(
            1,
            21,
            test_stress_limits["semiconductor"],
            current_ratio=0.2,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_quality_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid quality ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid semiconductor quality ID 31, "
        r"subcategory ID 3, or type ID 3.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.2,
            power_ratio=0.3,
            quality_id=31,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_type_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid type ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid semiconductor quality ID 3, "
        r"subcategory ID 1, or type ID 31.",
    ):
        semiconductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["semiconductor"],
            current_ratio=0.2,
            power_ratio=0.3,
            quality_id=3,
            type_id=31,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'str'>, power ratio type <class 'float'>, junction temperature type "
        r"<class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio="0.9",
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'NoneType'>, power ratio type <class 'float'>, junction temperature "
        r"type <class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=None,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_power_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string power ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'float'>, power ratio type <class 'str'>, junction temperature type "
        r"<class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio="0.9",
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_power_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the power ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'float'>, power ratio type <class 'NoneType'>, junction temperature "
        r"type <class 'float'>, or voltage ratio type <class 'float'>.  All should "
        r"be <type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio=None,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.skip
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_junction_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed a string junction temperature."""
    with pytest.raises(TypeError, match=r"Suck that cock nasty girl"):
        semiconductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["semiconductor"],
            current_ratio=0.9,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction="158.3",
            voltage_ratio=0.2,
        )


@pytest.mark.skip
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_junction_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the junction temperature."""
    with pytest.raises(TypeError, match=r"Suck that cock nasty girl"):
        semiconductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["semiconductor"],
            current_ratio=0.9,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=None,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'float'>, power ratio type <class 'float'>, junction temperature "
        r"type <class 'float'>, or voltage ratio type <class 'str'>.  All should be "
        r"<type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio="0.9",
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid semiconductor current ratio type "
        r"<class 'float'>, power ratio type <class 'float'>, junction temperature "
        r"type <class 'float'>, or voltage ratio type <class 'NoneType'>.  All should "
        r"be <type 'float'>.",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=None,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_missing_required_args(
    test_stress_limits,
):
    """Raises a TypeError when required arguments are missing."""
    with pytest.raises(
        TypeError,
        match=r"missing 1 required keyword-only argument: 'power_ratio'",
    ):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            # Missing power_ratio
            quality_id=3,
            type_id=3,
            temperature_junction=78.3,
            voltage_ratio=0.2,
        )
