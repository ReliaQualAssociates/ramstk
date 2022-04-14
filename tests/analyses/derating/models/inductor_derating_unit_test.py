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
def test_do_derating_analysis_no_stresses_coil(test_stress_limits):
    """should determine the inductor is not execeeding any limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
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
def test_do_derating_analysis_no_stresses_transformer(test_stress_limits):
    """should determine the transformer is not execeeding any limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
        2,
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
def test_do_derating_analysis_current(test_stress_limits):
    """should determine the inductor is execeeding the voltage limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.863,
        family_id=2,
        temperature_hot_spot=59.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.2,
    )

    assert _overstress == 1
    assert _reason == "Current ratio of 0.863 exceeds the allowable limit of 0.7.\n"


@pytest.mark.unit
def test_do_derating_analysis_hot_spot_temperature(test_stress_limits):
    """should determine the inductor is exceeding the hot spot temperature limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
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
        _reason == "Hot spot temperature of 111.3C exceeds the derated maximum hot "
        "spot temperature of 30.0C less than maximum rated hot spot temperature of "
        "130.0C.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_voltage(test_stress_limits):
    """should determine the inductor is execeeding the voltage limit."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
        1,
        test_stress_limits["inductor"],
        current_ratio=0.2,
        family_id=2,
        temperature_hot_spot=59.3,
        temperature_rated_max=130.0,
        voltage_ratio=0.863,
    )

    assert _overstress == 1
    assert _reason == "Voltage ratio of 0.863 exceeds the allowable limit of 0.7.\n"


@pytest.mark.unit
def test_do_derating_analysis_all_stresses(test_stress_limits):
    """should determine the inductor is execeeding both limits."""
    _overstress, _reason = inductor.do_derating_analysis(
        1,
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
        _reason == "Current ratio of 0.81 exceeds the allowable limit of 0.7.\nHot "
        "spot temperature of 109.3C exceeds the derated maximum hot spot temperature "
        "of 30.0C less than maximum rated hot spot temperature of 130.0C.\nVoltage "
        "ratio of 0.863 exceeds the allowable limit of 0.7.\n"
    )


@pytest.mark.unit
def test_do_derating_analysis_unknown_environment(test_stress_limits):
    """should raise am IndexError when passed an unknown environment."""
    with pytest.raises(IndexError):
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


@pytest.mark.unit
def test_do_derating_analysis_unknown_subcategory(test_stress_limits):
    """should raise am KeyError when passed an unknown subcategory."""
    with pytest.raises(KeyError):
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
def test_do_derating_analysis_unknown_family(test_stress_limits):
    """should raise am KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
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
@pytest.mark.parametrize("current_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_current_ratio(
    current_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=current_ratio,
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.parametrize("hot_spot_temperature", ["128.3", None])
def test_do_derating_analysis_non_numeric_temperature(
    hot_spot_temperature,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric current ratio."""
    with pytest.raises(TypeError):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot=hot_spot_temperature,
            temperature_rated_max=130.0,
            voltage_ratio=0.3,
        )


@pytest.mark.unit
@pytest.mark.parametrize("voltage_ratio", ["0.9", None])
def test_do_derating_analysis_non_numeric_voltage_ratio(
    voltage_ratio,
    test_stress_limits,
):
    """should raise am TypeError when passed a non-numeric voltage ratio."""
    with pytest.raises(TypeError):
        inductor.do_derating_analysis(
            1,
            1,
            test_stress_limits["inductor"],
            current_ratio=0.1,
            family_id=2,
            temperature_hot_spot=51.3,
            temperature_rated_max=130.0,
            voltage_ratio=voltage_ratio,
        )
