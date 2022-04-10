# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.derating.models.integrated_circuit_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the integrated circuit derating module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.derating import integratedcircuit


@pytest.mark.unit
def test_do_derating_analysis_no_stresses(test_stress_limits):
    """should determine the integrated circuit is not execeeding any limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.5,
        package_id=3,
        technology_id=2,
        temperature_junction=78.3,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_current(test_stress_limits):
    """should determine the integrated circuit is execeeding the current limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.87,
        package_id=3,
        technology_id=2,
        temperature_junction=78.3,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.87 exceeds the allowable limit of 0.85.\n"


@pytest.mark.unit
def test_do_derating_analysis_junction_temperature(test_stress_limits):
    """should determine the integrated circuit is execeeding the junction temperature
    limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.8,
        package_id=3,
        technology_id=2,
        temperature_junction=118.3,
    )

    assert _overstress == 1
    assert (
        _reason == "Junction temperature of 118.3C exceeds the allowable limit of "
        "110.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """should determine the integrated circuit is execeeding both limits."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.9,
        package_id=3,
        technology_id=2,
        temperature_junction=128.3,
    )

    assert _overstress == 1
    assert (
        _reason == "Current ratio of 0.9 exceeds the allowable limit of "
        "0.85.\nJunction temperature of 128.3C exceeds the allowable limit "
        "of 110.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
        integratedcircuit.do_derating_analysis(
            5,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=3,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
        integratedcircuit.do_derating_analysis(
            1,
            21,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=3,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_package(test_stress_limits):
    """should raise am KeyError when passed an unknown package ID."""
    with pytest.raises(KeyError):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=31,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
def test_do_derating_analysis_unknown_technology(test_stress_limits):
    """should raise am KeyError when passed an unknown technology ID."""
    with pytest.raises(KeyError):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=3,
            technology_id=21,
            temperature_junction=128.3,
        )


@pytest.mark.unit
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=current_ratio,
            package_id=3,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
@pytest.mark.parametrize("junction_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    junction_temperature,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=3,
            technology_id=2,
            temperature_junction=junction_temperature,
        )
