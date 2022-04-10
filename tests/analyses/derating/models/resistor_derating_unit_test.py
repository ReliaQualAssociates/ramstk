# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.resistor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import resistor


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """should determine the resistor is not execeeding any limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        specification_id=2,
        temperature_case=46.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_power(test_stress_limits):
    """should determine the resistor is execeeding the power limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.75,
        specification_id=2,
        temperature_case=46.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Power ratio of 0.75 exceeds the allowable limit of 0.65.\n"


@pytest.mark.unit
def test_do_derating_analysis_case_temperature(test_stress_limits):
    """should determine the resistor is exceeding the case temperature limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        specification_id=2,
        temperature_case=126.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason == "Case temperature of 126.3C exceeds the derated maximum temperature "
        "of 122.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_voltage(test_stress_limits):
    """should determine the resistor is execeeding the voltage limit."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.25,
        specification_id=2,
        temperature_case=56.3,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.8,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.8 exceeds the allowable limit of 0.7.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """should determine the resistor is execeeding both limits."""
    _overstress, _reason = resistor.do_derating_analysis(
        1,
        2,
        test_stress_limits["resistor"],
        power_rated=0.125,
        power_ratio=0.75,
        specification_id=2,
        temperature_case=128.4,
        temperature_knee=70.0,
        temperature_rated_max=150.0,
        voltage_ratio=0.8,
    )

    assert _overstress == 1
    assert (
        _reason == "Power ratio of 0.75 exceeds the allowable limit of 0.65.\nCase "
        "temperature of 128.4C exceeds the derated maximum temperature of "
        "122.0C.\nVoltage ratio of 0.8 exceeds the allowable limit of 0.7.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        resistor.do_derating_analysis(
            5,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            specification_id=2,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
        resistor.do_derating_analysis(
            1,
            21,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            specification_id=2,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.parametrize("power_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_power_ratio(
    power_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric voltage ratio."""
    with pytest.raises(TypeError):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=power_ratio,
            specification_id=2,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("case_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    case_temperature,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            specification_id=2,
            temperature_case=case_temperature,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=0.28,
        )


@pytest.mark.unit
@pytest.mark.parametrize("voltage_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_voltage_ratio(
    voltage_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric voltage ratio."""
    with pytest.raises(TypeError):
        resistor.do_derating_analysis(
            1,
            2,
            test_stress_limits["resistor"],
            power_rated=0.125,
            power_ratio=0.25,
            specification_id=2,
            temperature_case=68.4,
            temperature_knee=70.0,
            temperature_rated_max=150.0,
            voltage_ratio=voltage_ratio,
        )
