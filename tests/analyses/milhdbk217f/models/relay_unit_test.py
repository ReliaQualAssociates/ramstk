# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.relay_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the relay module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import relay


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(subcategory_id, type_id, environment_active_id):
    """get_part_count_lambda_b() should return a float value for the parts count base
    hazard rate on success."""
    _lambda_b = relay.get_part_count_lambda_b(
        subcategory_id=subcategory_id,
        type_id=type_id,
        environment_active_id=environment_active_id,
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert (
            _lambda_b
            == [
                0.13,
                0.28,
                2.1,
                1.1,
                3.8,
                1.1,
                1.4,
                1.9,
                2.0,
                7.0,
                0.66,
                3.5,
                10.0,
                0.0,
            ][environment_active_id - 1]
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        relay.get_part_count_lambda_b(
            subcategory_id=13, type_id=1, environment_active_id=2
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type
    ID."""
    with pytest.raises(KeyError):
        relay.get_part_count_lambda_b(
            subcategory_id=1, type_id=11, environment_active_id=2
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown
    active environment ID."""
    with pytest.raises(IndexError):
        relay.get_part_count_lambda_b(
            subcategory_id=1, type_id=1, environment_active_id=21
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_calculate_part_count(test_attributes_relay):
    """calculate_part_count() should return a float value for the parts count base
    hazard rate on success."""
    _lambda_b = relay.calculate_part_count(**test_attributes_relay)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 2.1


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 7])
@pytest.mark.parametrize("n_cycles", [0.5, 100.0, 1103.4])
def test_calculate_cycling_factor(quality_id, n_cycles):
    """calculate_cycling_factor() should return a float value for piCYC on success or
    0.0 if passed an unknown combination of arguments."""
    _pi_cyc = relay.calculate_cycling_factor(quality_id, n_cycles)

    assert isinstance(_pi_cyc, float)
    if quality_id == 1 and n_cycles == 0.5:
        assert _pi_cyc == 0.1
    elif quality_id == 7 and n_cycles == 100.0:
        assert _pi_cyc == 10.0
    elif quality_id == 7 and n_cycles == 1103.4:
        assert _pi_cyc == pytest.approx(121.749156)
    elif quality_id == 1 and n_cycles == 100.0:
        assert _pi_cyc == 0.0


@pytest.mark.unit
@pytest.mark.parametrize("technology_id", [1, 2, 3, 4])
def test_calculate_load_stress_factor(technology_id):
    """calculate_load_stress_factor() should return a float value for piL on
    success."""
    _pi_l = relay.calculate_load_stress_factor(technology_id, 0.382)

    assert isinstance(_pi_l, float)
    if technology_id == 1:
        assert _pi_l == 0.22800625
    elif technology_id == 2:
        assert _pi_l == 0.912025
    elif technology_id == 3:
        assert _pi_l == 3.6481
    elif technology_id == 4:
        assert _pi_l == 0.0


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 7])
def test_get_environment_factor(subcategory_id, quality_id):
    """get_environment_factor() should return a float value for piE on success."""
    _pi_e = relay.get_environment_factor(subcategory_id, quality_id, 1)

    assert isinstance(_pi_e, float)
    if subcategory_id == 1 and quality_id == 1:
        assert _pi_e == 1.0
    elif subcategory_id == 1 and quality_id == 7:
        assert _pi_e == 2.0
    elif subcategory_id == 2:
        assert _pi_e == 1.0


@pytest.mark.unit
def test_get_environment_factor_no_subcategory():
    """get_environment_factor() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        relay.get_environment_factor(12, 1, 1)


@pytest.mark.unit
def test_get_environment_factor_no_environment():
    """get_environment_factor() should raise an IndexError if passed an unknown active
    environment ID."""
    with pytest.raises(IndexError):
        relay.get_environment_factor(1, 1, 21)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 7])
def test_get_application_construction_factor(quality_id):
    """get_application_construction_factor() should return a float value for piF on
    success."""
    _pi_f = relay.get_application_construction_factor(quality_id, 1, 1, 1)

    assert isinstance(_pi_f, float)
    assert _pi_f == {1: 4.0, 7: 8.0}[quality_id]


@pytest.mark.unit
def test_get_application_construction_factor_no_contact_rating():
    """get_application_construction_factor() should raise a KeyError if passed an
    unknown contact rating ID."""
    with pytest.raises(KeyError):
        relay.get_application_construction_factor(1, 15, 1, 1)


@pytest.mark.unit
def test_get_application_construction_factor_no_construction():
    """get_application_construction_factor() should raise a KeyError if passed an
    unknown construction ID."""
    with pytest.raises(KeyError):
        relay.get_application_construction_factor(1, 1, 15, 1)


@pytest.mark.unit
def test_get_application_construction_factor_no_application():
    """get_application_construction_factor() should raise a KeyError if passed an
    unknown application ID."""
    with pytest.raises(KeyError):
        relay.get_application_construction_factor(1, 1, 1, 15)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 3])
@pytest.mark.parametrize("type_id", [1, 2])
def test_calculate_part_stress_lambda_b(subcategory_id, type_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard
    rate on success."""
    _lambda_b = relay.calculate_part_stress_lambda_b(subcategory_id, type_id, 38.2)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert _lambda_b == pytest.approx(0.0064130981)
    elif subcategory_id == 1 and type_id == 2:
        assert _lambda_b == pytest.approx(0.0061869201)
    elif subcategory_id == 2:
        assert _lambda_b == [0.4, 0.5, 0.5][type_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_relay,
):
    """calculate_part_stress() should return the attributes with updated values on
    success."""
    test_attributes_relay["type_id"] = 1
    test_attributes_relay["subcategory_id"] = subcategory_id
    _attributes = relay.calculate_part_stress(**test_attributes_relay)

    assert isinstance(_attributes, dict)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 4])
def test_set_default_quality(subcategory_id):
    """should return the default quality for the selected subcategory ID."""
    _quality = relay._set_default_quality(subcategory_id)

    assert _quality == {1: 1, 4: 5}[subcategory_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2])
def test_set_default_load_type(type_id):
    """should return the default load type for the selected type ID."""
    _load_type = relay._set_default_load_type(-1, type_id)

    assert _load_type == {1: 1, 2: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_contact_form(type_id):
    """should return the default contact form for the selected type ID."""
    _contact_form = relay._set_default_contact_form(-1, type_id)

    assert _contact_form == {1: 6, 4: 1}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_contact_rating(type_id):
    """should return the default contact rating for the selected type ID."""
    _contact_rating = relay._set_default_contact_rating(-2, type_id)

    assert _contact_rating == {1: 2, 2: 4, 3: 2, 4: 1, 5: 2, 6: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_application(type_id):
    """should return the default application for the selected type ID."""
    _application = relay._set_default_application(0, type_id)

    assert _application == {1: 1, 2: 1, 3: 8, 4: 1, 5: 6, 6: 3}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_construction(type_id):
    """should return the default construction for the selected type ID."""
    _construction = relay._set_default_construction(0, type_id)

    assert _construction == {1: 2, 2: 4, 3: 2, 4: 2, 5: 1, 6: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_duty_cycle(type_id):
    """should return the default duty cycle for the selected type ID."""
    _duty_cycle = relay._set_default_duty_cycle(0.0, type_id)

    assert _duty_cycle == {1: 10.0, 4: 20.0}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_rated_temperature(type_id):
    """should return the default rated temperature for the selected type ID."""
    _rated_temperature = relay._set_default_rated_temperature(0.0, type_id)

    assert _rated_temperature == {1: 125.0, 4: 85.0}[type_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_set_default_values(test_attributes_relay):
    """should set default values for each parameter <= 0.0."""
    test_attributes_relay["application_id"] = 0
    test_attributes_relay["construction_id"] = 0
    test_attributes_relay["contact_form_id"] = 0
    test_attributes_relay["contact_rating_id"] = 0
    test_attributes_relay["current_ratio"] = 0.0
    test_attributes_relay["duty_cycle"] = -2.5
    test_attributes_relay["quality_id"] = 0
    test_attributes_relay["subcategory_id"] = 1
    test_attributes_relay["technology_id"] = -1
    test_attributes_relay["temperature_rated_max"] = 0.0
    test_attributes_relay["type_id"] = 1
    _attributes = relay.set_default_values(**test_attributes_relay)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 1
    assert _attributes["construction_id"] == 2
    assert _attributes["contact_form_id"] == 6
    assert _attributes["contact_rating_id"] == 2
    assert _attributes["current_ratio"] == 0.5
    assert _attributes["duty_cycle"] == 10.0
    assert _attributes["quality_id"] == 1
    assert _attributes["technology_id"] == 1
    assert _attributes["temperature_rated_max"] == 125.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_set_default_values_none_needed(test_attributes_relay):
    """should not set default values for each parameter > 0.0."""
    test_attributes_relay["application_id"] = 2
    test_attributes_relay["construction_id"] = 4
    test_attributes_relay["contact_form_id"] = 2
    test_attributes_relay["contact_rating_id"] = 1
    test_attributes_relay["current_ratio"] = 0.3
    test_attributes_relay["duty_cycle"] = 45.0
    test_attributes_relay["quality_id"] = 2
    test_attributes_relay["subcategory_id"] = 1
    test_attributes_relay["technology_id"] = 2
    test_attributes_relay["temperature_rated_max"] = 105.0
    test_attributes_relay["type_id"] = 1
    _attributes = relay.set_default_values(**test_attributes_relay)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 2
    assert _attributes["construction_id"] == 4
    assert _attributes["contact_form_id"] == 2
    assert _attributes["contact_rating_id"] == 1
    assert _attributes["current_ratio"] == 0.3
    assert _attributes["duty_cycle"] == 45.0
    assert _attributes["quality_id"] == 2
    assert _attributes["technology_id"] == 2
    assert _attributes["temperature_rated_max"] == 105.0
