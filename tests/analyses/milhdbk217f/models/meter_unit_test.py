# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.meter_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the meter module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import meter


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_set_default_values(
    test_attributes_meter,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_meter["quality_id"] = 1
    _attributes = meter.set_default_values(test_attributes_meter)

    assert isinstance(_attributes, dict)
    assert _attributes["quality_id"] == 1


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_lambda_b(
    subcategory_id,
    type_id,
    environment_active_id,
    test_attributes_meter,
):
    """get_part_count_lambda_b() should return a float value for the parts count base
    hazard rate on success."""
    test_attributes_meter["environment_active_id"] = environment_active_id
    test_attributes_meter["subcategory_id"] = subcategory_id
    test_attributes_meter["type_id"] = type_id
    _lambda_b = meter.get_part_count_lambda_b(test_attributes_meter)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: {
                1: [
                    10.0,
                    20.0,
                    120.0,
                    70.0,
                    180.0,
                    50.0,
                    80.0,
                    160.0,
                    250.0,
                    260.0,
                    5.0,
                    140.0,
                    380.0,
                    0.0,
                ],
                2: [
                    15.0,
                    30.0,
                    180.0,
                    105.0,
                    270.0,
                    75.0,
                    120.0,
                    240.0,
                    375.0,
                    390.0,
                    7.5,
                    210.0,
                    570.0,
                    0.0,
                ],
                3: [
                    40.0,
                    80.0,
                    480.0,
                    280.0,
                    720.0,
                    200.0,
                    320.0,
                    640.0,
                    1000.0,
                    1040.0,
                    20.0,
                    560.0,
                    1520.0,
                    0.0,
                ],
            },
            2: {
                1: [
                    0.09,
                    0.36,
                    2.3,
                    1.1,
                    3.2,
                    2.5,
                    3.8,
                    5.2,
                    6.6,
                    5.4,
                    0.099,
                    5.4,
                    0.0,
                    0.0,
                ],
                2: [
                    0.15,
                    0.61,
                    2.8,
                    1.8,
                    5.4,
                    4.3,
                    6.4,
                    8.9,
                    11.0,
                    9.2,
                    0.17,
                    9.2,
                    0.0,
                    0.0,
                ],
            },
        }[subcategory_id][type_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_meter,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_meter["subcategory_id"] = 47
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid meter subcategory ID 47 or type ID 2.",
    ):
        meter.get_part_count_lambda_b(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_lambda_b_invalid_type_id(
    test_attributes_meter,
):
    """Raises a KeyError when passed an invalid type ID."""
    test_attributes_meter["type_id"] = 12
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid meter subcategory ID 1 or type ID 12.",
    ):
        meter.get_part_count_lambda_b(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_meter,
):
    """Raises an IndexError when passed an invalid environment ID."""
    test_attributes_meter["environment_active_id"] = 24
    with pytest.raises(
        IndexError, match=r"get_part_count_lambda_b: Invalid meter environment ID 24."
    ):
        meter.get_part_count_lambda_b(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_meter,
):
    """Returns a float value for the quality factor (piQ) on success."""
    test_attributes_meter["quality_id"] = quality_id
    test_attributes_meter["subcategory_id"] = subcategory_id
    _pi_q = meter.get_part_count_quality_factor(test_attributes_meter)

    assert isinstance(_pi_q, float)
    assert (
        _pi_q
        == {
            1: [1.0, 1.0],
            2: [1.0, 3.4],
        }[
            subcategory_id
        ][quality_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_quality_factor_invalid_subcategory_id(
    test_attributes_meter,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_meter["quality_id"] = 1
    test_attributes_meter["subcategory_id"] = 68
    with pytest.raises(
        KeyError,
        match=r"get_part_count_quality_factor: Invalid meter subcategory ID 68.",
    ):
        meter.get_part_count_quality_factor(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_meter,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_meter["quality_id"] = 66
    test_attributes_meter["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid meter quality ID 66.",
    ):
        meter.get_part_count_quality_factor(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2, 3])
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_stress_lambda_b(
    subcategory_id,
    type_id,
    test_attributes_meter,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_meter["subcategory_id"] = subcategory_id
    test_attributes_meter["type_id"] = type_id
    _lambda_b = meter.get_part_stress_lambda_b(test_attributes_meter)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == [20.0, 30.0, 80.0][type_id - 1]
    elif subcategory_id == 2:
        assert _lambda_b == 0.09


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_stress_lambda_b_invalid_type_id(
    test_attributes_meter,
):
    """Raises an IndexError when passed an invalid type ID."""
    test_attributes_meter["type_id"] = 4
    with pytest.raises(
        IndexError, match=r"get_part_stress_lambda_b: Invalid meter type ID 4."
    ):
        meter.get_part_stress_lambda_b(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_stress_lambda_b_invalid_subcategory_id(
    test_attributes_meter,
):
    """Returns 0.0 when passed an invalid subcategory ID."""
    test_attributes_meter["subcategory_id"] = 10

    assert meter.get_part_stress_lambda_b(test_attributes_meter) == 0.0


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_environment_factor(
    environment_active_id,
    subcategory_id,
    test_attributes_meter,
):
    """Returns a float value for the environment factor on success."""
    test_attributes_meter["environment_active_id"] = environment_active_id
    test_attributes_meter["subcategory_id"] = subcategory_id
    _pi_e = meter.get_environment_factor(test_attributes_meter)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == {
            1: [
                1.0,
                2.0,
                12.0,
                7.0,
                18.0,
                5.0,
                8.0,
                16.0,
                25.0,
                26.0,
                0.5,
                14.0,
                38.0,
                0.0,
            ],
            2: [
                1.0,
                4.0,
                25.0,
                12.0,
                35.0,
                28.0,
                42.0,
                58.0,
                73.0,
                60.0,
                1.1,
                60.0,
                0.0,
                0.0,
            ],
        }[subcategory_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_meter,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_meter["subcategory_id"] = 12
    with pytest.raises(
        KeyError, match=r"get_environment_factor: Invalid meter subcategory ID 12."
    ):
        meter.get_environment_factor(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_meter,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_meter["environment_active_id"] = 22
    with pytest.raises(
        IndexError, match=r"get_environment_factor: Invalid meter environment ID 22."
    ):
        meter.get_environment_factor(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2])
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_stress_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_meter,
):
    """Returns a float value for the quality factor."""
    test_attributes_meter["quality_id"] = quality_id
    test_attributes_meter["subcategory_id"] = subcategory_id
    _pi_q = meter.get_part_stress_quality_factor(test_attributes_meter)

    assert isinstance(_pi_q, float)
    if subcategory_id == 1:
        assert _pi_q == 1.0
    else:
        assert _pi_q == [1.0, 3.4][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_meter,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_meter["quality_id"] = 33
    test_attributes_meter["subcategory_id"] = 2
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid meter quality ID 33.",
    ):
        meter.get_part_stress_quality_factor(test_attributes_meter)


@pytest.mark.unit
@pytest.mark.parametrize("temperature_active", [25.0, 40.0, 55.0, 70.0])
def test_get_temperature_stress_factor(
    temperature_active,
):
    """Returns a float value for piT on success."""
    _pi_t = meter.get_temperature_stress_factor(temperature_active, 75.0)

    assert isinstance(_pi_t, float)
    assert _pi_t == {25.0: 0.5, 40.0: 0.6, 55.0: 0.8, 70.0: 1.0}[temperature_active]


@pytest.mark.unit
def test_get_temperature_stress_factor_zero_max_rated_temperature():
    """get_temperature_stress_factor() should raise a ZeroDivisionError when passed a
    maximum rated temperature of 0.0."""
    with pytest.raises(
        ZeroDivisionError,
        match=r"get_temperature_stress_factor: Meter maximum rated temperature "
        r"cannot be zero.",
    ):
        meter.get_temperature_stress_factor(35.0, 0.0)


@pytest.mark.unit
def test_get_temperature_stress_factor_wrong_type():
    """Raises a TypeError when passed a string for either temperature."""
    with pytest.raises(
        TypeError,
        match=r"get_temperature_stress_factor: Meter active temperature <class 'str'> "
        r"and maximum rated temperature <class 'float'> must both be non-negative "
        r"numbers.",
    ):
        meter.get_temperature_stress_factor("35.0", 75.0)

    with pytest.raises(
        TypeError,
        match=r"get_temperature_stress_factor: Meter active temperature "
        r"<class 'float'> and maximum rated temperature <class 'str'> must both "
        r"be non-negative numbers.",
    ):
        meter.get_temperature_stress_factor(35.0, "75.0")


@pytest.mark.unit
def test_get_temperature_stress_factor_temp_ratio_greater_than_one():
    """Returns 0.0 when the calculated temperature ratio is greater than 1.0."""
    _pi_t = meter.get_temperature_stress_factor(35.0, 1.0)

    assert _pi_t == 0.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_calculate_part_stress_elapsed_time_meter(
    test_attributes_meter,
):
    """Returns a dictionary of updated values on success."""
    test_attributes_meter["hazard_rate_active"] = 30.0
    _attributes = meter.calculate_part_stress(test_attributes_meter)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == 15.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_calculate_part_stress_panel_meter(
    test_attributes_meter,
):
    """Returns a dictionary of updated values on success."""
    test_attributes_meter["hazard_rate_active"] = 0.09
    test_attributes_meter["subcategory_id"] = 2
    _attributes = meter.calculate_part_stress(test_attributes_meter)

    assert isinstance(_attributes, dict)
    assert _attributes["piA"] == 1.7
    assert _attributes["piF"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.153)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_meter")
def test_calculate_part_stress_missing_attribute_key(
    test_attributes_meter,
):
    """Raises a KeyError when a required attribute is missing."""
    test_attributes_meter.pop("temperature_rated_max")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required meter attribute: "
        r"'temperature_rated_max'.",
    ):
        meter.calculate_part_stress(test_attributes_meter)
