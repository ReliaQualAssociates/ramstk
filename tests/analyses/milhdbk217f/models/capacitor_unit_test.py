# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.capacitor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor MIL-HDBK-217F module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import capacitor


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
def test_set_default_capacitance(subcategory_id):
    """Should return the default capacitance for the selected subcategory ID."""
    _capacitance = capacitor._set_default_capacitance(subcategory_id, 2)

    assert (
        _capacitance
        == {
            1: 0.15e-6,
            2: 0.061e-6,
            3: 0.033e-6,
            4: 0.14e-6,
            5: 0.33e-6,
            6: 0.14e-6,
            7: 300e-12,
            8: 160e-12,
            9: 30e-12,
            10: 3300e-12,
            11: 81e-12,
            12: 1e-6,
            13: 20e-6,
            14: 1700e-6,
            15: 1600e-6,
            16: 0.0,
            17: 0.0,
            18: 0.0,
            19: 0.0,
        }[subcategory_id]
    )


@pytest.mark.unit
def test_set_default_capacitance_with_style():
    assert capacitor._set_default_capacitance(3, 1) == 2.7e-08  # First style option
    assert capacitor._set_default_capacitance(3, 2) == 3.3e-08  # Second style option


@pytest.mark.unit
def test_set_default_capacitance_unknown_subcategory():
    """Test _set_default_capacitance() should return 1.0 for unknown subcategory IDs."""
    assert capacitor._set_default_capacitance(100, 2) == 1.0


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [10, 14, 15, 16])
def test_set_default_picv(subcategory_id):
    """Should return the default piCV for the selected subcategory ID."""
    _pi_cv = capacitor._set_default_picv(subcategory_id)

    assert _pi_cv == {10: 1.0, 14: 1.3, 15: 1.3, 16: 0.0}[subcategory_id]


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
def test_set_default_rated_temperature(subcategory_id):
    """Should return the default capacitance for the selected subcategory ID."""
    _temp_rated = capacitor._set_default_rated_temperature(subcategory_id, 2)

    assert (
        _temp_rated
        == {
            1: 85.0,
            2: 125.0,
            3: 125.0,
            4: 125.0,
            5: 125.0,
            6: 125.0,
            7: 125.0,
            8: 125.0,
            9: 125.0,
            10: 125.0,
            11: 125.0,
            12: 125.0,
            13: 125.0,
            14: 125.0,
            15: 85.0,
            16: 85.0,
            17: 125.0,
            18: 85.0,
            19: 85.0,
        }[subcategory_id]
    )


@pytest.mark.unit
def test_set_default_rated_temperature_with_style():
    assert capacitor._set_default_rated_temperature(1, 1) == 125.0  # First style
    assert capacitor._set_default_rated_temperature(1, 2) == 85.0  # Second style


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_capacitor")
def test_set_default_values(test_attributes_capacitor):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_capacitor["capacitance"] = 0.0
    test_attributes_capacitor["piCV"] = -1.0
    test_attributes_capacitor["style_id"] = 1
    test_attributes_capacitor["subcategory_id"] = 3
    test_attributes_capacitor["temperature_rated_max"] = 0.0
    test_attributes_capacitor["voltage_ratio"] = -2.5
    _attributes = capacitor.set_default_values(test_attributes_capacitor)

    assert isinstance(_attributes, dict)
    assert _attributes["capacitance"] == pytest.approx(0.027e-6)
    assert _attributes["piCV"] == pytest.approx(1.0)
    assert _attributes["temperature_rated_max"] == pytest.approx(125.0)
    assert _attributes["voltage_ratio"] == pytest.approx(0.5)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_capacitor")
def test_set_default_values_none_needed(test_attributes_capacitor):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_capacitor["capacitance"] = 0.047e-6
    test_attributes_capacitor["piCV"] = 1.3
    test_attributes_capacitor["style_id"] = 1
    test_attributes_capacitor["subcategory_id"] = 3
    test_attributes_capacitor["temperature_rated_max"] = 85.0
    test_attributes_capacitor["voltage_ratio"] = 0.35
    _attributes = capacitor.set_default_values(test_attributes_capacitor)

    assert isinstance(_attributes, dict)
    assert _attributes["capacitance"] == pytest.approx(0.047e-6)
    assert _attributes["piCV"] == pytest.approx(1.3)
    assert _attributes["temperature_rated_max"] == pytest.approx(85.0)
    assert _attributes["voltage_ratio"] == pytest.approx(0.35)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.parametrize(
    "environment_active_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.parametrize("specification_id", [1, 2])
def test_get_part_count_lambda_b(
    subcategory_id,
    environment_active_id,
    specification_id,
    test_attributes_capacitor,
):
    """get_part_count_lambda_b_list() should return a list of base hazard rates on
    success or raise a KeyError when no key exists."""
    test_attributes_capacitor["environment_active_id"] = environment_active_id
    test_attributes_capacitor["specification_id"] = specification_id
    test_attributes_capacitor["subcategory_id"] = subcategory_id

    _lambda_b = capacitor.get_part_count_lambda_b(test_attributes_capacitor)

    assert isinstance(_lambda_b, float)
    if environment_active_id == 14 and specification_id == 2:
        assert _lambda_b == pytest.approx(
            {
                1: 2.5,
                2: 2.7,
                3: 1.1,
                4: 1.5,
                5: 2.5,
                6: 1.2,
                7: 0.45,
                8: 11.0,
                9: 0.29,
                10: 2.3,
                11: 0.68,
                12: 1.0,
                13: 4.0,
                14: 21.0,
                15: 28.0,
                16: 85.0,
                17: 37.0,
                18: 100.0,
                19: 0.0,
            }[subcategory_id]
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory(test_attributes_capacitor):
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown
    subcategory ID."""
    test_attributes_capacitor["environment_active_id"] = 2
    test_attributes_capacitor["subcategory_id"] = 22
    with pytest.raises(KeyError):
        capacitor.get_part_count_lambda_b(test_attributes_capacitor)


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment(test_attributes_capacitor):
    """get_part_count_lambda_b_list() should raise an IndexError when passed an unknown
    active environment ID."""
    test_attributes_capacitor["environment_active_id"] = 22
    test_attributes_capacitor["specification_id"] = 1
    test_attributes_capacitor["subcategory_id"] = 2
    with pytest.raises(IndexError):
        capacitor.get_part_count_lambda_b(test_attributes_capacitor)


@pytest.mark.unit
def test_get_part_count_lambda_b_no_specification(test_attributes_capacitor):
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type
    ID."""
    test_attributes_capacitor["environment_active_id"] = 2
    test_attributes_capacitor["subcategory_id"] = 1
    test_attributes_capacitor["specification_id"] = 22

    with pytest.raises(KeyError):
        capacitor.get_part_count_lambda_b(test_attributes_capacitor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "quality_id",
    [1, 2, 3, 4, 5, 6, 7],
)
def test_get_part_count_pi_q(quality_id, test_attributes_capacitor):
    test_attributes_capacitor["quality_id"] = quality_id
    _pi_q = capacitor.get_part_count_pi_q(test_attributes_capacitor)

    assert (
        _pi_q
        == {1: 0.030, 2: 0.10, 3: 0.30, 4: 1.0, 5: 3.0, 6: 3.0, 7: 10.0}[quality_id]
    )


@pytest.mark.unit
def test_get_part_count_pi_q_unknown_id(test_attributes_capacitor):
    test_attributes_capacitor["quality_id"] = 22
    with pytest.raises(IndexError):
        capacitor.get_part_count_pi_q(test_attributes_capacitor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.parametrize(
    "ref_temp",
    [65.0, 70.0, 85.0, 105.0, 125.0, 150.0, 170.0, 175.0, 200.0],
)
def test_calculate_part_stress_lambda_b(
    subcategory_id, ref_temp, test_attributes_capacitor
):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard
    rate on success."""
    test_attributes_capacitor["temperature_active"] = 45.0
    test_attributes_capacitor["voltage_ratio"] = 0.65
    test_attributes_capacitor["ref_temp"] = ref_temp
    test_attributes_capacitor["subcategory_id"] = subcategory_id

    _base_hr = capacitor.calculate_part_stress_lambda_b(test_attributes_capacitor)

    assert isinstance(_base_hr, float)

    # Check good calculation for a sample of combinations.
    if subcategory_id == 1 and ref_temp == 105.0:
        assert _base_hr == pytest.approx(0.06621194)
    if subcategory_id == 10 and ref_temp == 175.0:
        assert _base_hr == pytest.approx(0.007772911)
    if subcategory_id == 15 and ref_temp == 65.0:
        assert _base_hr == pytest.approx(0.03244638)
    if subcategory_id == 19 and ref_temp == 200.0:
        assert _base_hr == pytest.approx(0.8410533)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_unknown_subcategory_id(
    test_attributes_capacitor,
):
    """calculate_part_stress_lambda_b() should raise a KeyError when an unknown
    subcategory ID is passed."""
    test_attributes_capacitor["subcategory_id"] = 22
    test_attributes_capacitor["temperature_rated_max"] = 105.0
    test_attributes_capacitor["temperature_active"] = 45.0
    test_attributes_capacitor["voltage_ratio"] = 0.65

    with pytest.raises(KeyError):
        capacitor.calculate_part_stress_lambda_b(test_attributes_capacitor)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_unknown_ref_temp(test_attributes_capacitor):
    """calculate_part_stress_lambda_b() should use the nearest reference temperature
    when an unknown reference temperature is passed."""
    test_attributes_capacitor["subcategory_id"] = 1
    test_attributes_capacitor["ref_temp"] = 125.0
    test_attributes_capacitor["temperature_rated_max"] = 100.0
    test_attributes_capacitor["temperature_active"] = 45.0
    test_attributes_capacitor["voltage_ratio"] = 0.65

    _base_hr = capacitor.calculate_part_stress_lambda_b(test_attributes_capacitor)

    assert isinstance(_base_hr, float)
    assert _base_hr == pytest.approx(0.09961831)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_pi_e(environment_active_id, test_attributes_capacitor):
    test_attributes_capacitor["environment_active_id"] = environment_active_id
    _pi_e = capacitor.get_environment_factor(test_attributes_capacitor)

    assert (
        _pi_e
        == {
            1: 1.0,
            2: 6.0,
            3: 9.0,
            4: 9.0,
            5: 19.0,
            6: 13.0,
            7: 29.0,
            8: 20.0,
            9: 43.0,
            10: 24.0,
            11: 0.5,
            12: 14.0,
            13: 32.0,
            14: 320.0,
        }[environment_active_id]
    )


@pytest.mark.unit
def test_get_pi_e_unknown_id(test_attributes_capacitor):
    test_attributes_capacitor["environment_active_id"] = 22
    with pytest.raises(IndexError):
        capacitor.get_environment_factor(test_attributes_capacitor)


@pytest.mark.unit
def test_get_part_stress_pi_q(test_attributes_capacitor):
    test_attributes_capacitor["subcategory_id"] = 1
    test_attributes_capacitor["quality_id"] = 1
    assert capacitor.get_part_stress_pi_q(test_attributes_capacitor) == 3.0

    test_attributes_capacitor["quality_id"] = 2
    assert capacitor.get_part_stress_pi_q(test_attributes_capacitor) == 7.0

    test_attributes_capacitor["subcategory_id"] = 12
    test_attributes_capacitor["quality_id"] = 1
    assert capacitor.get_part_stress_pi_q(test_attributes_capacitor) == 0.001

    test_attributes_capacitor["quality_id"] = 4
    assert capacitor.get_part_stress_pi_q(test_attributes_capacitor) == 0.03


@pytest.mark.unit
def test_get_part_stress_pi_q_unknown_subcategory_id(test_attributes_capacitor):
    test_attributes_capacitor["subcategory_id"] = 22
    with pytest.raises(KeyError):
        capacitor.get_part_stress_pi_q(test_attributes_capacitor)


@pytest.mark.unit
def test_get_part_stress_pi_q_unknown_quality_id(test_attributes_capacitor):
    test_attributes_capacitor["quality_id"] = 22
    with pytest.raises(IndexError):
        capacitor.get_part_stress_pi_q(test_attributes_capacitor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
def test_calculate_capacitance_factor(subcategory_id):
    """calculate_part_stress_lambda_b() should return a float value for piCV on
    success."""
    _results = {
        1: 0.36177626,
        2: 0.30785748,
        3: 0.31011787,
        4: 0.37573749,
        5: 0.37624122,
        6: 0.37573749,
        7: 0.076878423,
        8: 0.017006694,
        9: 0.10592138,
        10: 0.10228699,
        11: 0.12973994,
        12: 0.2198982,
        13: 0.35648050,
        14: 0.035059961,
        15: 0.029175794,
        16: 1.0,
        17: 1.0,
        18: 1.0,
        19: 1.0,
    }
    _pi_cv = capacitor.calculate_capacitance_factor(subcategory_id, 0.0000033)

    assert isinstance(_pi_cv, float)
    assert _pi_cv == pytest.approx(_results[subcategory_id])


@pytest.mark.unit
@pytest.mark.parametrize(
    "capacitance",
    [0.0, 1e-12, 1e-2],  # Test boundary capacitance values
)
def test_calculate_capacitance_factor_boundary_values(capacitance):
    """Test calculate_capacitance_factor() for boundary capacitance values."""
    _pi_cv = capacitor.calculate_capacitance_factor(1, capacitance)
    assert isinstance(_pi_cv, float)
    assert _pi_cv >= 0


@pytest.mark.unit
def test_calculate_capacitance_factor_unknown_subcategory_id():
    """calculate_capacitance_factor() should raise a KeyError when an unknown
    subcategory ID is passed."""
    with pytest.raises(KeyError):
        capacitor.calculate_capacitance_factor(200, 0.0000033)


@pytest.mark.unit
@pytest.mark.parametrize("resistance", [1.0, 2.0, 3.0, 5.0, 7.0, 9.0])
def test_calculate_series_resistance_factor(resistance):
    """calculate_series_resistance_factor() should return a float value for piSR on
    success and an empty error message."""
    _results = {
        1.0: 0.33,
        2.0: 0.27,
        3.0: 0.2,
        5.0: 0.13,
        7.0: 0.1,
        9.0: 0.066,
    }
    _pi_sr = capacitor.calculate_series_resistance_factor(
        resistance,
        10.0,
        0.1,
    )

    assert isinstance(_pi_sr, float)
    assert _pi_sr == _results[resistance]


@pytest.mark.unit
def test_calculate_series_resistance_factor_zero_voltage():
    """calculate_series_resistance_factor() should raise a ZeroDivisionError passed zreo
    voltage."""
    with pytest.raises(ZeroDivisionError):
        capacitor.calculate_series_resistance_factor(
            1.0,
            0.0,
            0.0,
        )


@pytest.mark.unit
def test_calculate_series_resistance_factor_string_input():
    """calculate_series_resistance_factor() should raise a TypeError if passed a string
    input."""
    with pytest.raises(TypeError):
        capacitor.calculate_series_resistance_factor(
            1.0,
            "10.0",
            0.1,
        )


@pytest.mark.unit
@pytest.mark.parametrize("resistance, voltage", [(1e-6, 10.0), (1e6, 1.0)])
def test_calculate_series_resistance_factor_extremes(resistance, voltage):
    """Test calculate_series_resistance_factor() with extreme resistance values."""
    _pi_sr = capacitor.calculate_series_resistance_factor(resistance, voltage, 0.1)

    assert isinstance(_pi_sr, float)
    assert _pi_sr > 0


@pytest.mark.unit
@pytest.mark.parametrize("construction_id", [1, 2, 3, 4, 5])
def test_get_construction_factor(construction_id):
    """get_construction_factor() should return a float value for piC on success."""
    _results = {1: 0.3, 2: 1.0, 3: 2.0, 4: 2.5, 5: 3.0}
    _pi_c = capacitor.get_construction_factor(construction_id)

    assert isinstance(_pi_c, float)
    assert _pi_c == _results[construction_id]


@pytest.mark.unit
def test_get_construction_factor_unknown_construction():
    """get_construction_factor() should return 1.0 when passed an unknown construction
    ID."""
    assert capacitor.get_construction_factor(12) == 1.0


@pytest.mark.unit
@pytest.mark.parametrize("configuration_id", [1, 2])
def test_get_configuration_factor(configuration_id):
    """get_configuration_factor() should return a float value for piCF on success."""
    _results = {1: 0.1, 2: 1.0}
    _pi_cf = capacitor.get_configuration_factor(configuration_id)

    assert isinstance(_pi_cf, float)
    assert _pi_cf == _results[configuration_id]


@pytest.mark.unit
def test_get_configuration_factor_unknown_configuration():
    """get_configuration_factor() should return 1.0 when passed an unknown configuration
    ID."""
    assert capacitor.get_configuration_factor(12) == 1.0


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 12, 13, 19])
@pytest.mark.usefixtures("test_attributes_capacitor")
def test_calculate_part_stress(subcategory_id, test_attributes_capacitor):
    """calculate_part_stress() should return a dict of updated attributes and an empty
    error message on success."""
    test_attributes_capacitor["environment_active_id"] = 1
    test_attributes_capacitor["ref_temp"] = 125.0
    test_attributes_capacitor["specification_id"] = 1
    test_attributes_capacitor["temperature_rated_max"] = 100.0
    test_attributes_capacitor["temperature_active"] = 45.0
    test_attributes_capacitor["voltage_ratio"] = 0.65
    test_attributes_capacitor["subcategory_id"] = subcategory_id
    test_attributes_capacitor["hazard_rate_active"] = 1.855154067
    _attributes = capacitor.calculate_part_stress(test_attributes_capacitor)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["piCV"] == pytest.approx(0.36177626)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.6711507)
    elif subcategory_id == 12:
        assert _attributes["piCV"] == pytest.approx(0.2198982)
        assert _attributes["piSR"] == pytest.approx(0.33)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1346219)
    elif subcategory_id == 13:
        assert _attributes["piC"] == pytest.approx(0.3)
        assert _attributes["piCV"] == pytest.approx(0.3564805)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1983979)
    elif subcategory_id == 19:
        assert _attributes["piCF"] == pytest.approx(0.1)
        assert _attributes["piCV"] == pytest.approx(1.0)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1855154)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_capacitor")
def test_calculate_part_stress_missing_attribute_key(test_attributes_capacitor):
    """calculate_part_stress() should raise a KeyError when a required attribute is
    missing."""
    test_attributes_capacitor.pop("capacitance")
    with pytest.raises(
        KeyError, match=r"Missing " r"required attribute: 'capacitance'"
    ):
        capacitor.calculate_part_stress(test_attributes_capacitor)
