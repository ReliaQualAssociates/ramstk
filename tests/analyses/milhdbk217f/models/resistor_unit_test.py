# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk271f.models.resistor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the resistor module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import resistor


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
def test_get_part_count_lambda_b(
    subcategory_id,
    environment_active_id,
):
    """get_part_count_lambda_b() should return a float value for the parts count base
    hazard rate on success."""
    _lambda_b = resistor.get_part_count_lambda_b(
        subcategory_id,
        environment_active_id,
        1,
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert (
            _lambda_b
            == [
                0.0005,
                0.0022,
                0.0071,
                0.0037,
                0.012,
                0.0052,
                0.0065,
                0.016,
                0.025,
                0.025,
                0.00025,
                0.0098,
                0.035,
                0.36,
            ][environment_active_id - 1]
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        resistor.get_part_count_lambda_b(
            28,
            2,
            1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_specification():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    specification ID."""
    with pytest.raises(KeyError):
        resistor.get_part_count_lambda_b(
            2,
            1,
            24,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active
    environment ID."""
    with pytest.raises(IndexError):
        resistor.get_part_count_lambda_b(
            2,
            24,
            1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_count(test_attributes_resistor):
    """calculate_part_count() should return a float value for the parts count base
    hazard rate on success."""
    _lambda_b = resistor.calculate_part_count(**test_attributes_resistor)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.0071


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 8])
def test_calculate_part_stress_lambda_b(subcategory_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard
    rate on success."""
    _lambda_b = resistor.calculate_part_stress_lambda_b(
        subcategory_id,
        1,
        1,
        39.5,
        0.45,
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == pytest.approx(0.00059453715)
    elif subcategory_id == 2:
        assert _lambda_b == pytest.approx(0.0083680087)
    elif subcategory_id == 4:
        assert _lambda_b == 6e-05
    elif subcategory_id == 8:
        assert _lambda_b == 0.021


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 4, 6])
def test_get_resistance_factor(subcategory_id):
    """calculate_resistance_factor() should return a float value for piR on success."""
    _pi_r = resistor.get_resistance_factor(
        subcategory_id,
        1,
        2,
        3300,
    )

    assert isinstance(_pi_r, float)
    if subcategory_id == 1:
        assert _pi_r == 1.1
    elif subcategory_id == 4:
        assert _pi_r == 0.0
    elif subcategory_id == 6:
        assert _pi_r == 1.2


@pytest.mark.unit
def test_get_resistance_factor_no_specification():
    """calculate_resistance_factor() should raise an IndexError when passed an unknown
    specification ID."""
    with pytest.raises(IndexError):
        resistor.get_resistance_factor(
            6,
            71,
            2,
            3300,
        )


@pytest.mark.unit
def test_get_resistance_factor_no_family():
    """calculate_resistance_factor() should raise an IndexError when passed an unknown
    family ID."""
    with pytest.raises(IndexError):
        resistor.get_resistance_factor(
            6,
            1,
            21,
            3300,
        )


@pytest.mark.unit
def test_get_resistance_factor_no_subcategory():
    """calculate_resistance_factor() should raise a KeyError when passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        resistor.get_resistance_factor(
            61,
            1,
            2,
            3300,
        )


@pytest.mark.unit
def test_calculate_temperature_factor():
    """calculate_temperature_factor() should return a tuple of two float values for
    case temperature and piT on success."""
    _temperature_case, _pi_t = resistor.calculate_temperature_factor(38.2, 0.45)

    assert isinstance(_temperature_case, float)
    assert isinstance(_pi_t, float)
    assert _temperature_case == 62.95
    assert _pi_t == pytest.approx(4.653004187)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [9, 13])
def test_get_voltage_factor(subcategory_id):
    """get_voltage_factor() should return a float value for piV on success."""
    _pi_v = resistor.get_voltage_factor(subcategory_id, 0.85)

    assert isinstance(_pi_v, float)
    assert _pi_v == {9: 1.4, 13: 1.05}[subcategory_id]


@pytest.mark.unit
def test_get_voltage_factor_no_subcategory():
    """get_voltage_factor() should raise a KeyError if passed an unknown subcategory
    ID."""
    with pytest.raises(KeyError):
        resistor.get_voltage_factor(71, 0.85)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
@pytest.mark.parametrize("subcategory_id", [1, 4, 9, 10])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_resistor,
):
    """calculate_part_stress() should return the attributes dict with updated values on
    success."""
    test_attributes_resistor["subcategory_id"] = subcategory_id
    _attributes = resistor.calculate_part_stress(**test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert (
        _attributes["hazard_rate_active"]
        == {
            1: 0.001217492244190985,
            4: 0.0016392858777726734,
            9: 4.434316747334665,
            10: 56.840234045545884,
        }[subcategory_id]
    )
    if subcategory_id == 10:
        assert _attributes["piTAPS"] == 0.9998460969082653
        assert _attributes["piC"] == 2.0


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
)
def test_set_default_resistance(subcategory_id):
    """should return the default resistance for the selected subcategory ID."""
    _resistance = resistor._set_default_resistance(0.0, subcategory_id)

    assert (
        _resistance
        == {
            1: 1000000.0,
            2: 1000000.0,
            3: 100.0,
            4: 1000.0,
            5: 100000.0,
            6: 5000.0,
            7: 5000.0,
            8: 1000.0,
            9: 5000.0,
            10: 50000.0,
            11: 5000.0,
            12: 5000.0,
            13: 200000.0,
            14: 200000.0,
            15: 200000.0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
)
def test_set_default_elements(subcategory_id):
    """should return the default elements for the selected subcategory ID."""
    _n_elements = resistor._set_default_elements(0.0, subcategory_id)

    assert (
        _n_elements
        == {
            1: 0,
            2: 0,
            3: 0,
            4: 10,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 3,
            10: 3,
            11: 3,
            12: 3,
            13: 3,
            14: 3,
            15: 3,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_set_default_values(test_attributes_resistor):
    """should set default values for each parameter <= 0.0."""
    test_attributes_resistor["n_elements"] = -1
    test_attributes_resistor["power_ratio"] = -1.0
    test_attributes_resistor["resistance"] = 0.0
    test_attributes_resistor["subcategory_id"] = 4
    test_attributes_resistor["temperature_active"] = 35.0
    test_attributes_resistor["temperature_case"] = -10.0
    _attributes = resistor.set_default_values(**test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert _attributes["resistance"] == 1000.0
    assert _attributes["power_ratio"] == 0.5
    assert _attributes["temperature_case"] == 63.0
    assert _attributes["n_elements"] == 10


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_set_default_values_none_needed(test_attributes_resistor):
    """should set default values for each parameter <= 0.0."""
    test_attributes_resistor["n_elements"] = 4
    test_attributes_resistor["power_ratio"] = 0.2
    test_attributes_resistor["resistance"] = 4700.0
    test_attributes_resistor["subcategory_id"] = 10
    test_attributes_resistor["temperature_active"] = 35.0
    test_attributes_resistor["temperature_case"] = 72.0
    _attributes = resistor.set_default_values(**test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert _attributes["resistance"] == 4700.0
    assert _attributes["power_ratio"] == 0.2
    assert _attributes["temperature_case"] == 72.0
    assert _attributes["n_elements"] == 4
