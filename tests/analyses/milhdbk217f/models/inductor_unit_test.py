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
def test_set_default_rated_temperature():
    """Should return the default capacitance for the selected subcategory ID."""
    assert inductor._set_default_rated_temperature(1) == 130.0
    assert inductor._set_default_rated_temperature(2) == 125.0


@pytest.mark.unit
def test_set_default_temperature_rise():
    """Should return the default capacitance for the selected subcategory ID."""
    assert inductor._set_default_temperature_rise(1, 1) == 10.0
    assert inductor._set_default_temperature_rise(1, 3) == 30.0
    assert inductor._set_default_temperature_rise(2, 1) == 10.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_set_default_values(
    test_attributes_inductor,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_inductor["rated_temperature_max"] = 0.0
    test_attributes_inductor["temperature_rise"] = 0.0
    test_attributes_inductor["subcategory_id"] = 1
    _attributes = inductor.set_default_values(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_temperature_max"] == 130.0
    assert _attributes["temperature_rise"] == 10.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_set_default_values_none_needed(
    test_attributes_inductor,
):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_inductor["rated_temperature_max"] = 135.0
    test_attributes_inductor["temperature_rise"] = 5.0
    test_attributes_inductor["subcategory_id"] = 1
    _attributes = inductor.set_default_values(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["rated_temperature_max"] == 135.0
    assert _attributes["temperature_rise"] == 5.0


@pytest.mark.unit
@pytest.mark.parametrize("family_id", [1, 2, 3, 4])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_lambda_b_xfmr(
    family_id,
    environment_active_id,
    test_attributes_inductor,
):
    """Returns a float value for the base hazard rate on success."""
    test_attributes_inductor["environment_active_id"] = environment_active_id
    test_attributes_inductor["family_id"] = family_id
    test_attributes_inductor["subcategory_id"] = 1
    _lambda_b = inductor.get_part_count_lambda_b(test_attributes_inductor)

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
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_lambda_b_inductor(
    family_id,
    environment_active_id,
    test_attributes_inductor,
):
    """Should return a float value for the base hazard rate on success."""
    test_attributes_inductor["environment_active_id"] = environment_active_id
    test_attributes_inductor["family_id"] = family_id
    test_attributes_inductor["subcategory_id"] = 2
    _lambda_b = inductor.get_part_count_lambda_b(test_attributes_inductor)

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
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_inductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_inductor["subcategory_id"] = 3
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid inductive device family ID 1 or "
        r"subcategory ID 3.",
    ):
        inductor.get_part_count_lambda_b(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_lambda_b_invalid_family_id(
    test_attributes_inductor,
):
    """Should raise a KeyError when passed an unknown family ID."""
    test_attributes_inductor["environment_active_id"] = 3
    test_attributes_inductor["family_id"] = 12
    test_attributes_inductor["subcategory_id"] = 2
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid inductive device family ID 12 or "
        r"subcategory ID 2.",
    ):
        inductor.get_part_count_lambda_b(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_inductor,
):
    """Should raise an IndexError when passed an unknown active environment ID."""
    test_attributes_inductor["environment_active_id"] = 31
    test_attributes_inductor["family_id"] = 1
    test_attributes_inductor["subcategory_id"] = 2
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid inductive device environment ID 31.",
    ):
        inductor.get_part_count_lambda_b(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3])
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_quality_factor(
    quality_id,
    test_attributes_inductor,
):
    """Returns the quality factor (piQ) for the passed quality ID."""
    test_attributes_inductor["quality_id"] = quality_id
    _pi_q = inductor.get_part_count_quality_factor(test_attributes_inductor)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 0.25, 2: 1.0, 3: 10.0}[quality_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_inductor,
):
    """Returns the quality factor (piQ) for the passed quality ID."""
    test_attributes_inductor["quality_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid inductive device quality ID 22.",
    ):
        inductor.get_part_count_quality_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "insulation_id",
    [1, 2, 3, 4],
)
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_lambda_b(
    insulation_id,
    test_attributes_inductor,
):
    """Returns a float value on success."""
    test_attributes_inductor["insulation_id"] = insulation_id
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["temperature_hot_spot"] = 98.6
    _lambda_b = inductor.calculate_part_stress_lambda_b(test_attributes_inductor)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == pytest.approx(
        {
            1: 1.4366534,
            2: 0.01691947,
            3: 0.00595802,
            4: 0.003228283,
        }[insulation_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_lambda_b_invalid_subcategory_id(
    test_attributes_inductor,
):
    """Should raise an KeyError when passed an invalid subcategory ID."""
    test_attributes_inductor["subcategory_id"] = 101
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid inductive device subcategory "
        r"ID 101 or insulation ID 3.",
    ):
        inductor.calculate_part_stress_lambda_b(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_lambda_b_invalid_insulation_id(
    test_attributes_inductor,
):
    """Raises an KeyError when passed an invalid insulation ID."""
    test_attributes_inductor["insulation_id"] = 41
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid inductive device subcategory "
        r"ID 1 or insulation ID 41.",
    ):
        inductor.calculate_part_stress_lambda_b(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_environment_factor(
    environment_id,
    subcategory_id,
    test_attributes_inductor,
):
    """Returns the environment factor for the passed environment ID."""
    test_attributes_inductor["environment_active_id"] = environment_id
    test_attributes_inductor["subcategory_id"] = subcategory_id
    _pi_e = inductor.get_environment_factor(test_attributes_inductor)

    assert isinstance(_pi_e, float)
    if subcategory_id == 1:
        assert (
            _pi_e
            == {
                1: 1.0,
                2: 6.0,
                3: 12.0,
                4: 5.0,
                5: 16.0,
                6: 6.0,
                7: 8.0,
                8: 7.0,
                9: 9.0,
                10: 24.0,
                11: 0.5,
                12: 13.0,
                13: 34.0,
                14: 610.0,
            }[environment_id]
        )
    elif subcategory_id == 2:
        assert (
            _pi_e
            == {
                1: 1.0,
                2: 4.0,
                3: 12.0,
                4: 5.0,
                5: 16.0,
                6: 5.0,
                7: 7.0,
                8: 6.0,
                9: 8.0,
                10: 24.0,
                11: 0.5,
                12: 13.0,
                13: 34.0,
                14: 610.0,
            }[environment_id]
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_inductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_inductor["subcategory_id"] = 3
    with pytest.raises(
        KeyError,
        match=r"get_environment_factor: Invalid inductive device subcategory ID 3.",
    ):
        inductor.get_environment_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_inductor,
):
    """Raises am IndexError when passed an invalid environment ID."""
    test_attributes_inductor["environment_active_id"] = 32
    test_attributes_inductor["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid inductive device environment ID 32.",
    ):
        inductor.get_environment_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_stress_quality_factor(
    subcategory_id,
    test_attributes_inductor,
):
    """Should return a float value for piQ on success."""
    test_attributes_inductor["subcategory_id"] = subcategory_id
    _pi_q = inductor.get_part_stress_quality_factor(test_attributes_inductor)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 1.5, 2: 0.03}[subcategory_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_stress_quality_factor_invalid_subcategory_id(
    test_attributes_inductor,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_inductor["subcategory_id"] = 4
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid inductive device family ID 1 "
        r"or subcategory ID 4.",
    ):
        inductor.get_part_stress_quality_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_stress_quality_factor_invalid_family_id(
    test_attributes_inductor,
):
    """Raises a KeyError when passed an invalid family ID."""
    test_attributes_inductor["family_id"] = 14
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid inductive device family ID 14 "
        r"or subcategory ID 1.",
    ):
        inductor.get_part_stress_quality_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_inductor,
):
    """Raises am IndexError when passed an invalid quality ID."""
    test_attributes_inductor["quality_id"] = 14
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid inductive device quality "
        r"ID 14.",
    ):
        inductor.get_part_stress_quality_factor(test_attributes_inductor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "page_number",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_temperature_rise_spec_sheet(
    page_number,
):
    """Returns a float value for the temperature rise on success."""
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
def test_get_temperature_rise_spec_sheet_invalid_page_number():
    """Raises a KeyError when passed an invalid page number."""
    with pytest.raises(
        KeyError,
        match=r"get_temperature_rise_spec_sheet: Invalid inductive device page "
        r"number 22.",
    ):
        inductor.get_temperature_rise_spec_sheet(22)


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_surface():
    """Returns a float value on success."""
    _temperature_rise = inductor.calculate_temperature_rise_power_loss_surface(
        0.387, 12.5
    )

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == 3.87


@pytest.mark.unit
def test_calculate_temperature_rise_power_loss_surface_zero_area():
    """Raises a ZeroDivisionError when passed and area = 0.0."""
    with pytest.raises(
        ZeroDivisionError,
        match=r"calculate_temperature_rise_power_loss_surface: Inductive device area "
        r"must not be zero.",
    ):
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
    with pytest.raises(
        ZeroDivisionError,
        match=r"calculate_temperature_rise_power_loss_weight: Inductive device weight "
        r"must not be zero.",
    ):
        inductor.calculate_temperature_rise_power_loss_weight(0.387, 0.0)


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
    with pytest.raises(
        ZeroDivisionError,
        match=r"calculate_temperature_rise_input_power_weight: Inductive device "
        r"weight must not be zero.",
    ):
        inductor.calculate_temperature_rise_input_power_weight(0.387, 0.0)


@pytest.mark.unit
def test_calculate_hot_spot_temperature():
    """Should return a float value on success."""
    _temperature_hot_spot = inductor.calculate_hot_spot_temperature(43.2, 38.7)

    assert isinstance(_temperature_hot_spot, float)
    assert _temperature_hot_spot == pytest.approx(85.77)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_inductor(
    test_attributes_inductor,
):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["construction_id"] = 2
    test_attributes_inductor["hazard_rate_active"] = 0.000467123
    test_attributes_inductor["piQ"] = 0.3
    test_attributes_inductor["subcategory_id"] = 2
    _attributes = inductor.calculate_part_stress(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["piC"] == 2.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.001401369)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_surface_area(
    test_attributes_inductor,
):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["hazard_rate_active"] = 0.000467123
    test_attributes_inductor["piQ"] = 0.3
    test_attributes_inductor["subcategory_id"] = 1
    _attributes = inductor.calculate_part_stress(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["piC"] == 1.0
    assert _attributes["lambda_b"] == pytest.approx(0.002635803)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.003953705)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_weight(
    test_attributes_inductor,
):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["hazard_rate_active"] = 0.000467123
    test_attributes_inductor["piQ"] = 0.3
    test_attributes_inductor["power_operating"] = 0.387
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["voltage_dc_operating"] = 0.0
    test_attributes_inductor["weight"] = 2.5
    _attributes = inductor.calculate_part_stress(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(2.39421196)
    assert _attributes["piC"] == 1.0
    assert _attributes["lambda_b"] == pytest.approx(0.002468465)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.003702698)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_with_input_power(
    test_attributes_inductor,
):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["hazard_rate_active"] = 0.000467123
    test_attributes_inductor["piQ"] = 0.3
    test_attributes_inductor["power_operating"] = 0.0
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["voltage_dc_operating"] = 3.3
    test_attributes_inductor["weight"] = 2.5
    _attributes = inductor.calculate_part_stress(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(0.0040553804)
    assert _attributes["piC"] == 1.0
    assert _attributes["lambda_b"] == pytest.approx(0.002414871)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.003622307)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_inductor")
def test_calculate_part_stress_xfmr_no_temperature_rise(
    test_attributes_inductor,
):
    """Should return a dictionary of updated values on success."""
    test_attributes_inductor["area"] = 0.0
    test_attributes_inductor["construction_id"] = 1
    test_attributes_inductor["hazard_rate_active"] = 0.000467123
    test_attributes_inductor["piQ"] = 0.3
    test_attributes_inductor["power_operating"] = 0.0
    test_attributes_inductor["subcategory_id"] = 1
    test_attributes_inductor["voltage_dc_operating"] = 0.0
    test_attributes_inductor["weight"] = 0.0
    _attributes = inductor.calculate_part_stress(test_attributes_inductor)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == 0.0
    assert _attributes["piC"] == 1.0
    assert _attributes["lambda_b"] == pytest.approx(0.002414784)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.003622176)
