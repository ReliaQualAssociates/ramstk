# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.capacitor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import capacitor


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """Should determine the capacitor is not execeeding any limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=46.3,
        temperature_rated_max=70.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_case_temperature(test_stress_limits):
    """Should determine the capacitor is exceeding the case temperature limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=79.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 79.3C exceeds the derated maximum temperature "
        "of 10.0C less than maximum rated temperature of 85.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_voltage(test_stress_limits):
    """Should determine the capacitor is execeeding the voltage limit."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=59.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.95,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.95 exceeds the allowable limit of 0.6.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """Should determine the capacitor is execeeding both limits."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=79.3,
        temperature_rated_max=85.0,
        voltage_ratio=0.95,
    )

    assert _overstress == 1
    assert (
        _reason == "Temperature of 79.3C exceeds the derated maximum temperature "
        "of 10.0C less than maximum rated temperature of 85.0C.\nVoltage ratio of 0.95 "
        "exceeds the allowable limit of 0.6.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """Should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        capacitor.do_derating_analysis(
            5,
            10,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """Should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
        capacitor.do_derating_analysis(
            1,
            21,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_specification(test_stress_limits):
    """Should raise am ValueError when passed an unknown type ID."""
    with pytest.raises(ValueError):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=22,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
@pytest.mark.parametrize("case_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    case_temperature,
    test_stress_limits,
):
    """Should raise am TypeError when passed a non-numeric case temperature."""
    with pytest.raises(TypeError):
        capacitor.do_derating_analysis(
            1,
            1,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=case_temperature,
            temperature_rated_max=70.0,
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
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=2,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=voltage_ratio,
        )


@pytest.mark.unit
def test_do_derating_analysis_borderline_temperature(test_stress_limits):
    """Should determine the capacitor is not exceeding the case temperature limit on the
    boundary."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=60.0,  # Exactly at the boundary
        temperature_rated_max=70.0,
        voltage_ratio=0.5,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_borderline_voltage(test_stress_limits):
    """Should determine the capacitor is not exceeding the voltage limit on the
    boundary."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=46.3,
        temperature_rated_max=70.0,
        voltage_ratio=0.6,  # Exactly at the voltage limit
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_nominal_values(test_stress_limits):
    """Should not report overstress when all values are within limits."""
    _overstress, _reason = capacitor.do_derating_analysis(
        1,
        11,
        test_stress_limits["capacitor"],
        specification_id=2,
        temperature_case=45.0,
        temperature_rated_max=70.0,
        voltage_ratio=0.4,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_string_specification_id(test_stress_limits):
    """Should raise a ValueError when passed a str for specification ID."""
    with pytest.raises(ValueError):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id="1",
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


@pytest.mark.unit
def test_do_derating_analysis_none_specification_id(test_stress_limits):
    """Should raise a ValueError when passed None for specification ID."""
    with pytest.raises(ValueError):
        capacitor.do_derating_analysis(
            1,
            11,
            test_stress_limits["capacitor"],
            specification_id=None,
            temperature_case=46.3,
            temperature_rated_max=70.0,
            voltage_ratio=0.2,
        )


def test_resolve_subcategory_success():
    """Test resolving subcategory successfully."""
    assert capacitor._do_resolve_subcategory(11, 1) == "temp_comp_ceramic"
    assert capacitor._do_resolve_subcategory(11, 2) == "ceramic_chip"
    assert capacitor._do_resolve_subcategory(1, None) == "paper"


@pytest.mark.unit
def test_resolve_subcategory_invalid_subcategory():
    """Test _do_resolve_subcategory with invalid subcategory_id."""
    with pytest.raises(KeyError):
        capacitor._do_resolve_subcategory(99, None)


@pytest.mark.unit
def test_resolve_subcategory_missing_specification():
    """Test _do_resolve_subcategory when specification_id is required but missing."""
    with pytest.raises(ValueError):
        capacitor._do_resolve_subcategory(11, None)


@pytest.mark.unit
def test_resolve_subcategory_invalid_specification():
    """Test _do_resolve_subcategory with invalid specification_id."""
    with pytest.raises(ValueError):
        capacitor._do_resolve_subcategory(11, 99)
