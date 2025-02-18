# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.inductor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the inductor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import inductor


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses_coil(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and an empty reason string when not exceeding limits."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.2,
        family_id=2,
        temperature_hot_spot=51.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses_transformer(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and en empty reason string when not exceeding limits."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        2,
        test_stress_limits["inductor"],
        current_ratio=0.2,
        family_id=1,
        temperature_hot_spot=51.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_current(
    test_stress_limits,
):
    """Returns o and empty reason string when current ratio limit on boundary."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.7,  # Exactly at the current limit
        family_id=2,
        temperature_hot_spot=50.0,
        temperature_rated_max=130.0,
        voltage_ratio=0.5,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns o and empty reason string when hot spot temperature limit on boundary."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.5,
        family_id=2,
        temperature_hot_spot=100.0,  # Exactly at the temperature limit
        temperature_rated_max=130.0,
        voltage_ratio=0.4,
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
    """Returns 1 and the reason string when exceeding the current ratio limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.863,
        family_id=2,
        temperature_hot_spot=59.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            1: "Current ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            2: "Current ratio of 0.863 exceeds the allowable limit of 0.6.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_hot_spot_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the hot spot temperature limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.2,
        family_id=2,
        temperature_hot_spot=111.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 111.3C exceeds the derated maximum temperature of "
        "30.0C less than maximum rated temperature of 130.0C.\n"
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_voltage_ratio(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the voltage limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.2,
        family_id=2,
        temperature_hot_spot=59.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.863,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Voltage ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            1: "Voltage ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            2: "Voltage ratio of 0.863 exceeds the allowable limit of 0.6.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding all limits."""
    _overstress, _reason = inductor.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.81,
        family_id=2,
        temperature_hot_spot=109.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.863,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.81 exceeds the allowable limit of 0.7.\n"
            "Temperature of 109.3C exceeds the derated maximum temperature of "
            "30.0C less than maximum rated temperature of 130.0C.\nVoltage "
            "ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            1: "Current ratio of 0.81 exceeds the allowable limit of 0.7.\n"
            "Temperature of 109.3C exceeds the derated maximum temperature of "
            "30.0C less than maximum rated temperature of 130.0C.\n"
            "Voltage ratio of 0.863 exceeds the allowable limit of 0.7.\n",
            2: "Current ratio of 0.81 exceeds the allowable limit of 0.6.\n"
            "Temperature of 109.3C exceeds the derated maximum temperature of "
            "30.0C less than maximum rated temperature of 130.0C.\n"
            "Voltage ratio of 0.863 exceeds the allowable limit of 0.6.\n",
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
        match=r"do_derating_analysis: Invalid inductive device environment ID 5.",
    ):
        inductor.do_derating_analysis(
            5,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.81,
            family_id=2,
            temperature_hot_spot=109.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.863,
        )


@pytest.mark.skip(reason="Defaulting to 'high frequency for now.")
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid inductive device family ID 2 or "
        r"subcategory ID 21.",
    ):
        inductor.do_derating_analysis(
            1,
            21,
            test_stress_limits["inductor"],
            current_ratio=0.81,
            family_id=2,
            temperature_hot_spot=109.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.863,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_family_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid family ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid inductive device family ID 21.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.81,
            family_id=21,
            temperature_hot_spot=109.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.863,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'str'>, hot spot temperature type <class 'float'>, or voltage ratio "
        r"type <class 'float'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio="0.9",
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'NoneType'>, hot spot temperature type <class 'float'>, or voltage "
        r"ratio type <class 'float'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=None,
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_hot_spot_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed a string hot spot temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'float'>, hot spot temperature type <class 'str'>, or voltage ratio "
        r"type <class 'float'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot="128.3",
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_hot_spot_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the hot spot temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'float'>, hot spot temperature type <class 'NoneType'>, or voltage "
        r"ratio type <class 'float'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot=None,
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'float'>, hot spot temperature type <class 'float'>, or voltage ratio "
        r"type <class 'str'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
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
        match=r"do_derating_analysis: Invalid inductive device current ratio type "
        r"<class 'float'>, hot spot temperature type <class 'float'>, or voltage ratio "
        r"type <class 'NoneType'>.  All should be <type 'float'>.",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
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
        match=r"missing 3 required keyword-only arguments: 'current_ratio', "
        r"'temperature_hot_spot', and 'voltage_ratio'",
    ):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            family_id=2,
            temperature_rated_max=130.0,
        )
