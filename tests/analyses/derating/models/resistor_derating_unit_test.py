# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.resistor_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import resistor


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.parametrize(
    "subcategory",
    [
        "fixed_composition",
        "fixed_film",
        "fixed_film_power",
        "fixed_film_network",
        "fixed_wirewound",
        "fixed_wirewound_power",
        "fixed_wirewound_chassis",
        "variable_wirewound",
        "variable_wirewound_precision",
        "variable_wirewound_power",
        "variable_non_wirewound",
        "variable_composition",
        "variable_film",
    ],
)
@pytest.mark.usefixtures("test_stress_limits")
def test_do_get_stress_limit_power(
    environment_id,
    subcategory,
    test_stress_limits,
):
    """Returns the power stress ratio limit."""
    _stress_limit = resistor._get_stress_limit(
        subcategory,
        environment_id,
        0.125,
        test_stress_limits["resistor"],
        "power",
    )

    assert isinstance(_stress_limit, float)
    assert (
        _stress_limit
        == {
            "fixed_composition": 0.65,
            "fixed_film": 0.65,
            "fixed_film_power": 0.55,
            "fixed_film_network": 0.55,
            "fixed_wirewound": 0.7,
            "fixed_wirewound_power": 0.6,
            "fixed_wirewound_chassis": 0.5,
            "variable_wirewound": 0.55,
            "variable_wirewound_precision": 0.55,
            "variable_wirewound_power": 0.55,
            "variable_non_wirewound": 0.55,
            "variable_composition": 0.5,
            "variable_film": 0.5,
        }[subcategory]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.parametrize(
    "subcategory",
    [
        "fixed_composition",
        "fixed_film",
        "fixed_film_power",
        "fixed_film_network",
        "fixed_wirewound",
        "fixed_wirewound_power",
        "fixed_wirewound_chassis",
        "variable_wirewound",
        "variable_wirewound_precision",
        "variable_wirewound_power",
        "variable_non_wirewound",
        "variable_composition",
        "variable_film",
    ],
)
@pytest.mark.usefixtures("test_stress_limits")
def test_do_get_stress_limit_temperature(
    environment_id,
    subcategory,
    test_stress_limits,
):
    """Returns the temperature stress limit."""
    _stress_limit = resistor._get_stress_limit(
        subcategory,
        environment_id,
        0.125,
        test_stress_limits["resistor"],
        "temperature",
    )

    assert isinstance(_stress_limit, float)
    assert (
        _stress_limit
        == {
            "fixed_composition": 0.65,
            "fixed_film": 0.65,
            "fixed_film_power": 0.55,
            "fixed_film_network": 0.55,
            "fixed_wirewound": 1.0,
            "fixed_wirewound_power": 0.6,
            "fixed_wirewound_chassis": 0.5,
            "variable_wirewound": 0.55,
            "variable_wirewound_precision": 0.55,
            "variable_wirewound_power": 110.0,
            "variable_non_wirewound": 0.55,
            "variable_composition": 0.5,
            "variable_film": 0.5,
        }[subcategory]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.parametrize(
    "subcategory",
    [
        "fixed_composition",
        "fixed_film",
        "fixed_film_network",
        "fixed_wirewound",
        "fixed_wirewound_power",
        "fixed_wirewound_chassis",
        # "variable_wirewound",
        # "variable_wirewound_precision",
        # "variable_wirewound_power",
        # "variable_non_wirewound",
        # "variable_composition",
        # "variable_film",
    ],
)
@pytest.mark.usefixtures("test_stress_limits")
def test_do_get_stress_limit_voltage(
    environment_id,
    subcategory,
    test_stress_limits,
):
    """Returns the temperature stress limit."""
    _stress_limit = resistor._get_stress_limit(
        subcategory,
        environment_id,
        0.125,
        test_stress_limits["resistor"],
        "voltage",
    )

    assert isinstance(_stress_limit, float)
    assert (
        _stress_limit
        == {
            "fixed_composition": 0.7,
            "fixed_film": 0.7,
            "fixed_film_network": 0.7,
            "fixed_wirewound": 0.7,
            "fixed_wirewound_power": 0.7,
            "fixed_wirewound_chassis": 0.7,
            "variable_wirewound": 1.0,
            "variable_wirewound_precision": 1.0,
            "variable_wirewound_power": 1.0,
            "variable_non_wirewound": 1.0,
            "variable_composition": 1.0,
            "variable_film": 1.0,
        }[subcategory]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    test_stress_limits,
):
    """Returns 0 and an empty string when the resistor is not exceeding any limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        temperature_case=46.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_power(
    test_stress_limits,
):
    """Returns 0 and an empty string when the power ratio is on the boundary."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.65,  # Exactly at the power limit
        temperature_case=46.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_borderline_temperature(
    test_stress_limits,
):
    """Returns 0 and an empty string when the temperature is on the boundary."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        temperature_case=122.0,  # Exactly at the temperature limit
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_power_ratio(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the power ratio limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        environment_id,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.75,
        temperature_case=46.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Power ratio of 0.75 exceeds the allowable limit of 0.65.\n"


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_case_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the case temperature limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        environment_id,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        temperature_case=126.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason
        == "Temperature of 126.3C exceeds the derated maximum temperature of 122.0C.\n"
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_voltage_ratio(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the voltage ratio limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        environment_id,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        temperature_case=56.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.8,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.8 exceeds the allowable limit of 0.7.\n"


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding both limits."""
    _overstress, _reason = resistor.do_derating_analysis(
        environment_id,
        6,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.75,
        temperature_case=128.4,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.8,
    )

    assert _overstress == 1
    assert (
        _reason
        == "Power ratio of 0.75 exceeds the allowable limit of 0.6.\nTemperature of 128.4C exceeds the "
        "derated maximum temperature of 118.0C.\nVoltage ratio of 0.8 exceeds the allowable limit of 0.7.\n"
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises am IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError, match=r"do_derating_analysis: Invalid resistor environment ID 5."
    ):
        resistor.do_derating_analysis(
            5,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError, match=r"_get_subcategory_name: Invalid resistor subcategory ID 21."
    ):
        resistor.do_derating_analysis(
            1,
            21,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_power_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string power ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid resistor power ratio type <class 'str'>, "
        r"rated power type <class 'float'>, case temperature type <class 'float'>, "
        r"knee temperature type <class 'float'>, rated temperature type "
        r"<class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio="0.9",
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
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
        match=r"do_derating_analysis: Invalid resistor power ratio type <class "
        r"'NoneType'>, rated power type <class 'float'>, case temperature type "
        r"<class 'float'>, knee temperature type <class 'float'>, rated temperature "
        r"type <class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=None,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed a string case temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid resistor power ratio type "
        r"<class 'float'>, rated power type <class 'float'>, case temperature type "
        r"<class 'str'>, knee temperature type <class 'float'>, rated temperature "
        r"type <class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case="128.3",
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_temperature(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the case temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid resistor power ratio type "
        r"<class 'float'>, rated power type <class 'float'>, case temperature type "
        r"<class 'NoneType'>, knee temperature type <class 'float'>, rated temperature "
        r"type <class 'float'>, or voltage ratio type <class 'float'>.  All should be "
        r"<type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case=None,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_voltage_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string voltage ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid resistor power ratio type "
        r"<class 'float'>, rated power type <class 'float'>, case temperature type "
        r"<class 'float'>, knee temperature type <class 'float'>, rated temperature "
        r"type <class 'float'>, or voltage ratio type <class 'str'>.  All should be "
        r"<type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
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
        match=r"do_derating_analysis: Invalid resistor power ratio type "
        r"<class 'float'>, rated power type <class 'float'>, case temperature type "
        r"<class 'float'>, knee temperature type <class 'float'>, rated temperature "
        r"type <class 'float'>, or voltage ratio type <class 'NoneType'>.  All should "
        r"be <type 'float'>.",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=None,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_missing_required_args(
    test_stress_limits,
):
    """Raises a TypeError when missing required arguments."""
    with pytest.raises(
        TypeError,
        match=r"missing 1 required keyword-only argument: 'power_ratio'",
    ):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,  # Missing power_ratio
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )
