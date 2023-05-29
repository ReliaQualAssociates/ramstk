# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.semiconductor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import semiconductor


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """Should determine the semiconductor is not execeeding any limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.5,
        power_ratio=0.3,
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert not _reason


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """Should determine the semiconductor is execeeding the current limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.82,
        power_ratio=0.3,
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.82 exceeds the allowable limit of 0.8.\n"


@pytest.mark.unit
def test_do_derating_analysis_power(test_stress_limits):
    """Should determine the semiconductor is execeeding the power limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.72,
        power_ratio=0.9,
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Power ratio of 0.9 exceeds the allowable limit of 0.8.\n"


@pytest.mark.unit
def test_do_derating_analysis_junction_temperature(test_stress_limits):
    """Should determine semiconductor is execeeding the junction temperature limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.72,
        power_ratio=0.53,
        quality_id=3,
        type_id=3,
        temperature_junction=118.3,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason == "Junction temperature of 118.3C exceeds the allowable limit of "
        "85.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_voltage(test_stress_limits):
    """Should determine the semiconductor is execeeding the voltage limit."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
        3,
        test_stress_limits["semiconductor"],
        current_ratio=0.72,
        power_ratio=0.53,
        quality_id=3,
        type_id=3,
        temperature_junction=78.3,
        voltage_ratio=0.92,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.92 exceeds the allowable limit of 0.75.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """Should determine the semiconductor is execeeding both limits."""
    _overstress, _reason = semiconductor.do_derating_analysis(
        1,
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
        _reason == "Current ratio of 0.92 exceeds the allowable limit of 0.8.\nPower "
        "ratio of 0.93 exceeds the allowable limit of 0.8.\nJunction "
        "temperature of 128.3C exceeds the allowable limit of "
        "85.0C.\nVoltage ratio of 0.92 exceeds the allowable limit of "
        "0.75.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """Should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
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


@pytest.mark.skip
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """Should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
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


@pytest.mark.skip
def test_do_derating_analysis_unknown_quality(test_stress_limits):
    """Should raise am KeyError when passed an unknown quality ID."""
    with pytest.raises(KeyError):
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


@pytest.mark.skip
def test_do_derating_analysis_unknown_type(test_stress_limits):
    """Should raise am KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
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
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=current_ratio,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("power_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_power_ratio(
    power_ratio,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric power ratio."""
    with pytest.raises(TypeError):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio=power_ratio,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("junction_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    junction_temperature,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        semiconductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["semiconductor"],
            current_ratio=0.9,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=junction_temperature,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("voltage_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_voltage_ratio(
    voltage_ratio,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric voltage ratio."""
    with pytest.raises(TypeError):
        semiconductor.do_derating_analysis(
            1,
            3,
            test_stress_limits["semiconductor"],
            current_ratio=0.3,
            power_ratio=0.3,
            quality_id=3,
            type_id=3,
            temperature_junction=68.3,
            voltage_ratio=voltage_ratio,
        )
