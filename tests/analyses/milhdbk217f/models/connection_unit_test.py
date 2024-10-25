# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.connection_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the connection module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import connection


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("type_id", [1, 2])
def test_get_part_count_lambda_b(subcategory_id, environment_active_id, type_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rates
    on success."""
    _lambda_b = connection._get_part_count_lambda_b(
        subcategory_id=subcategory_id,
        environment_active_id=environment_active_id,
        type_id=type_id,
    )
    assert isinstance(_lambda_b, float)

    # Verify a sampling of base hazard rates.


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        connection._get_part_count_lambda_b(
            subcategory_id=88, environment_active_id=12, type_id=2
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b_list() should raise an IndexError when passed an unknown
    active environment ID."""
    with pytest.raises(IndexError):
        connection._get_part_count_lambda_b(
            subcategory_id=3, environment_active_id=22, type_id=-1
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type
    ID."""
    with pytest.raises(KeyError):
        connection._get_part_count_lambda_b(
            subcategory_id=1, environment_active_id=2, type_id=22
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_connection")
def test_calculate_part_count(test_attributes_connection):
    """calculate_part_count() should return a list of base hazard rates on success."""
    _lst_lambda_b = connection.calculate_part_count(**test_attributes_connection)

    assert isinstance(_lst_lambda_b, float)
    assert _lst_lambda_b == pytest.approx(0.03)


@pytest.mark.unit
@pytest.mark.parametrize("contact_gauge", [12, 16, 20, 22, 26])
def test_calculate_insert_temperature(contact_gauge):
    """calculate_insert_temperature() should return a float value for the temperature
    rise on success."""
    _dic_factors = {12: 0.1, 16: 0.274, 20: 0.64, 22: 0.989, 26: 2.1}
    _temperature_rise = connection._calculate_insert_temperature(contact_gauge, 0.05)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == _dic_factors[contact_gauge] * 0.05**1.85


@pytest.mark.unit
def test_calculate_insert_temperature_no_gauge():
    """calculate_insert_temperature() should raise a KeyError when passed an unknown
    contact gauge."""
    with pytest.raises(KeyError):
        connection._calculate_insert_temperature(0, 0.05)


@pytest.mark.unit
def test_calculate_insert_temperature_string_current():
    """calculate_insert_temperature() should raise a TypeError when passed a string for
    the operating current."""
    with pytest.raises(TypeError):
        connection._calculate_insert_temperature(12, "0.05")


@pytest.mark.unit
def test_calculate_active_pins_factor():
    """calculate_active_pins_factor() should return a float value for piP on success."""
    _pi_p = connection._calculate_active_pins_factor(15)

    assert isinstance(_pi_p, float)
    assert _pi_p == pytest.approx(3.2787411)


@pytest.mark.unit
@pytest.mark.parametrize("n_circuit_planes", [1, 2])
def test_calculate_complexity_factor_less_than_three_planes(n_circuit_planes):
    """calculate_complexity_factor() should return 1.0 for piC when there are less than
    three planes in the PCB/PWA."""
    _pi_c = connection._calculate_complexity_factor(n_circuit_planes)

    assert isinstance(_pi_c, float)
    assert _pi_c == pytest.approx(1.0)


@pytest.mark.unit
@pytest.mark.parametrize("n_cycles", [0.01, 0.1, 1, 10, 100])
def test_get_mate_unmate_factor(n_cycles):
    """get_mate_unmate_factor() should return a float value for piK on success."""
    _pi_k = connection._get_mate_unmate_factor(n_cycles)

    assert isinstance(_pi_k, float)
    if n_cycles == 0.01:
        assert _pi_k == pytest.approx(1.0)
    elif n_cycles == 0.1:
        assert _pi_k == pytest.approx(1.5)
    elif n_cycles == 1:
        assert _pi_k == pytest.approx(2.0)
    elif n_cycles == 10:
        assert _pi_k == pytest.approx(3.0)
    elif n_cycles == 100:
        assert _pi_k == pytest.approx(4.0)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 5])
def test_calculate_part_stress_lambda_b(subcategory_id):
    """calculate_part_stress_lamba_b() should return a float value for the part stress
    base hazard rate on success."""
    _factor_key = 2 if subcategory_id == 1 else 5
    _lambda_b = connection._calculate_part_stress_lambda_b(
        subcategory_id, 4, 325, _factor_key
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == pytest.approx(0.00097886687)
    elif subcategory_id == 3:
        assert _lambda_b == pytest.approx(0.00042)
    elif subcategory_id == 5:
        assert _lambda_b == pytest.approx(5e-05)


@pytest.mark.unit
def test_calculate_part_stress_lambda_no_type():
    """calculate_part_stress_lamba_b() should raise an IndexError when passed an unknown
    type ID."""
    with pytest.raises(IndexError):
        connection._calculate_part_stress_lambda_b(4, 26, 325, 5)


@pytest.mark.unit
def test_calculate_part_stress_lambda_zero_contact_temperature():
    """calculate_part_stress_lamba_b() should raise a ZeroDivisionError when passed a
    contact temperature=0.0."""
    with pytest.raises(ZeroDivisionError):
        connection._calculate_part_stress_lambda_b(1, 4, 0.0, 2)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_connection")
@pytest.mark.parametrize("subcategory_id", [1, 3, 4, 5])
def test_calculate_part_stress(subcategory_id, test_attributes_connection):
    """calculate_part_stress() should return a dict of updated attributes on success."""
    test_attributes_connection["subcategory_id"] = subcategory_id
    _attributes = connection.calculate_part_stress(**test_attributes_connection)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["lambda_b"] == pytest.approx(0.00073120394)
        assert _attributes["piK"] == pytest.approx(1.5)
        assert _attributes["piP"] == pytest.approx(3.27874110)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0035961426)
    elif subcategory_id == 3:
        assert _attributes["lambda_b"] == pytest.approx(0.00042)
        assert _attributes["piP"] == pytest.approx(3.27874110)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0013770713)
    elif subcategory_id == 4:
        assert _attributes["lambda_b"] == pytest.approx(0.00026)
        assert _attributes["piC"] == pytest.approx(1.29867281)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1202604)
    elif subcategory_id == 5:
        assert _attributes["lambda_b"] == pytest.approx(0.00014)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00014)


@pytest.mark.unit
def test_set_default_active_pins():
    """Should return default number of active pins for the selected subcategory ID."""
    _n_active_pins = connection._set_default_active_pins(1, 1)
    assert _n_active_pins == 40

    _n_active_pins = connection._set_default_active_pins(1, 4)
    assert _n_active_pins == 2

    _n_active_pins = connection._set_default_active_pins(2, 1)
    assert _n_active_pins == 40

    _n_active_pins = connection._set_default_active_pins(3, 1)
    assert _n_active_pins == 24

    _n_active_pins = connection._set_default_active_pins(4, 1)
    assert _n_active_pins == 1000

    _n_active_pins = connection._set_default_active_pins(5, 1)
    assert _n_active_pins == 0


@pytest.mark.unit
def test_set_default_temperature_rise():
    """Should return the default temperature rise for the selected subcategory ID."""
    _temperature_rise = connection._set_default_temperature_rise(1, 1)
    assert _temperature_rise == pytest.approx(10.0)

    _temperature_rise = connection._set_default_temperature_rise(1, 5)
    assert _temperature_rise == pytest.approx(5.0)

    _temperature_rise = connection._set_default_temperature_rise(2, 1)
    assert _temperature_rise == pytest.approx(10.0)

    _temperature_rise = connection._set_default_temperature_rise(5, 1)
    assert _temperature_rise == pytest.approx(0.0)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_connection")
def test_set_default_values(test_attributes_connection):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_connection["temperature_rise"] = -50.0
    test_attributes_connection["n_cycles"] = -5.0
    test_attributes_connection["n_active_pins"] = 0
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    _attributes = connection.set_default_values(**test_attributes_connection)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(10.0)
    assert _attributes["n_cycles"] == pytest.approx(3.0)
    assert _attributes["n_active_pins"] == 40


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_connection")
def test_set_default_values_none_needed(test_attributes_connection):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_connection["temperature_rise"] = 10.6
    test_attributes_connection["n_cycles"] = 0.5
    test_attributes_connection["n_active_pins"] = 36
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    _attributes = connection.set_default_values(**test_attributes_connection)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(10.6)
    assert _attributes["n_cycles"] == pytest.approx(0.5)
    assert _attributes["n_active_pins"] == 36


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id", [0, 6]
)  # values just outside the valid range
def test_get_part_count_lambda_b_out_of_range(subcategory_id):
    """Test that _get_part_count_lambda_b() handles out-of-range subcategory IDs
    properly."""
    with pytest.raises(KeyError):
        connection._get_part_count_lambda_b(subcategory_id, 2, 1)


@pytest.mark.unit
def test_get_part_count_lambda_b_invalid_type():
    """Test that _get_part_count_lambda_b() raises TypeError when passed invalid
    types."""
    with pytest.raises(KeyError):
        connection._get_part_count_lambda_b("invalid", 2, 1)


@pytest.mark.unit
def test_set_default_values_partial_default():
    """Test that set_default_values() only sets default values for parameters <= 0."""
    test_attributes_connection = {
        "temperature_rise": -0.05,
        "n_cycles": 3.0,
        "n_active_pins": 0,
        "subcategory_id": 1,
        "type_id": 1,
    }
    _attributes = connection.set_default_values(**test_attributes_connection)

    assert _attributes["temperature_rise"] == pytest.approx(10.0)  # default applied
    assert _attributes["n_cycles"] == pytest.approx(3.0)  # no default needed
