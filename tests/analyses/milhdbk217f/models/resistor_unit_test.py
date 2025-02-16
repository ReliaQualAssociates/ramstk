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


# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import resistor
from ramstk.constants.resistor import PART_STRESS_PI_Q, PI_E


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
)
def test_set_default_resistance(
    subcategory_id,
):
    """Returns the default resistance for the selected subcategory ID."""
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
def test_set_default_elements(
    subcategory_id,
):
    """Returns the default elements for the selected subcategory ID."""
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
def test_set_default_values(
    test_attributes_resistor,
):
    """Sets default values for each parameter <= 0.0."""
    test_attributes_resistor["n_elements"] = -1
    test_attributes_resistor["power_ratio"] = -1.0
    test_attributes_resistor["resistance"] = 0.0
    test_attributes_resistor["subcategory_id"] = 4
    test_attributes_resistor["temperature_active"] = 35.0
    test_attributes_resistor["temperature_case"] = -10.0
    _attributes = resistor.set_default_values(test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert _attributes["resistance"] == 1000.0
    assert _attributes["power_ratio"] == 0.5
    assert _attributes["temperature_case"] == 63.0
    assert _attributes["n_elements"] == 10


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_set_default_values_none_needed(
    test_attributes_resistor,
):
    """Sets nothing when each parameter > 0.0."""
    test_attributes_resistor["n_elements"] = 4
    test_attributes_resistor["power_ratio"] = 0.2
    test_attributes_resistor["resistance"] = 4700.0
    test_attributes_resistor["subcategory_id"] = 10
    test_attributes_resistor["temperature_active"] = 35.0
    test_attributes_resistor["temperature_case"] = 72.0
    _attributes = resistor.set_default_values(test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert _attributes["resistance"] == 4700.0
    assert _attributes["power_ratio"] == 0.2
    assert _attributes["temperature_case"] == 72.0
    assert _attributes["n_elements"] == 4


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize(
    "subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
)
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_lambda_b(
    subcategory_id,
    environment_active_id,
    test_attributes_resistor,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_resistor["environment_active_id"] = environment_active_id
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = subcategory_id
    _lambda_b = resistor.get_part_count_lambda_b(test_attributes_resistor)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
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
            ],
            2: [
                0.0012,
                0.0027,
                0.011,
                0.0054,
                0.020,
                0.0063,
                0.013,
                0.018,
                0.033,
                0.030,
                0.00025,
                0.014,
                0.044,
                0.69,
            ],
            3: [
                0.012,
                0.025,
                0.13,
                0.062,
                0.21,
                0.078,
                0.10,
                0.19,
                0.24,
                0.32,
                0.0060,
                0.18,
                0.47,
                8.2,
            ],
            4: [
                0.0023,
                0.0066,
                0.031,
                0.013,
                0.055,
                0.022,
                0.043,
                0.077,
                0.15,
                0.10,
                0.0011,
                0.055,
                0.15,
                1.7,
            ],
            5: [
                0.0085,
                0.018,
                0.10,
                0.045,
                0.16,
                0.15,
                0.17,
                0.30,
                0.38,
                0.26,
                0.0068,
                0.13,
                0.37,
                5.4,
            ],
            6: [
                0.014,
                0.031,
                0.16,
                0.077,
                0.26,
                0.073,
                0.15,
                0.19,
                0.39,
                0.42,
                0.0042,
                0.21,
                0.62,
                9.4,
            ],
            7: [
                0.008,
                0.18,
                0.096,
                0.045,
                0.15,
                0.044,
                0.088,
                0.12,
                0.24,
                0.25,
                0.004,
                0.13,
                0.37,
                5.5,
            ],
            8: [
                0.065,
                0.32,
                1.4,
                0.71,
                1.6,
                0.71,
                1.9,
                1.0,
                2.7,
                2.4,
                0.032,
                1.3,
                3.4,
                62.0,
            ],
            9: [
                0.025,
                0.055,
                0.35,
                0.15,
                0.58,
                0.16,
                0.26,
                0.35,
                0.58,
                1.1,
                0.013,
                0.52,
                1.6,
                24.0,
            ],
            10: [
                0.33,
                0.73,
                7.0,
                2.9,
                12.0,
                3.5,
                5.3,
                7.1,
                9.8,
                23.0,
                0.16,
                11.0,
                33.0,
                510.0,
            ],
            11: [
                0.15,
                0.35,
                3.1,
                1.2,
                5.4,
                1.9,
                2.8,
                0.0,
                0.0,
                9.0,
                0.075,
                0.0,
                0.0,
                0.0,
            ],
            12: [
                0.15,
                0.34,
                2.9,
                1.2,
                5.0,
                1.6,
                2.4,
                0.0,
                0.0,
                7.6,
                0.076,
                0.0,
                0.0,
                0.0,
            ],
            13: [
                0.043,
                0.15,
                0.75,
                0.35,
                1.3,
                0.39,
                0.78,
                1.8,
                2.8,
                2.5,
                0.21,
                1.2,
                3.7,
                49.0,
            ],
            14: [
                0.05,
                0.11,
                1.1,
                0.45,
                1.7,
                2.8,
                4.6,
                4.6,
                7.5,
                3.3,
                0.025,
                1.5,
                4.7,
                67.0,
            ],
            15: [
                0.048,
                0.16,
                0.76,
                0.36,
                1.3,
                0.36,
                0.72,
                1.4,
                2.2,
                2.3,
                0.024,
                1.2,
                3.4,
                52.0,
            ],
        }[subcategory_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_resistor,
):
    """Raises an IndexError if passed an invalid active environment ID."""
    test_attributes_resistor["environment_active_id"] = 24
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = 2
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid resistor environment ID 24.",
    ):
        resistor.get_part_count_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_resistor,
):
    """Raises a KeyError if passed an invalid subcategory ID."""
    test_attributes_resistor["environment_active_id"] = 2
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = 28
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid resistor specification ID 1 or "
        r"subcategory ID 28.",
    ):
        resistor.get_part_count_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_lambda_b_invalid_specification_id(
    test_attributes_resistor,
):
    """Raises a KeyError if passed an invalid specification ID."""
    test_attributes_resistor["environment_active_id"] = 1
    test_attributes_resistor["specification_id"] = 24
    test_attributes_resistor["subcategory_id"] = 2
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid resistor specification ID 24 or "
        r"subcategory ID 2.",
    ):
        resistor.get_part_count_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6])
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_quality_factor(
    quality_id,
    test_attributes_resistor,
):
    """Returns a float value for the quality factor (piQ) for the passed quality ID."""
    test_attributes_resistor["quality_id"] = quality_id
    _pi_q = resistor.get_part_count_quality_factor(test_attributes_resistor)

    assert isinstance(_pi_q, float)
    assert _pi_q == [0.030, 0.10, 0.30, 1.0, 3.0, 10.0][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_resistor,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_resistor["quality_id"] = 7
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid resistor quality ID 7.",
    ):
        resistor.get_part_count_quality_factor(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 8])
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    test_attributes_resistor,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_resistor["power_ratio"] = 0.45
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = subcategory_id
    test_attributes_resistor["temperature_active"] = 39.5
    test_attributes_resistor["type_id"] = 1
    _lambda_b = resistor.calculate_part_stress_lambda_b(test_attributes_resistor)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(
        {
            1: 0.00059453715,
            2: 0.0083680087,
            4: 6e-05,
            8: 0.021,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress_lambda_b_invalid_type_id(
    test_attributes_resistor,
):
    """Raises an IndexError when passed an invalid type ID."""
    test_attributes_resistor["power_ratio"] = 0.45
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = 8
    test_attributes_resistor["temperature_active"] = 39.5
    test_attributes_resistor["type_id"] = 10
    with pytest.raises(
        IndexError,
        match=r"calculate_part_stress_lambda_b: Invalid resistor type ID 10.",
    ):
        resistor.calculate_part_stress_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress_lambda_b_invalid_specification_id(
    test_attributes_resistor,
):
    """Raises an KeyError when passed an invalid specification ID."""
    test_attributes_resistor["power_ratio"] = 0.45
    test_attributes_resistor["specification_id"] = 15
    test_attributes_resistor["subcategory_id"] = 2
    test_attributes_resistor["temperature_active"] = 39.5
    test_attributes_resistor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid resistor specification ID 15 "
        r"or subcategory_id 2.",
    ):
        resistor.calculate_part_stress_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress_lambda_b_invalid_subcategory_id(
    test_attributes_resistor,
):
    """Raises an KeyError when passed an invalid subcategory ID."""
    test_attributes_resistor["power_ratio"] = 0.45
    test_attributes_resistor["specification_id"] = 1
    test_attributes_resistor["subcategory_id"] = 83
    test_attributes_resistor["temperature_active"] = 39.5
    test_attributes_resistor["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid resistor specification ID 1 "
        r"or subcategory_id 83.",
    ):
        resistor.calculate_part_stress_lambda_b(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize(
    "subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
)
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_environment_factor(
    environment_active_id,
    subcategory_id,
    test_attributes_resistor,
):
    """Returns a float value for the environment factor (piE)."""
    test_attributes_resistor["environment_active_id"] = environment_active_id
    test_attributes_resistor["subcategory_id"] = subcategory_id
    _pi_e = resistor.get_environment_factor(test_attributes_resistor)

    assert isinstance(_pi_e, float)
    assert _pi_e == PI_E[subcategory_id][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_resistor,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_resistor["environment_active_id"] = 52
    test_attributes_resistor["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid resistor environment ID 52.",
    ):
        resistor.get_environment_factor(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_resistor,
):
    """Raises a KeyError when passed an invalid subcategpry ID."""
    test_attributes_resistor["environment_active_id"] = 2
    test_attributes_resistor["subcategory_id"] = 101
    with pytest.raises(
        KeyError, match=r"get_environment_id: Invalid resistor subcategory ID 101."
    ):
        resistor.get_environment_factor(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize(
    "subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
)
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_stress_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_resistor,
):
    """Returns a float value for the quality factor (piQ)."""
    test_attributes_resistor["quality_id"] = quality_id
    test_attributes_resistor["subcategory_id"] = subcategory_id
    _pi_q = resistor.get_part_stress_quality_factor(test_attributes_resistor)

    assert isinstance(_pi_q, float)
    assert _pi_q == PART_STRESS_PI_Q[subcategory_id][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_resistor,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_resistor["quality_id"] = 52
    test_attributes_resistor["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid resistor quality ID 52.",
    ):
        resistor.get_part_stress_quality_factor(test_attributes_resistor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_get_part_stress_quality_factor_invalid_subcategory_id(
    test_attributes_resistor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_resistor["quality_id"] = 2
    test_attributes_resistor["subcategory_id"] = 101
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid resistor subcategory ID 101.",
    ):
        resistor.get_part_stress_quality_factor(test_attributes_resistor)


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
    assert (
        _pi_r
        == {
            1: 1.1,
            4: 0.0,
            6: 1.2,
        }[subcategory_id]
    )


@pytest.mark.unit
def test_get_resistance_factor_invalid_family_id():
    """Raises an IndexError when passed an invalid family ID."""
    with pytest.raises(
        IndexError,
        match=r"get_resistance_factor: Invalid resistor family ID 52 or "
        r"specification ID 1.",
    ):
        resistor.get_resistance_factor(
            6,
            1,
            52,
            3300,
        )


@pytest.mark.unit
def test_get_resistance_factor_invalid_specification_id():
    """Raises an IndexError when passed an invalid specification ID."""
    with pytest.raises(
        IndexError,
        match=r"get_resistance_factor: Invalid resistor family ID 2 or specification "
        r"ID 71.",
    ):
        resistor.get_resistance_factor(
            6,
            71,
            2,
            3300,
        )


@pytest.mark.unit
def test_get_resistance_factor_invalid_subcategory_id():
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"get_resistance_factor: Invalid resistor subcategory ID 16.",
    ):
        resistor.get_resistance_factor(
            16,
            1,
            2,
            3300,
        )


@pytest.mark.unit
def test_calculate_temperature_factor():
    """Returns a tuple of two float values for case temperature and piT on success."""
    _temperature_case, _pi_t = resistor.calculate_temperature_factor(38.2, 0.45)

    assert isinstance(_temperature_case, float)
    assert isinstance(_pi_t, float)
    assert _temperature_case == 62.95
    assert _pi_t == pytest.approx(4.653004187)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [9, 13])
def test_get_voltage_factor(subcategory_id):
    """Returns a float value for the voltage factor (piV) on success."""
    _pi_v = resistor.get_voltage_factor(subcategory_id, 0.85)

    assert isinstance(_pi_v, float)
    assert _pi_v == {9: 1.4, 13: 1.05}[subcategory_id]


@pytest.mark.unit
def test_get_voltage_factor_invalid_subcategory_id():
    """Raises a KeyError if passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError, match="get_voltage_factor: Invalid resistor subcategory ID 71."
    ):
        resistor.get_voltage_factor(71, 0.85)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 4, 9, 10])
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_resistor,
):
    """Returns the attributes dict with updated values on success."""
    test_attributes_resistor["hazard_rate_active"] = 0.001217492
    test_attributes_resistor["subcategory_id"] = subcategory_id
    _attributes = resistor.calculate_part_stress(test_attributes_resistor)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == pytest.approx(
        {
            1: 0.0013392412,
            4: 0.01663181,
            9: 0.003408453,
            10: 0.006816906,
        }[subcategory_id]
    )
    if subcategory_id == 10:
        assert _attributes["piTAPS"] == 0.9998460969082653
        assert _attributes["piC"] == 2.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_resistor")
def test_calculate_part_stress_missing_attribute_key(
    test_attributes_resistor,
):
    """Raises a KeyError when a required attribute is missing."""
    test_attributes_resistor.pop("power_ratio")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required resistor attribute: "
        r"'power_ratio'.",
    ):
        resistor.calculate_part_stress(test_attributes_resistor)
