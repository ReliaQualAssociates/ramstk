# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.semiconductor_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the semiconductor module."""

# Standard Library Imports
import copy

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import semiconductor


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 5])
def test_get_part_count_quality_factor(
    subcategory_id,
    type_id,
):
    """get_part_count_quality_factor() should return a float value for piQ on
    success."""
    _pi_q = semiconductor.get_part_count_quality_factor(subcategory_id, 3, type_id)

    assert isinstance(_pi_q, float)
    if subcategory_id == 1:
        assert _pi_q == 2.4
    elif subcategory_id == 2 and type_id == 1:
        assert _pi_q == 5.0
    elif subcategory_id == 2 and type_id == 5:
        assert _pi_q == 1.8


@pytest.mark.unit
def test_get_part_count_quality_factor_no_quality():
    """get_part_count_quality_factor() should raise an IndexError when passed an
    unknown quality ID."""
    with pytest.raises(IndexError):
        semiconductor.get_part_count_quality_factor(
            3,
            33,
            1,
        )


@pytest.mark.unit
def test_get_part_count_quality_factor_no_subcategory():
    """get_part_count_quality_factor() should raise a KeyError when passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        semiconductor.get_part_count_quality_factor(
            21,
            1,
            1,
        )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 4])
def test_get_part_count_lambda_b(subcategory_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
    _lambda_b = semiconductor.get_part_count_lambda_b(
        subcategory_id,
        3,
        1,
    )

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.049, 4: 0.16}[subcategory_id]


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active
    environment ID."""
    with pytest.raises(IndexError):
        semiconductor.get_part_count_lambda_b(
            1,
            32,
            1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        semiconductor.get_part_count_lambda_b(
            47,
            3,
            1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown type
    ID."""
    with pytest.raises(KeyError):
        semiconductor.get_part_count_lambda_b(
            1,
            3,
            31,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 2, 4])
@pytest.mark.parametrize("type_id", [1, 5])
def test_calculate_part_count(subcategory_id, type_id, test_attributes_semiconductor):
    """calculate_part_count() should return the semiconductor attributes dict with
    updated values."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["type_id"] = type_id
    _lambda_b = semiconductor.calculate_part_count(**_attributes)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert _lambda_b == 0.049
    elif subcategory_id == 1 and type_id == 5:
        assert _lambda_b == 0.04
    elif subcategory_id == 2 and type_id == 1:
        assert _lambda_b == 8.9
    elif subcategory_id == 2 and type_id == 5:
        assert _lambda_b == 0.31
    elif subcategory_id == 4:
        assert _lambda_b == 0.16


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_get_part_stress_quality_factor(subcategory_id):
    """get_part_stress_quality_factor() should return a float value for piQ on
    success."""
    _pi_q = semiconductor.get_part_stress_quality_factor(
        subcategory_id,
        3,
        1,
    )

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 2.4, 2: 5.0}[subcategory_id]


@pytest.mark.unit
def test_get_part_stress_quality_factor_no_quality():
    """get_part_stress_quality_factor() should raise an IndexError when passed an
    unknown quality ID."""
    with pytest.raises(IndexError):
        semiconductor.get_part_stress_quality_factor(
            3,
            31,
            1,
        )


@pytest.mark.unit
def test_get_part_stress_quality_factor_no_subcategory():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        semiconductor.get_part_stress_quality_factor(
            21,
            1,
            1,
        )


@pytest.mark.unit
def test_get_part_stress_quality_factor_no_type():
    """get_part_stress_quality_factor() should raise a KeyError when passed an unknown
    type ID."""
    with pytest.raises(KeyError):
        semiconductor.get_part_stress_quality_factor(
            2,
            1,
            21,
        )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 7, 8, 12])
@pytest.mark.parametrize("frequency_operating", [0.5, 5.0])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    frequency_operating,
    application_id,
):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard
    rate on success."""
    _lambda_b = semiconductor.calculate_part_stress_lambda_b(
        subcategory_id,
        1,
        application_id,
        frequency_operating,
        0.05,
        8,
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == 0.0038
    elif subcategory_id == 3:
        assert _lambda_b == 0.00074
    elif subcategory_id == 7 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.038206853)
    elif subcategory_id == 8 and frequency_operating == 0.5:
        assert _lambda_b == pytest.approx(0.011808438)
    elif subcategory_id == 8 and frequency_operating == 5.0:
        assert _lambda_b == 0.052
    elif subcategory_id == 12 and application_id == 1:
        assert _lambda_b == 0.003483
    elif subcategory_id == 12 and application_id == 2:
        assert _lambda_b == 0.00344


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_type():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown
    type ID."""
    with pytest.raises(IndexError):
        semiconductor.calculate_part_stress_lambda_b(
            1,
            11,
            1,
            1.5,
            0.055,
            8,
        )


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_subcategory():
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        semiconductor.calculate_part_stress_lambda_b(
            2300,
            1,
            1,
            5,
            0.05,
            8,
        )


@pytest.mark.unit
def test_calculate_junction_temperature():
    """calculate_junction_temperature() should return a float value for the junction
    temperature on success."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        38.2,
        105.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 43.45


@pytest.mark.unit
def test_calculate_junction_temperature_zero_case_temp():
    """calculate_junction_temperature() should return a float value for the case
    temperature and the junction temperature when passed a case temperature <=0.0."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        -38.2,
        105.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 40.25


@pytest.mark.unit
def test_calculate_junction_temperature_zero_theta_jc():
    """calculate_junction_temperature() should return a float value for the thetaJC and
    the junction temperature when passed a theta_jc <=0.0."""
    _temperature_junction = semiconductor.calculate_junction_temperature(
        1,
        2,
        38.2,
        0.0,
        0.05,
    )

    assert isinstance(_temperature_junction, float)
    assert _temperature_junction == 38.7


@pytest.mark.unit
def test_calculate_junction_temperature_zero_case_temp_no_environment():
    """calculate_junction_temperature() should raise an IndexError when passed a case
    temperature <=0.0 and an unknown active environment_id."""
    with pytest.raises(IndexError):
        semiconductor.calculate_junction_temperature(
            31,
            1,
            0.0,
            105.0,
            0.05,
        )


@pytest.mark.unit
def test_calculate_junction_temperature_zero_theta_jc_no_package():
    """calculate_junction_temperature() should raise an IndexError when passed a
    theta_jc <=0.0 and an unknown package ID."""
    with pytest.raises(IndexError):
        semiconductor.calculate_junction_temperature(
            1,
            128,
            38.2,
            -10.0,
            0.05,
        )


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 3, 7])
@pytest.mark.parametrize("voltage_ratio", [0.4, 0.8])
def test_calculate_temperature_factor(
    subcategory_id,
    voltage_ratio,
):
    """calculate_temperature_factor() should return a float value for piT on
    success."""
    _pi_t = semiconductor.calculate_temperature_factor(
        subcategory_id,
        1,
        voltage_ratio,
        52.8,
    )

    assert isinstance(_pi_t, float)
    if subcategory_id == 1:
        assert _pi_t == pytest.approx(2.42314826)
    elif subcategory_id == 3:
        assert _pi_t == pytest.approx(1.83183169)
    elif subcategory_id == 7 and voltage_ratio == 0.4:
        assert _pi_t == pytest.approx(0.229615567)
    elif subcategory_id == 7 and voltage_ratio == 0.8:
        assert _pi_t == pytest.approx(2.06654010)


@pytest.mark.unit
def test_calculate_temperature_factor_no_subcategory():
    """calculate_temperature_factor() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        semiconductor.calculate_temperature_factor(
            27,
            1,
            0.5,
            52.8,
        )


@pytest.mark.unit
def test_calculate_temperature_factor_no_type():
    """calculate_temperature_factor() should raise an IndexError if passed an unknown
    type ID."""
    with pytest.raises(IndexError):
        semiconductor.calculate_temperature_factor(
            2,
            17,
            0.5,
            52.8,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 2, 7, 13])
@pytest.mark.parametrize("application_id", [1, 2])
def test_calculate_application_factor(
    subcategory_id, application_id, test_attributes_semiconductor
):
    """calculate_application_factor() should return a float value on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["application_id"] = application_id
    _attributes["duty_cycle"] = 65.0

    _attributes = semiconductor.calculate_application_factor(_attributes)

    assert isinstance(_attributes["piA"], float)
    if subcategory_id == 1:
        assert _attributes["piA"] == 0.0
    elif subcategory_id == 2 and application_id == 1:
        assert _attributes["piA"] == 0.5
    elif subcategory_id == 2 and application_id == 2:
        assert _attributes["piA"] == 2.5
    elif subcategory_id == 7 and application_id == 1:
        assert _attributes["piA"] == 7.6
    elif subcategory_id == 7 and application_id == 2:
        assert _attributes["piA"] == 0.439
    elif subcategory_id == 13 and application_id == 1:
        assert _attributes["piA"] == 4.4
    elif subcategory_id == 13 and application_id == 2:
        assert _attributes["piA"] == pytest.approx(0.80622577)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_type_6(test_attributes_semiconductor):
    """calculate_application_factor() should return a float value on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 2
    _attributes["application_id"] = 1
    _attributes["type_id"] = 6

    _attributes = semiconductor.calculate_application_factor(_attributes)

    assert isinstance(_attributes["piA"], float)
    assert _attributes["piA"] == 0.5


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_no_application(test_attributes_semiconductor):
    """calculate_application_factor() should return the default piA when passed an
    unknown application ID."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 4
    _attributes["application_id"] = 11
    _attributes["duty_cycle"] = 65.0
    with pytest.raises(IndexError):
        _attributes = semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_application_factor_negative_duty_cycle(
    test_attributes_semiconductor,
):
    """calculate_application_factor() should raise a ValueError when passed a negative
    value for the duty cycle."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 13
    _attributes["application_id"] = 2
    _attributes["duty_cycle"] = -65.0
    with pytest.raises(ValueError):
        _attributes = semiconductor.calculate_application_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 4])
@pytest.mark.parametrize("power_rated", [0.075, 10.0])
def test_calculate_power_rating_factor(
    subcategory_id, type_id, power_rated, test_attributes_semiconductor
):
    """calculate_power_rating_factor() should return a float value for piR on
    success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["type_id"] = type_id
    _attributes["power_rated"] = power_rated
    _attributes["current_rated"] = 0.125
    _attributes = semiconductor.calculate_power_rating_factor(_attributes)

    assert isinstance(_attributes["piR"], float)
    if subcategory_id == 2 and type_id == 1:
        assert _attributes["piR"] == 1.0
    elif subcategory_id == 2 and type_id == 4 and power_rated == 10.0:
        assert _attributes["piR"] == pytest.approx(0.50064274)
    elif subcategory_id == 3 and power_rated == 0.075:
        assert _attributes["piR"] == 0.43
    elif subcategory_id == 3 and power_rated == 10.0:
        assert _attributes["piR"] == pytest.approx(2.34422882)
    elif subcategory_id == 10:
        assert _attributes["piR"] == pytest.approx(0.435275282)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_power_rating_factor_low_power_bjt(test_attributes_semiconductor):
    """calculate_power_rating_factor() should set piR=0.43 for a low power BJT with
    rated power < 0.1W."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 6
    _attributes["power_rated"] = 0.05

    _attributes = semiconductor.calculate_power_rating_factor(_attributes)

    assert _attributes["piR"] == 0.43


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_power_rating_factor_negative_input(test_attributes_semiconductor):
    """calculate_power_rating_factor() should raise a ValueError when passed a negative
    value for rated power."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = 2
    _attributes["type_id"] = 4
    _attributes["power_rated"] = -10.0
    _attributes["current_rated"] = 0.125
    with pytest.raises(ValueError):
        semiconductor.calculate_power_rating_factor(_attributes)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 10])
@pytest.mark.parametrize("type_id", [1, 6])
@pytest.mark.parametrize("voltage_ratio", [0.25, 0.75])
def test_calculate_electrical_stress_factor(
    subcategory_id, type_id, voltage_ratio, test_attributes_semiconductor
):
    """calculate_electrical_stress_factor() should return a float value on success."""
    _attributes = copy.deepcopy(test_attributes_semiconductor)
    _attributes["subcategory_id"] = subcategory_id
    _attributes["type_id"] = type_id
    _attributes["voltage_ratio"] = voltage_ratio
    _attributes = semiconductor.calculate_electrical_stress_factor(_attributes)

    assert isinstance(_attributes["piS"], float)
    if subcategory_id == 1 and type_id == 6:
        assert _attributes["piS"] == 1.0
    elif subcategory_id == 1 and voltage_ratio == 0.25:
        assert _attributes["piS"] == 0.054
    elif subcategory_id == 1 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.49704862)
    elif subcategory_id == 3 and voltage_ratio == 0.25:
        assert _attributes["piS"] == pytest.approx(0.097676646)
    elif subcategory_id == 10 and voltage_ratio == 0.25:
        assert _attributes["piS"] == 0.1
    elif subcategory_id == 10 and voltage_ratio == 0.75:
        assert _attributes["piS"] == pytest.approx(0.57891713)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 6, 7, 13])
def test_calculate_part_stress(subcategory_id, test_attributes_semiconductor):
    """calculate_part_stress() should return the semiconductor attributes dict with
    updated values on success."""
    test_attributes_semiconductor["subcategory_id"] = subcategory_id
    test_attributes_semiconductor["type_id"] = 1
    _attributes = semiconductor.calculate_part_stress(**test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["lambda_b"] == 0.0038
        assert _attributes["temperature_junction"] == 45.7
        assert _attributes["piC"] == 1.0
        assert _attributes["piQ"] == 0.7
        assert _attributes["piS"] == pytest.approx(0.14365026)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0007495062)
    elif subcategory_id == 2:
        assert _attributes["piA"] == 0.5
        assert _attributes["piR"] == 1.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.1730863)
    elif subcategory_id == 6:
        assert _attributes["piR"] == 1.0
        assert _attributes["piS"] == pytest.approx(0.18157386)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.02590612)
    elif subcategory_id == 7:
        assert _attributes["piM"] == 2.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.2225089)
    elif subcategory_id == 13:
        assert _attributes["piI"] == pytest.approx(0.10820637)
        assert _attributes["piP"] == pytest.approx(0.69444444)
        assert _attributes["hazard_rate_active"] == pytest.approx(2.9328130)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_no_construction(test_attributes_semiconductor):
    """calculate_part_stress() should raise an IndexError if passed an unknown
    construction ID."""
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["construction_id"] = 5
    with pytest.raises(IndexError):
        semiconductor.calculate_part_stress(**test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_calculate_part_stress_no_matching(test_attributes_semiconductor):
    """calculate_part_stress() should raise an IndexError if passed an unknown matching
    ID."""
    test_attributes_semiconductor["subcategory_id"] = 1
    test_attributes_semiconductor["construction_id"] = 1
    test_attributes_semiconductor["matching_id"] = 6
    with pytest.raises(IndexError):
        semiconductor.calculate_part_stress(**test_attributes_semiconductor)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 4, 7, 8],
)
def test_set_default_application_id(subcategory_id):
    """should return the default application ID for the selected subcategory ID."""
    _application_id = semiconductor._set_default_application_id(0, subcategory_id, 1)

    assert (
        _application_id
        == {
            2: 0,
            3: 2,
            4: 2,
            7: 2,
            8: 1,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 6, 7, 8],
)
def test_set_default_rated_power(subcategory_id):
    """should return the default rated power for the selected subcategory ID."""
    _power_rated = semiconductor._set_default_rated_power(0.0, subcategory_id, 1)

    assert (
        _power_rated
        == {
            2: 0.0,
            3: 0.5,
            6: 0.5,
            7: 100.0,
            8: 0.0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 3, 6, 13],
)
def test_set_default_voltage_ratio(subcategory_id):
    """should return the default voltage ratio for the selected subcategory ID."""
    _voltage_ratio = semiconductor._set_default_voltage_ratio(0.0, subcategory_id, 1)

    assert (
        _voltage_ratio
        == {
            1: 0.7,
            3: 0.5,
            6: 0.7,
            13: 0.5,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_set_default_values(test_attributes_semiconductor):
    """should set default values for each parameter <= 0.0."""
    test_attributes_semiconductor["application_id"] = 0
    test_attributes_semiconductor["construction_id"] = 0
    test_attributes_semiconductor["power_rated"] = 0.0
    test_attributes_semiconductor["subcategory_id"] = 4
    test_attributes_semiconductor["type_id"] = 0
    test_attributes_semiconductor["voltage_ratio"] = -2.5
    _attributes = semiconductor.set_default_values(**test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 2
    assert _attributes["type_id"] == 1
    assert _attributes["power_rated"] == 0.0
    assert _attributes["voltage_ratio"] == 1.0

    test_attributes_semiconductor["subcategory_id"] = 1
    _attributes = semiconductor.set_default_values(**test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["construction_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_semiconductor")
def test_set_default_values_none_needed(test_attributes_semiconductor):
    """should set default values for each parameter <= 0.0."""
    test_attributes_semiconductor["application_id"] = 2
    test_attributes_semiconductor["construction_id"] = 4
    test_attributes_semiconductor["power_rated"] = 0.5
    test_attributes_semiconductor["subcategory_id"] = 4
    test_attributes_semiconductor["type_id"] = 2
    test_attributes_semiconductor["voltage_ratio"] = 0.45
    _attributes = semiconductor.set_default_values(**test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 2
    assert _attributes["type_id"] == 2
    assert _attributes["power_rated"] == 0.5
    assert _attributes["voltage_ratio"] == 0.45

    test_attributes_semiconductor["subcategory_id"] = 1
    _attributes = semiconductor.set_default_values(**test_attributes_semiconductor)

    assert isinstance(_attributes, dict)
    assert _attributes["construction_id"] == 4
