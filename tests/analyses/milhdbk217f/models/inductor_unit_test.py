# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.inductor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the inductor module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import inductor


@pytest.mark.unit
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b_xfmr(family_id, environment_active_id):
    """Should return a float value for the base hazard rate on success."""
    _lambda_b = inductor.get_part_count_lambda_b(
        1,
        environment_active_id,
        family_id,
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
                0.0035,
                0.023,
                0.049,
                0.019,
                0.065,
                0.027,
                0.037,
                0.041,
                0.052,
                0.11,
                0.0018,
                0.053,
                0.16,
                2.3,
            ],
            2: [
                0.0071,
                0.046,
                0.097,
                0.038,
                0.13,
                0.055,
                0.073,
                0.081,
                0.10,
                0.22,
                0.035,
                0.11,
                0.31,
                4.7,
            ],
            3: [
                0.023,
                0.16,
                0.35,
                0.13,
                0.45,
                0.21,
                0.27,
                0.35,
                0.45,
                0.82,
                0.011,
                0.37,
                1.2,
                16.0,
            ],
            4: [
                0.028,
                0.18,
                0.39,
                0.15,
                0.52,
                0.22,
                0.29,
                0.33,
                0.42,
                0.88,
                0.015,
                0.42,
                1.2,
                19.0,
            ],
        }[family_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("family_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b_inductor(
    family_id,
    environment_active_id,
):
    """Should return a float value for the base hazard rate on success."""
    _lambda_b = inductor.get_part_count_lambda_b(
        2,
        environment_active_id,
        family_id,
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
                0.0017,
                0.0073,
                0.023,
                0.0091,
                0.031,
                0.011,
                0.015,
                0.016,
                0.022,
                0.052,
                0.00083,
                0.25,
                0.073,
                1.1,
            ],
            2: [
                0.0033,
                0.015,
                0.046,
                0.018,
                0.061,
                0.022,
                0.03,
                0.033,
                0.044,
                0.10,
                0.0017,
                0.05,
                0.15,
                2.2,
            ],
        }[family_id][environment_active_id - 1]
    )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """Should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        inductor.get_part_count_lambda_b(
            20,
            3,
            1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_family():
    """Should raise a KeyError when passed an unknown family ID."""
    with pytest.raises(KeyError):
        inductor.get_part_count_lambda_b(
            2,
            3,
            12,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """Should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        inductor.get_part_count_lambda_b(
            2,
            31,
            1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
@pytest.mark.parametrize("family_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
def test_calculate_part_count_inductor(
    family_id,
    environment_active_id,
    test_attributes_inductor,
):
    """Should return a float value for the base hazard rate on success."""
    test_attributes_inductor["subcategory_id"] = 2
    test_attributes_inductor["family_id"] = family_id
    test_attributes_inductor["environment_active_id"] = environment_active_id
    _lambda_b = inductor.calculate_part_count(**test_attributes_inductor)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
                0.0017,
                0.0073,
                0.023,
                0.0091,
                0.031,
                0.011,
                0.015,
                0.016,
                0.022,
                0.052,
                0.00083,
                0.25,
                0.073,
                1.1,
            ],
            2: [
                0.0033,
                0.015,
                0.046,
                0.018,
                0.061,
                0.022,
                0.03,
                0.033,
                0.044,
                0.10,
                0.0017,
                0.05,
                0.15,
                2.2,
            ],
        }[family_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_part_count_xfmr(
    family_id,
    environment_active_id,
    test_attributes_inductor,
):
    """Should return a float value for the base hazard rate on success."""
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["family_id"] = family_id
    test_attributes_inductor["environment_active_id"] = environment_active_id
    _lambda_b = inductor.calculate_part_count(**test_attributes_inductor)

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: [
                0.0035,
                0.023,
                0.049,
                0.019,
                0.065,
                0.027,
                0.037,
                0.041,
                0.052,
                0.11,
                0.0018,
                0.053,
                0.16,
                2.3,
            ],
            2: [
                0.0071,
                0.046,
                0.097,
                0.038,
                0.13,
                0.055,
                0.073,
                0.081,
                0.10,
                0.22,
                0.035,
                0.11,
                0.31,
                4.7,
            ],
            3: [
                0.023,
                0.16,
                0.35,
                0.13,
                0.45,
                0.21,
                0.27,
                0.35,
                0.45,
                0.82,
                0.011,
                0.37,
                1.2,
                16.0,
            ],
            4: [
                0.028,
                0.18,
                0.39,
                0.15,
                0.52,
                0.22,
                0.29,
                0.33,
                0.42,
                0.88,
                0.015,
                0.42,
                1.2,
                19.0,
            ],
        }[family_id][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "page_number",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_temperature_rise_spec_sheet(page_number):
    """Should return a float value for the temperature_rise on success."""
    _temperature_rise = inductor.get_temperature_rise_spec_sheet(page_number)

    assert isinstance(_temperature_rise, float)
    assert (
        _temperature_rise
        == {
            1: 15.0,
            2: 15.0,
            3: 15.0,
            4: 35.0,
            5: 15.0,
            6: 35.0,
            7: 15.0,
            8: 35.0,
            9: 15.0,
            10: 15.0,
            11: 35.0,
            12: 35.0,
            13: 15.0,
            14: 15.0,
        }[page_number]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_temperature_rise_spec_id(test_attributes_inductor):
    """Should return a float value for the temperature_rise on success."""
    test_attributes_inductor["subcategory_id"] = 2
    test_attributes_inductor["specification_id"] = 2
    test_attributes_inductor["page_number"] = 14

    test_attributes_inductor = inductor.calculate_part_stress(
        **test_attributes_inductor
    )

    assert isinstance(test_attributes_inductor["temperature_rise"], float)
    assert test_attributes_inductor["temperature_rise"] == 15.0


@pytest.mark.unit
def test_get_temperature_rise_no_spec_sheet():
    """Should raise a KeyError when passed an unkown page number."""
    with pytest.raises(KeyError):
        inductor.get_temperature_rise_spec_sheet(22)


@pytest.mark.unit
def test_calculate_temperature_rise_input_power_weight():
    """Should return a float value on success."""
    _temperature_rise = inductor.calculate_temperature_rise_input_power_weight(
        0.387, 0.015
    )

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == pytest.approx(13.93114825)


@pytest.mark.unit
def test_calculate_temperature_rise_input_power_weight_zero_weight():
    """Should raise a ZeroDivisionError when passed a weight=0.0."""
    with pytest.raises(ZeroDivisionError):
        inductor.calculate_temperature_rise_input_power_weight(0.387, 0.0)


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_surface():
    """Should return a float value on success."""
    _temperature_rise = inductor.calculate_temperature_rise_power_loss_surface(
        0.387, 12.5
    )

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == 3.87


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_surface_zero_area():
    """Should raise a ZeroDivisionError when passed an area=0.0."""
    with pytest.raises(ZeroDivisionError):
        inductor.calculate_temperature_rise_power_loss_surface(0.387, 0.0)


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_weight():
    """Should return a float value on success."""
    _temperature_rise = inductor.calculate_temperature_rise_power_loss_weight(
        0.387, 2.5
    )

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == pytest.approx(2.394211958)


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_weight_zero_weight():
    """Should raise a ZeroDivisionError when passed a weight=0.0."""
    with pytest.raises(ZeroDivisionError):
        inductor.calculate_temperature_rise_power_loss_weight(0.387, 0.0)


@pytest.mark.unit
def test_calculate_hot_spot_temperature():
    """Should return a float value on success."""
    _temperature_hot_spot = inductor.calculate_hot_spot_temperature(43.2, 38.7)

    assert isinstance(_temperature_hot_spot, float)
    assert _temperature_hot_spot == pytest.approx(85.77)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b():
    """Should return a float value on success."""
    _lambda_b = inductor.calculate_part_stress_lambda_b(1, 4, 85.77)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(0.00280133)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_subcategory():
    """Should raise an KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        inductor.calculate_part_stress_lambda_b(101, 4, 85.77)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_insulation():
    """Should raise an KeyError when passed an unknown insulation ID."""
    with pytest.raises(KeyError):
        inductor.calculate_part_stress_lambda_b(1, 41, 85.77)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_stress_quality_factor(subcategory_id):
    """Should return a float value for piQ on success."""
    _pi_q = inductor.get_part_stress_quality_factor(subcategory_id, 1, 1)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 1.5, 2: 0.03}[subcategory_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_inductor(test_attributes_inductor):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["subcategory_id"] = 2
    test_attributes_inductor["construction_id"] = 2
    _attributes = inductor.calculate_part_stress(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(0.00046712295)
    assert _attributes["piC"] == 2.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.00014013688)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_surface_area(test_attributes_inductor):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["construction_id"] = 1
    _attributes = inductor.calculate_part_stress(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["lambda_b"] == pytest.approx(0.0026358035)
    assert _attributes["piC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.01976853)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_weight(test_attributes_inductor):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["power_operating"] = 0.387
    test_attributes_inductor["voltage_dc_operating"] = 0.0
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["weight"] = 2.5
    _attributes = inductor.calculate_part_stress(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(2.39421196)
    assert _attributes["lambda_b"] == pytest.approx(0.0024684654)
    assert _attributes["piC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.01851349)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_input_power(test_attributes_inductor):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["power_operating"] = 0.0
    test_attributes_inductor["voltage_dc_operating"] = 3.3
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["weight"] = 2.5
    _attributes = inductor.calculate_part_stress(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(0.0040553804)
    assert _attributes["lambda_b"] == pytest.approx(0.0024148713)
    assert _attributes["piC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.01811153)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_no_temperature_rise(test_attributes_inductor):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["power_operating"] = 0.0
    test_attributes_inductor["voltage_dc_operating"] = 0.0
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["weight"] = 0.0
    _attributes = inductor.calculate_part_stress(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == 0.0
    assert _attributes["lambda_b"] == pytest.approx(0.0024147842)
    assert _attributes["piC"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.01811088)


@pytest.mark.unit
def test_set_default_max_rated_temperature():
    """Should return the default capacitance for the selected subcategory ID."""
    assert inductor._set_default_max_rated_temperature(1) == 130.0
    assert inductor._set_default_max_rated_temperature(2) == 125.0


@pytest.mark.unit
def test_set_default_temperature_rise():
    """Should return the default capacitance for the selected subcategory ID."""
    assert inductor._set_default_temperature_rise(1, 1) == 10.0
    assert inductor._set_default_temperature_rise(1, 3) == 30.0
    assert inductor._set_default_temperature_rise(2, 1) == 10.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_set_default_values(test_attributes_inductor):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_inductor["rated_temperature_max"] = 0.0
    test_attributes_inductor["temperature_rise"] = 0.0
    test_attributes_inductor["subcategory_id"] = 1
    _attributes = inductor.set_default_values(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_temperature_max"] == 130.0
    assert _attributes["temperature_rise"] == 10.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_set_default_values_none_needed(test_attributes_inductor):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_inductor["rated_temperature_max"] = 135.0
    test_attributes_inductor["temperature_rise"] = 5.0
    test_attributes_inductor["subcategory_id"] = 1
    _attributes = inductor.set_default_values(**test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_temperature_max"] == 135.0
    assert _attributes["temperature_rise"] == 5.0
