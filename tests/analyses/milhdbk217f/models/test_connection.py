# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_connection.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the connection module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import Connection

ATTRIBUTES = {
    'category_id': 8,
    'subcategory_id': 1,
    'environment_active_id': 2,
    'type_id': 2,
    'specification_id': 1,
    'n_circuit_planes': 3,
    'contact_gauge': 20,
    'current_operating': 0.005,
    'n_active_pins': 15,
    'n_cycles': 0.1,
    'temperature_active': 40.0,
    'insert_id': 2,
    'n_wave_soldered': 45,
    'n_hand_soldered': 4,
    'lambda_b': 0.0,
    'piQ': 1.0,
    'piE': 1.0,
    'piC': 0.0,
    'piK': 0.0,
    'piP': 0.0,
    'hazard_rate_active': 0.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("type_id", [1, 2])
def test_get_part_count_lambda_b(subcategory_id, environment_active_id,
                                 type_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rates on success."""
    _lambda_b = Connection.get_part_count_lambda_b(
        subcategory_id,
        environment_active_id,
        type_id=type_id,
    )
    assert isinstance(_lambda_b, float)

    # Verify a sampling of base hazard rates.


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = Connection.get_part_count_lambda_b(12, 2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b_list() should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = Connection.get_part_count_lambda_b(3, 22)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = Connection.get_part_count_lambda_b(1, 2, type_id=22)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a list of base hazard rates on success."""
    _lst_lambda_b = Connection.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lst_lambda_b, float)
    assert _lst_lambda_b == 0.015


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("contact_gauge", [12, 16, 20, 22, 26])
def test_calculate_insert_temperature(contact_gauge):
    """calculate_insert_temperature() should return a float value for the temperature rise on success."""
    _dic_factors = {12: 0.1, 16: 0.274, 20: 0.64, 22: 0.989, 26: 2.1}
    _temperature_rise = Connection.calculate_insert_temperature(
        contact_gauge, 0.05)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == _dic_factors[contact_gauge] * 0.05**1.85


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_insert_temperature_no_gauge():
    """calculate_insert_temperature() should raise a KeyError when passed an unknown contact gauge."""
    with pytest.raises(KeyError):
        _temperature_rise = Connection.calculate_insert_temperature(0, 0.05)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_insert_temperature_string_current():
    """calculate_insert_temperature() should raise a TypeError when passed a string for the operating current."""
    with pytest.raises(TypeError):
        _temperature_rise = Connection.calculate_insert_temperature(12, '0.05')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_active_pins_factor():
    """calculate_active_pins_factor() should return a float value for piP on success."""
    _pi_p = Connection.calculate_active_pins_factor(15)

    assert isinstance(_pi_p, float)
    assert _pi_p == pytest.approx(3.2787411)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("n_circuit_planes", [1, 2])
def test_calculate_complexity_factor_less_than_three_planes(n_circuit_planes):
    """calculate_complexity_factor() should return 1.0 for piC when there are less than three planes in the PCB/PWA."""
    _pi_c = Connection.calculate_complexity_factor(n_circuit_planes)

    assert isinstance(_pi_c, float)
    assert _pi_c == 1.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("n_cycles", [0.01, 0.1, 1, 10, 100])
def test_get_mate_unmate_factor(n_cycles):
    """get_mate_unmate_factor() should return a float value for piK on success."""
    _pi_k = Connection.get_mate_unmate_factor(n_cycles)

    assert isinstance(_pi_k, float)
    if n_cycles == 0.01:
        assert _pi_k == 1.0
    elif n_cycles == 0.1:
        assert _pi_k == 1.5
    elif n_cycles == 1:
        assert _pi_k == 2.0
    elif n_cycles == 10:
        assert _pi_k == 3.0
    elif n_cycles == 100:
        assert _pi_k == 4.0


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 5])
def test_calculate_part_stress_lambda_b(subcategory_id):
    """calculate_part_stress_lamba_b() should return a float value for the part stress base hazard rate on success."""
    _lambda_b = Connection.calculate_part_stress_lambda_b(
        subcategory_id, 4, 8, 3, 325)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == pytest.approx(0.00097886687)
    elif subcategory_id == 3:
        assert _lambda_b == 0.00042
    elif subcategory_id == 5:
        assert _lambda_b == 5e-05


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_no_type():
    """calculate_part_stress_lamba_b() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = Connection.calculate_part_stress_lambda_b(1, 6, 8, 3, 325)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_no_specification():
    """calculate_part_stress_lamba_b() should raise a KeyError when passed an unknown specification ID."""
    with pytest.raises(KeyError):
        _lambda_b = Connection.calculate_part_stress_lambda_b(1, 4, 18, 3, 325)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_lambda_zero_contact_temperature():
    """calculate_part_stress_lamba_b() should raise a ZeroDivisionError when passed a contact temperature=0.0."""
    with pytest.raises(ZeroDivisionError):
        _lambda_b = Connection.calculate_part_stress_lambda_b(1, 4, 8, 3, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 3, 4, 5])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return a dict of updated attributes on success."""
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = Connection.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes['lambda_b'] == pytest.approx(0.00073120394)
        assert _attributes['piK'] == 1.5
        assert _attributes['piP'] == pytest.approx(3.27874110)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0035961426)
    elif subcategory_id == 3:
        assert _attributes['lambda_b'] == 0.00042
        assert _attributes['piP'] == pytest.approx(3.27874110)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.0013770713)
    elif subcategory_id == 4:
        assert _attributes['lambda_b'] == 0.00026
        assert _attributes['piC'] == pytest.approx(1.29867281)
        assert _attributes['hazard_rate_active'] == pytest.approx(0.030065092)
    elif subcategory_id == 5:
        assert _attributes['lambda_b'] == 0.00014
        assert _attributes['hazard_rate_active'] == 0.00014
