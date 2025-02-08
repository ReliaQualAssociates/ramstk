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
from tests.analyses.milhdbk217f.models.conftest import test_attributes_connection


@pytest.mark.unit
def test_set_default_active_pins():
    """Should return default number of active pins for the selected subcategory ID."""
    assert connection._set_default_active_pins(1, 1) == 40
    assert connection._set_default_active_pins(1, 4) == 2
    assert connection._set_default_active_pins(2, 1) == 40
    assert connection._set_default_active_pins(3, 1) == 24
    assert connection._set_default_active_pins(4, 1) == 1000
    assert connection._set_default_active_pins(5, 1) == 0


@pytest.mark.unit
def test_set_default_temperature_rise():
    """Should return the default temperature rise for the selected subcategory ID."""
    assert connection._set_default_temperature_rise(1, 1) == pytest.approx(10.0)
    assert connection._set_default_temperature_rise(1, 5) == pytest.approx(5.0)
    assert connection._set_default_temperature_rise(2, 1) == pytest.approx(10.0)
    assert connection._set_default_temperature_rise(5, 1) == pytest.approx(0.0)


@pytest.mark.unit
def test_set_default_values(
    test_attributes_connection,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_connection["temperature_rise"] = -50.0
    test_attributes_connection["n_cycles"] = -5.0
    test_attributes_connection["n_active_pins"] = 0
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    _attributes = connection.set_default_values(test_attributes_connection)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(10.0)
    assert _attributes["n_cycles"] == pytest.approx(3.0)
    assert _attributes["n_active_pins"] == 40


@pytest.mark.unit
def test_set_default_values_none_needed(
    test_attributes_connection,
):
    """Should not set default values for each parameter > 0.0."""
    test_attributes_connection["temperature_rise"] = 10.6
    test_attributes_connection["n_cycles"] = 0.5
    test_attributes_connection["n_active_pins"] = 36
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    _attributes = connection.set_default_values(test_attributes_connection)

    assert isinstance(_attributes, dict)
    assert _attributes["temperature_rise"] == pytest.approx(10.6)
    assert _attributes["n_cycles"] == pytest.approx(0.5)
    assert _attributes["n_active_pins"] == 36


@pytest.mark.unit
def test_set_default_values_partial_needed(
    test_attributes_connection,
):
    """Test that set_default_values() only sets default values for parameters <= 0."""
    test_attributes_connection["temperature_rise"] = -0.05
    test_attributes_connection["n_cycles"] = 3.0
    test_attributes_connection["n_active_pins"] = 0
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    _attributes = connection.set_default_values(test_attributes_connection)

    assert _attributes["temperature_rise"] == pytest.approx(10.0)  # default applied
    assert _attributes["n_cycles"] == pytest.approx(3.0)  # no default needed


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
def test_get_part_count_lambda_b(
    subcategory_id,
    environment_active_id,
    type_id,
    test_attributes_connection,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rates
    on success."""
    test_attributes_connection["subcategory_id"] = subcategory_id
    test_attributes_connection["environment_active_id"] = environment_active_id
    test_attributes_connection["type_id"] = type_id

    _lambda_b = connection.get_part_count_lambda_b(test_attributes_connection)
    assert isinstance(_lambda_b, float)

    # Verify a sampling of base hazard rates.
    if subcategory_id == 1 and environment_active_id == 1 and type_id == 1:
        assert _lambda_b == pytest.approx(0.011)

    if subcategory_id == 2 and environment_active_id == 2 and type_id == 2:
        assert _lambda_b == pytest.approx(0.021)

    if subcategory_id == 3 and environment_active_id == 8 and type_id == 1:
        assert _lambda_b == pytest.approx(0.021)

    if subcategory_id == 4 and environment_active_id == 12 and type_id == 2:
        assert _lambda_b == pytest.approx(0.53)

    if subcategory_id == 5 and environment_active_id == 4 and type_id == 1:
        assert _lambda_b == pytest.approx(0.01)


@pytest.mark.unit
def test_get_part_count_lambda_b_unknown_subcategory_id(
    test_attributes_connection,
):
    """Test that _get_part_count_lambda_b() raises KeyError when passed invalid
    types."""
    test_attributes_connection["subcategory_id"] = 34
    test_attributes_connection["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lamda_b: Invalid connection subcategory ID 34 or type ID 1.",
    ):
        connection.get_part_count_lambda_b(test_attributes_connection)


@pytest.mark.unit
def test_get_part_count_lambda_b_unknown_type_id(
    test_attributes_connection,
):
    """Test that _get_part_count_lambda_b() raises KeyError when passed invalid
    types."""
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 34
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lamda_b: Invalid connection subcategory ID 1 or type ID 34.",
    ):
        connection.get_part_count_lambda_b(test_attributes_connection)


@pytest.mark.unit
def test_get_part_count_lambda_b_unknown_environment_id(
    test_attributes_connection,
):
    """Test that _get_part_count_lambda_b() raises IndexError when passed invalid
    environments."""
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["type_id"] = 1
    test_attributes_connection["environment_active_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lamda_b: Invalid environment ID 22 for subcategory 1.",
    ):
        connection.get_part_count_lambda_b(test_attributes_connection)


@pytest.mark.unit
@pytest.mark.parametrize(
    "quality_id",
    [1, 2],
)
def test_get_part_count_quality_factor(
    quality_id,
    test_attributes_connection,
):
    test_attributes_connection["quality_id"] = quality_id
    _pi_q = connection.get_part_count_quality_factor(test_attributes_connection)

    assert _pi_q == {1: 1.0, 2: 2.0}[quality_id]


@pytest.mark.unit
def test_get_part_count_quality_factor_unknown_quality_id(
    test_attributes_connection,
):
    test_attributes_connection["quality_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_count_quality_factor: Invalid connection quality ID 22.",
    ):
        connection.get_part_count_quality_factor(test_attributes_connection)


@pytest.mark.unit
@pytest.mark.parametrize("contact_gauge", [12, 16, 20, 22, 26])
def test_calculate_insert_temperature(
    contact_gauge,
):
    """_calculate_insert_temperature() should return a float value for the temperature
    rise on success."""
    _dic_factors = {12: 0.1, 16: 0.274, 20: 0.64, 22: 0.989, 26: 2.1}
    _temperature_rise = connection._calculate_insert_temperature(contact_gauge, 0.05)

    assert isinstance(_temperature_rise, float)
    assert _temperature_rise == _dic_factors[contact_gauge] * 0.05**1.85


@pytest.mark.unit
def test_calculate_insert_temperature_unknown_gauge():
    """_calculate_insert_temperature() should raise a KeyError when passed an unknown
    contact gauge."""
    with pytest.raises(
        KeyError,
        match=r"_calculate_insert_temperature: Invalid connection contact gauge 0.",
    ):
        connection._calculate_insert_temperature(0, 0.05)


@pytest.mark.unit
def test_calculate_insert_temperature_string_current():
    """_calculate_insert_temperature() should raise a TypeError when passed a string for
    the operating current."""
    with pytest.raises(
        TypeError,
        match=r"_calculate_insert_temperature: Invalid type for connection operating "
        r"current: <class 'str'>.  Should be <class 'float'>.",
    ):
        connection._calculate_insert_temperature(12, "0.05")


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5])
def test_get_factor_key(
    type_id,
):
    _factor_key = connection._get_factor_key(type_id, 1, 2)

    assert _factor_key == {1: 2, 2: 2, 3: 2, 4: 3, 5: 3}[type_id]


@pytest.mark.unit
def test_get_factor_key_unknown_type_id():
    with pytest.raises(
        KeyError,
        match=r"_get_factor_key: Invalid connection specification ID 1 or type ID 22.",
    ):
        connection._get_factor_key(22, 1, 2)


@pytest.mark.unit
def test_get_factor_key_unknown_specification_id():
    with pytest.raises(
        KeyError,
        match=r"_get_factor_key: Invalid connection specification ID 11 or type ID 2.",
    ):
        connection._get_factor_key(2, 11, 2)


@pytest.mark.unit
def test_get_factor_key_unknown_insert_id():
    with pytest.raises(
        IndexError, match=r"_get_factor_key: Invalid connection insert ID 22."
    ):
        connection._get_factor_key(2, 1, 22)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 5])
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    test_attributes_connection,
):
    """calculate_part_stress_lamba_b() should return a float value for the part stress
    base hazard rate on success."""
    test_attributes_connection["subcategory_id"] = subcategory_id
    test_attributes_connection["type_id"] = 4
    test_attributes_connection["contact_gauge"] = 22
    test_attributes_connection["current_operating"] = 0.05

    _factor_key = 2 if subcategory_id == 1 else 5
    _lambda_b = connection.calculate_part_stress_lambda_b(test_attributes_connection)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == pytest.approx(0.004829323)
    elif subcategory_id == 3:
        assert _lambda_b == pytest.approx(0.00042)
    elif subcategory_id == 5:
        assert _lambda_b == pytest.approx(5e-05)


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_unknown_type_id(
    test_attributes_connection,
):
    """calculate_part_stress_lamba_b() should raise a KeyError when passed an unknown
    type ID."""
    test_attributes_connection["subcategory_id"] = 4
    test_attributes_connection["type_id"] = 26
    test_attributes_connection["contact_gauge"] = 22
    test_attributes_connection["current_operating"] = 0.05
    with pytest.raises(
        KeyError,
        match=r"_get_factor_key: Invalid connection specification ID 1 or type ID 26.",
    ):
        connection.calculate_part_stress_lambda_b(test_attributes_connection)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_environment_factor(
    environment_active_id,
    test_attributes_connection,
):
    test_attributes_connection["category_id"] = 2
    test_attributes_connection["subcategory_id"] = 2
    test_attributes_connection["environment_active_id"] = environment_active_id
    _pi_e = connection.get_environment_factor(test_attributes_connection)

    assert (
        _pi_e
        == {
            1: 2.0,
            2: 7.0,
            3: 17.0,
            4: 10.0,
            5: 26.0,
            6: 14.0,
            7: 22.0,
            8: 14.0,
            9: 22.0,
            10: 37.0,
            11: 0.8,
            12: 20.0,
            13: 54.0,
            14: 970.0,
        }[environment_active_id]
    )


@pytest.mark.unit
def test_get_environment_factor_invalid_category_id(
    test_attributes_connection,
):
    test_attributes_connection["category_id"] = 22
    test_attributes_connection["subcategory_id"] = 2
    test_attributes_connection["environment_active_id"] = 2

    assert connection.get_environment_factor(
        test_attributes_connection
    ) == pytest.approx(1.0)


@pytest.mark.unit
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_connection,
):
    test_attributes_connection["category_id"] = 2
    test_attributes_connection["subcategory_id"] = 22
    test_attributes_connection["environment_active_id"] = 2
    with pytest.raises(
        KeyError, match=r"get_environment_factor: Invalid connection subcategory ID 22."
    ):
        connection.get_environment_factor(test_attributes_connection)


@pytest.mark.unit
def test_get_environment_factor_invalid_environment_id(
    test_attributes_connection,
):
    test_attributes_connection["category_id"] = 2
    test_attributes_connection["subcategory_id"] = 2
    test_attributes_connection["environment_active_id"] = 22
    with pytest.raises(
        IndexError, match=r"get_environment_factor: Invalid environment ID 22."
    ):
        connection.get_environment_factor(test_attributes_connection)


@pytest.mark.unit
def test_get_part_stress_quality_factor(
    test_attributes_connection,
):
    test_attributes_connection["subcategory_id"] = 1
    test_attributes_connection["quality_id"] = 1
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 1.0

    test_attributes_connection["subcategory_id"] = 4
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 1.0

    test_attributes_connection["quality_id"] = 2
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 2.0

    test_attributes_connection["subcategory_id"] = 5
    test_attributes_connection["quality_id"] = 1
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 1.0

    test_attributes_connection["quality_id"] = 2
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 1.0

    test_attributes_connection["quality_id"] = 3
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 2.0

    test_attributes_connection["quality_id"] = 4
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 20.0


@pytest.mark.unit
def test_get_part_stress_quality_factor_invalid_subcategory_id(
    test_attributes_connection,
):
    test_attributes_connection["subcategory_id"] = 22
    assert connection.get_part_stress_quality_factor(test_attributes_connection) == 1.0


@pytest.mark.unit
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_connection,
):
    test_attributes_connection["subcategory_id"] = 4
    test_attributes_connection["quality_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid connection quality ID 22.",
    ):
        connection.get_part_stress_quality_factor(test_attributes_connection)


@pytest.mark.unit
@pytest.mark.parametrize("n_cycles", [0.01, 0.1, 1, 10, 100])
def test_get_mate_unmate_factor(
    n_cycles,
):
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
def test_calculate_active_pins_factor():
    """calculate_active_pins_factor() should return a float value for piP on success."""
    _pi_p = connection._calculate_active_pins_factor(15)

    assert isinstance(_pi_p, float)
    assert _pi_p == pytest.approx(3.2787411)


@pytest.mark.unit
@pytest.mark.parametrize("n_circuit_planes", [1, 2, 4])
def test_calculate_complexity_factor(
    n_circuit_planes,
):
    """calculate_complexity_factor() should return 1.0 for piC when there are less than
    three planes in the PCB/PWA."""
    _pi_c = connection._calculate_complexity_factor(n_circuit_planes)

    assert isinstance(_pi_c, float)
    if n_circuit_planes == 4:
        assert _pi_c == pytest.approx(1.5567223)
    else:
        assert _pi_c == pytest.approx(1.0)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 4, 5])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_connection,
):
    """calculate_part_stress() should return a dict of updated attributes on success."""
    test_attributes_connection["subcategory_id"] = subcategory_id
    test_attributes_connection["hazard_rate_active"] = 0.00073120394
    test_attributes_connection["n_active_pins"] = 8
    test_attributes_connection["n_cycles"] = 0.075
    _attributes = connection.calculate_part_stress(test_attributes_connection)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["piK"] == pytest.approx(1.5)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.001096806)
    elif subcategory_id == 3:
        assert _attributes["piP"] == pytest.approx(2.3013385)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.002524122)
    elif subcategory_id == 4:
        assert _attributes["piC"] == pytest.approx(1.29867281)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1268291)
    elif subcategory_id == 5:
        assert _attributes["hazard_rate_active"] == pytest.approx(0.001096806)
