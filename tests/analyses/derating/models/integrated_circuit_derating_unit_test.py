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
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_no_stresses(
    environment_id,
    test_stress_limits,
):
    """Returns 0 and empty string when integrated circuit is not exceeding any limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        environment_id,
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
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_current(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the current limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.97,
        package_id=3,
        technology_id=2,
        temperature_junction=78.3,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Current ratio of 0.97 exceeds the allowable limit of " "0.9.\n",
            1: "Current ratio of 0.97 exceeds the allowable limit of 0.85.\n",
            2: "Current ratio of 0.97 exceeds the allowable limit of 0.8.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("environment_id", [0, 1, 2])
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_junction_temperature(
    environment_id,
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding the junction temperature limit."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        environment_id,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.8,
        package_id=3,
        technology_id=2,
        temperature_junction=158.3,
    )

    assert _overstress == 1
    assert (
        _reason
        == {
            0: "Temperature of 158.3C exceeds the derated maximum temperature "
            "of 125.0C.\n",
            1: "Temperature of 158.3C exceeds the derated maximum temperature "
            "of 110.0C.\n",
            2: "Temperature of 158.3C exceeds the derated maximum temperature "
            "of 100.0C.\n",
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_all_stresses(
    test_stress_limits,
):
    """Returns 1 and the reason string when exceeding both limits."""
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
        "0.85.\nTemperature of 128.3C exceeds the derated maximum "
        "temperature of 110.0C.\n"
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_environment_id(
    test_stress_limits,
):
    """Raises an IndexError when passed an invalid environment ID."""
    with pytest.raises(
        IndexError,
        match="do_derating_analysis: Invalid integrated circuit environment ID 5.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_subcategory_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid subcategory."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid integrated circuit package ID 3, "
        r"subcategory ID 21, or technology ID 2.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_package_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid package ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid integrated circuit package ID 31, "
        r"subcategory ID 1, or technology ID 2.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_invalid_technology_id(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid technology ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid integrated circuit package ID 3, "
        r"subcategory ID 1, or technology ID 21.",
    ):
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
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed a string current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid integrated circuit current ratio type "
        r"<class 'str'> or junction temperature <class 'float'>.",
    ):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio="0.9",
            package_id=3,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_none_current_ratio(
    test_stress_limits,
):
    """Raises a TypeError when passed None for the current ratio."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid integrated circuit current ratio type "
        r"<class 'NoneType'> or junction temperature <class 'float'>.",
    ):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=None,
            package_id=3,
            technology_id=2,
            temperature_junction=128.3,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_stress_limits")
def test_do_derating_analysis_string_junction_temperature(
    test_stress_limits,
):
    """Raises am TypeError when passed a string junction temperature."""
    with pytest.raises(
        TypeError,
        match=r"do_derating_analysis: Invalid integrated circuit current ratio type "
        r"<class 'float'> or junction temperature <class 'str'>.",
    ):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.9,
            package_id=3,
            technology_id=2,
            temperature_junction="128.3",
        )


@pytest.mark.unit
def test_do_derating_analysis_borderline_current(test_stress_limits):
    """Returns 0 and an empty reason string when the current limit on the boundary."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.85,  # Exactly at the current limit
        package_id=3,
        technology_id=2,
        temperature_junction=78.3,
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_borderline_junction_temperature(test_stress_limits):
    """Returns 1 and an empty reason string when the junction temperature limit is on
    the boundary."""
    _overstress, _reason = integratedcircuit.do_derating_analysis(
        1,
        1,
        test_stress_limits["integrated_circuit"],
        current_ratio=0.8,
        package_id=3,
        technology_id=2,
        temperature_junction=110.0,  # Exactly at the temperature limit
    )

    assert _overstress == 0
    assert _reason == ""


@pytest.mark.unit
def test_do_derating_analysis_missing_required_args(test_stress_limits):
    """Raises a typeError when required arguments are missing."""
    with pytest.raises(
        TypeError,
        match=r"missing 2 required keyword-only arguments: 'current_ratio' and "
        r"'temperature_junction'",
    ):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            package_id=3,
            technology_id=2,
        )


@pytest.mark.unit
def test_do_derating_analysis_invalid_package_technology_combination(
    test_stress_limits,
):
    """Raises a KeyError when passed an invalid combination of package ID and technology
    ID."""
    with pytest.raises(
        KeyError,
        match=r"do_derating_analysis: Invalid integrated circuit package ID 31, "
        r"subcategory ID 1, or technology ID 21.",
    ):
        integratedcircuit.do_derating_analysis(
            1,
            1,
            test_stress_limits["integrated_circuit"],
            current_ratio=0.8,
            package_id=31,  # Invalid package ID
            technology_id=21,  # Invalid technology ID
            temperature_junction=90.0,
        )
