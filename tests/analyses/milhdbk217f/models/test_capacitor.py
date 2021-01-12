# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_capacitor.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the capacitor MIL-HDBK-217F module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import capacitor

ATTRIBUTES = {
    'hardware_id': 12,
    'subcategory_id': 1,
    'temperature_rated_max': 105.0,
    'temperature_active': 45.0,
    'voltage_ratio': 0.54,
    'capacitance': 0.0000033,
    'construction_id': 1,
    'configuration_id': 1,
    'resistance': 0.05,
    'voltage_dc_operating': 3.3,
    'voltage_ac_operating': 0.04,
    'lambda_b': 0.0,
    'piQ': 1.0,
    'piE': 1.0,
    'piC': 0.0,
    'piCF': 0.0,
    'piCV': 0.0,
    'piSR': 0.0,
    'hazard_rate_active': 0.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
@pytest.mark.parametrize("specification_id", [1, 2])
def test_get_part_count_lambda_b(subcategory_id, environment_active_id,
                                 specification_id):
    """get_part_count_lambda_b_list() should return a list of base hazard rates on success or raise a KeyError when no key exists."""
    _lambda_b = capacitor.get_part_count_lambda_b(
        subcategory_id,
        environment_active_id,
        specification_id=specification_id,
    )

    assert isinstance(_lambda_b, float)

    # Verify a sampling of base hazard rates.


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = capacitor.get_part_count_lambda_b(22, 2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b_list() should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = capacitor.get_part_count_lambda_b(3, 22)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_specification():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = capacitor.get_part_count_lambda_b(1,
                                                      2,
                                                      specification_id=22)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
@pytest.mark.parametrize(
    "ref_temp",
    [65.0, 70.0, 85.0, 105.0, 125.0, 150.0, 170.0, 175.0, 200.0],
)
def test_calculate_part_stress_lambda_b(subcategory_id, ref_temp):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard rate on success."""
    _base_hr = capacitor.calculate_part_stress_lambda_b(
        subcategory_id,
        ref_temp,
        45.0,
        0.65,
    )

    assert isinstance(_base_hr, float)

    # Check good calculation for a sample of combinations.
    if subcategory_id == 1 and ref_temp == 105.0:
        assert _base_hr == pytest.approx(0.06621194)
    if subcategory_id == 10 and ref_temp == 175.0:
        assert _base_hr == pytest.approx(0.0068154785)
    if subcategory_id == 15 and ref_temp == 65.0:
        assert _base_hr == pytest.approx(0.12880427)
    if subcategory_id == 19 and ref_temp == 200.0:
        assert _base_hr == pytest.approx(0.65589138)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_unknown_subcategory_id():
    """calculate_part_stress_lambda_b() should raise a KeyError when an unknown subcategory ID is passed."""
    with pytest.raises(KeyError):
        _base_hr = capacitor.calculate_part_stress_lambda_b(
            22,
            105.0,
            45.0,
            0.65,
        )


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_b_unknown_ref_temp():
    """calculate_part_stress_lambda_b() should use the nearest reference temperature when an unknown reference temperature is passed."""
    _base_hr = capacitor.calculate_part_stress_lambda_b(
        1,
        100.0,
        45.0,
        0.65,
    )

    assert isinstance(_base_hr, float)
    assert _base_hr == pytest.approx(0.06621194)

@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)
def test_calculate_capacitance_factor(subcategory_id):
    """calculate_part_stress_lambda_b() should return a float value for piCV on success."""
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
        19: 1.0
    }
    _pi_cv = capacitor.calculate_capacitance_factor(subcategory_id, 0.0000033)

    assert isinstance(_pi_cv, float)
    assert _pi_cv == pytest.approx(_results[subcategory_id])


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_capacitance_factor_unknown_subcategory_id():
    """calculate_capacitance_factor() should raise a KeyError when an unknown subcategory ID is passed."""
    with pytest.raises(KeyError):
        _pi_cv = capacitor.calculate_capacitance_factor(200, 0.0000033)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("resistance", [1.0, 2.0, 3.0, 5.0, 7.0, 9.0])
def test_calculate_series_resistance_factor(resistance):
    """calculate_series_resistance_factor() should return a float value for piSR on success and an empty error message."""
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
@pytest.mark.calculation
def test_calculate_series_resistance_factor_zero_voltage():
    """calculate_series_resistance_factor() should raise a ZeroDivisionError passed zreo voltage."""
    with pytest.raises(ZeroDivisionError):
        _pi_sr, = capacitor.calculate_series_resistance_factor(
            1.0,
            0.0,
            0.0,
        )


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_series_resistance_factor_string_input():
    """calculate_series_resistance_factor() should raise a TypeError if passed a string input."""
    with pytest.raises(TypeError):
        _pi_sr, = capacitor.calculate_series_resistance_factor(
            1.0,
            '10.0',
            0.1,
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("configuration_id", [1, 2])
def test_get_configuration_factor(configuration_id):
    """get_configuration_factor() should return a float value for piCF on success."""
    _results = {1: 0.1, 2: 1.0}
    _pi_cf = capacitor.get_configuration_factor(configuration_id)

    assert isinstance(_pi_cf, float)
    assert _pi_cf == _results[configuration_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_configuration_factor_unknown_configuration():
    """get_configuration_factor() should raise a KeyError when passed an unknown configuration ID."""
    with pytest.raises(KeyError):
        _pi_cf = capacitor.get_configuration_factor(12)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("construction_id", [1, 2, 3, 4, 5])
def test_get_construction_factor(construction_id):
    """get_construction_factor() should return a float value for piC on success."""
    _results = {1: 0.3, 2: 1.0, 3: 2.0, 4: 2.5, 5: 3.0}
    _pi_c = capacitor.get_construction_factor(construction_id)

    assert isinstance(_pi_c, float)
    assert _pi_c == _results[construction_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_construction_factor_unknown_construction():
    """get_construction_factor() should raise a KeyError when passed an unknown construction ID."""
    with pytest.raises(KeyError):
        _pi_c = capacitor.get_construction_factor(12)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 12, 13, 19])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return a dict of updated attributes and an empty error message on success."""
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = capacitor.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == pytest.approx(0.029446888)
        assert _attributes['piCV'] == pytest.approx(0.36177626)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.010653185)
    elif subcategory_id == 12:
        assert _attributes['lambda_b'] == pytest.approx(0.022463773)
        assert _attributes['piCV'] == pytest.approx(0.2198982)
        assert _attributes['piSR'] == 0.33
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0016301152)
    elif subcategory_id == 13:
        assert _attributes['lambda_b'] == pytest.approx(0.0098840599)
        assert _attributes['piC'] == 0.3
        assert _attributes['piCV'] == pytest.approx(0.3564805)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0010570424)
    elif subcategory_id == 19:
        assert _attributes['lambda_b'] == pytest.approx(0.48854794)
        assert _attributes['piCF'] == 0.1
        assert _attributes['piCV'] == 1.0
        assert _attributes['hazard_rate_active'] == pytest.approx(0.048854794)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_missing_attribute_key():
    """calculate_part_stress() should return a dict of updated attributes and an empty error message on success."""
    ATTRIBUTES.pop('voltage_ratio')
    with pytest.raises(KeyError):
        _attributes = capacitor.calculate_part_stress(**ATTRIBUTES)
