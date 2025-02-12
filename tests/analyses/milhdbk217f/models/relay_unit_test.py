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
@pytest.mark.parametrize("subcategory_id", [1, 4])
def test_set_default_quality(
    subcategory_id,
):
    """Should return the default quality for the selected subcategory ID."""
    _quality = relay._set_default_quality(subcategory_id)

    assert _quality == {1: 1, 4: 5}[subcategory_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2])
def test_set_default_load_type(
    type_id,
):
    """Should return the default load type for the selected type ID."""
    _load_type = relay._set_default_load_type(-1, type_id)

    assert _load_type == {1: 1, 2: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_contact_form(
    type_id,
):
    """Should return the default contact form for the selected type ID."""
    _contact_form = relay._set_default_contact_form(-1, type_id)

    assert _contact_form == {1: 6, 4: 1}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_contact_rating(
    type_id,
):
    """Should return the default contact rating for the selected type ID."""
    _contact_rating = relay._set_default_contact_rating(-2, type_id)

    assert _contact_rating == {1: 2, 2: 4, 3: 2, 4: 1, 5: 2, 6: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_application(
    type_id,
):
    """Should return the default application for the selected type ID."""
    _application = relay._set_default_application(0, type_id)

    assert _application == {1: 1, 2: 1, 3: 8, 4: 1, 5: 6, 6: 3}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
def test_set_default_construction(
    type_id,
):
    """Should return the default construction for the selected type ID."""
    _construction = relay._set_default_construction(0, type_id)

    assert _construction == {1: 2, 2: 4, 3: 2, 4: 2, 5: 1, 6: 2}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_duty_cycle(
    type_id,
):
    """Should return the default duty cycle for the selected type ID."""
    _duty_cycle = relay._set_default_duty_cycle(0.0, type_id)

    assert _duty_cycle == {1: 10.0, 4: 20.0}[type_id]


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 4])
def test_set_default_rated_temperature(
    type_id,
):
    """Should return the default rated temperature for the selected type ID."""
    _rated_temperature = relay._set_default_rated_temperature(0.0, type_id)

    assert _rated_temperature == {1: 125.0, 4: 85.0}[type_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_set_default_values(
    test_attributes_relay,
):
    """Should set default values for each parameter <= 0.0."""
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
    _attributes = relay.set_default_values(test_attributes_relay)

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
def test_set_default_values_none_needed(
    test_attributes_relay,
):
    """Should not set default values for each parameter > 0.0."""
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
    _attributes = relay.set_default_values(test_attributes_relay)

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


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_lambda_b(
    subcategory_id,
    type_id,
    environment_active_id,
    test_attributes_relay,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_relay["environment_active_id"] = environment_active_id
    test_attributes_relay["subcategory_id"] = subcategory_id
    test_attributes_relay["type_id"] = type_id
    _lambda_b = relay.get_part_count_lambda_b(test_attributes_relay)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert (
            _lambda_b
            == {
                1: {
                    1: [
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
                    ],
                    2: [
                        0.43,
                        0.89,
                        6.9,
                        3.6,
                        12.0,
                        3.4,
                        4.4,
                        6.2,
                        6.7,
                        22.0,
                        0.21,
                        11.0,
                        32.0,
                        0.0,
                    ],
                },
                2: {
                    1: [
                        0.40,
                        1.2,
                        4.8,
                        2.4,
                        6.8,
                        4.8,
                        7.6,
                        8.4,
                        13.0,
                        9.2,
                        0.16,
                        4.8,
                        13.0,
                        240.0,
                    ],
                    2: [
                        0.50,
                        1.5,
                        6.0,
                        3.0,
                        8.5,
                        5.0,
                        9.5,
                        11.0,
                        16.0,
                        12.0,
                        0.20,
                        5.0,
                        17.0,
                        300.0,
                    ],
                },
            }[subcategory_id][type_id][environment_active_id - 1]
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_relay,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_relay["subcategory_id"] = 13
    with pytest.raises(
        KeyError,
        match="get_part_count_lambda_b: Invalid relay subcategory ID 13 or type ID 3.",
    ):
        relay.get_part_count_lambda_b(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_lambda_b_invalid_type_id(
    test_attributes_relay,
):
    """Raises a KeyError when passed an invalid type ID."""
    test_attributes_relay["type_id"] = 11
    with pytest.raises(
        KeyError,
        match="get_part_count_lambda_b: Invalid relay subcategory ID 1 or type ID 11.",
    ):
        relay.get_part_count_lambda_b(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_relay,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_relay["environment_active_id"] = 21
    with pytest.raises(
        IndexError, match="get_part_count_lambda_b: Invalid relay environment ID 21."
    ):
        relay.get_part_count_lambda_b(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3])
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_relay,
):
    """Returns a float value for the quality factor (piQ) on success."""
    test_attributes_relay["quality_id"] = quality_id
    test_attributes_relay["subcategory_id"] = subcategory_id
    _pi_q = relay.get_part_count_quality_factor(test_attributes_relay)

    assert isinstance(_pi_q, float)
    assert (
        _pi_q
        == {
            1: [0.6, 3.0, 9.0],
            2: [0.0, 1.0, 4.0],
        }[
            subcategory_id
        ][quality_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_quality_factor_invalid_quality_id(
    test_attributes_relay,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_relay["quality_id"] = 5
    test_attributes_relay["subcategory_id"] = 1
    with pytest.raises(
        IndexError, match=r"get_part_count_quality_factor: Invalid relay quality ID 5."
    ):
        relay.get_part_count_quality_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_count_quality_factor_invalid_subcategory_id(
    test_attributes_relay,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_relay["quality_id"] = 1
    test_attributes_relay["subcategory_id"] = 5
    with pytest.raises(
        KeyError,
        match=r"get_part_count_quality_factor: Invalid relay subcategory ID 5.",
    ):
        relay.get_part_count_quality_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_relay")
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    type_id,
    test_attributes_relay,
):
    """Returns a float value for the part stress base hazard rate on success."""
    test_attributes_relay["subcategory_id"] = subcategory_id
    test_attributes_relay["temperature_active"] = 38.2
    test_attributes_relay["type_id"] = type_id
    _lambda_b = relay.calculate_part_stress_lambda_b(test_attributes_relay)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1:
        assert _lambda_b == pytest.approx([0.0064130981, 0.0061869201][type_id - 1])
    elif subcategory_id == 2:
        assert _lambda_b == [0.4, 0.5, 0.5][type_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_calculate_part_stress_lambda_b_invalid_type_id(
    test_attributes_relay,
):
    """Raises an IndexError when passed an invalid type ID."""
    test_attributes_relay["subcategory_id"] = 1
    test_attributes_relay["temperature_active"] = 38.2
    test_attributes_relay["type_id"] = 44
    with pytest.raises(
        IndexError, match=r"calculate_part_stress_lambda_b: Invalid relay type ID 44."
    ):
        relay.calculate_part_stress_lambda_b(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_calculate_part_stress_lambda_b_invalid_subcategory_id(
    test_attributes_relay,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_relay["subcategory_id"] = 12
    test_attributes_relay["temperature_active"] = 38.2
    test_attributes_relay["type_id"] = 1
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress_lambda_b: Invalid relay subcategory ID 12.",
    ):
        relay.calculate_part_stress_lambda_b(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_environment_factor(
    subcategory_id,
    quality_id,
    test_attributes_relay,
):
    """Returns a float value for the environment factor (piE) on success."""
    test_attributes_relay["environment_active_id"] = 1
    test_attributes_relay["quality_id"] = quality_id
    test_attributes_relay["subcategory_id"] = subcategory_id
    _pi_e = relay.get_environment_factor(test_attributes_relay)

    assert isinstance(_pi_e, float)
    if subcategory_id == 1:
        assert _pi_e == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0][quality_id - 1]
    elif subcategory_id == 2:
        assert _pi_e == 1.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_relay,
):
    """Raise an IndexError if passed an invalid active environment ID."""
    test_attributes_relay["environment_active_id"] = 21
    test_attributes_relay["quality_id"] = 1
    test_attributes_relay["subcategory_id"] = 1
    with pytest.raises(
        IndexError, match="get_environment_factor: Invalid relay environment ID 21."
    ):
        relay.get_environment_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_environment_factor_invalid_subcategory_id(
    test_attributes_relay,
):
    """Raises a KeyError if passed an invalid subcategory ID."""
    test_attributes_relay["environment_active_id"] = 1
    test_attributes_relay["quality_id"] = 1
    test_attributes_relay["subcategory_id"] = 12
    with pytest.raises(
        KeyError, match="get_environment_factor: Invalid relay subcategory ID 12."
    ):
        relay.get_environment_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_stress_quality_factor(
    quality_id,
    subcategory_id,
    test_attributes_relay,
):
    """Returns a float value for  part stress quality factor (piQ) on success."""
    if subcategory_id == 1 or (subcategory_id == 2 and quality_id in [1, 2]):
        test_attributes_relay["quality_id"] = quality_id
    test_attributes_relay["subcategory_id"] = subcategory_id
    _pi_q = relay.get_part_stress_quality_factor(test_attributes_relay)

    assert isinstance(_pi_q, float)
    if subcategory_id == 1:
        assert _pi_q == [0.1, 0.3, 0.45, 0.6, 1.0, 1.5, 3.0][quality_id - 1]
    elif subcategory_id == 2 and quality_id in [1, 2]:
        assert _pi_q == [1.0, 4.0][quality_id - 1]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_stress_quality_factor_invalid_quality_id(
    test_attributes_relay,
):
    """Raises an IndexError when passed an invalid quality ID."""
    test_attributes_relay["quality_id"] = 43
    test_attributes_relay["subcategory_id"] = 1
    with pytest.raises(
        IndexError,
        match=r"get_part_stress_quality_factor: Invalid relay quality ID 43.",
    ):
        relay.get_part_stress_quality_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_get_part_stress_quality_factor_invalid_subcategory_id(
    test_attributes_relay,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_relay["quality_id"] = 1
    test_attributes_relay["subcategory_id"] = 12
    with pytest.raises(
        KeyError,
        match=r"get_part_stress_quality_factor: Invalid relay subcategory ID 12.",
    ):
        relay.get_part_stress_quality_factor(test_attributes_relay)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3, 4, 5, 6, 7])
@pytest.mark.parametrize("n_cycles", [0.5, 100.0, 1103.4])
def test_calculate_cycling_factor(quality_id, n_cycles):
    """Returns a float value for piCYC on success or 0.0 if passed an invalid
    combination of arguments."""
    _pi_cyc = relay._calculate_cycling_factor(quality_id, n_cycles)

    assert isinstance(_pi_cyc, float)
    if quality_id in {1, 2, 3, 4, 5, 6} and n_cycles < 1.0:
        assert _pi_cyc == 0.1
    elif quality_id == 7 and n_cycles > 1000.0:
        assert _pi_cyc == pytest.approx(121.749156)
    elif quality_id == 7 and 10.0 < n_cycles < 1000.0:
        assert _pi_cyc == 10.0
    elif quality_id == 1 and n_cycles == 100.0:
        assert _pi_cyc == 0.0


@pytest.mark.unit
@pytest.mark.parametrize("technology_id", [1, 2, 3, 4])
def test_calculate_load_stress_factor(technology_id):
    """Returns a float value for piL on success."""
    _pi_l = relay._calculate_load_stress_factor(technology_id, 0.382)

    assert isinstance(_pi_l, float)
    assert _pi_l == pytest.approx(
        [
            0.22800625,
            0.912025,
            3.6481,
            0.0,
        ][technology_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 7])
def test_get_application_construction_factor(quality_id):
    """Returns a float value for piF on success."""
    _pi_f = relay._get_application_construction_factor(quality_id, 1, 1, 1)

    assert isinstance(_pi_f, float)
    assert _pi_f == {1: 4.0, 7: 8.0}[quality_id]


@pytest.mark.unit
def test_get_application_construction_factor_invalid_contact_rating_id():
    """Raises a KeyError if passed an invalid contact rating ID."""
    with pytest.raises(
        KeyError,
        match=r"_get_application_construction_factor: Invalid relay application ID 1, "
        r"contact rating ID 15, construction ID 1.",
    ):
        relay._get_application_construction_factor(1, 15, 1, 1)


@pytest.mark.unit
def test_get_application_construction_factor_invalid_construction_id():
    """Raises a KeyError if passed an invalid construction ID."""
    with pytest.raises(
        KeyError,
        match=r"_get_application_construction_factor: Invalid relay application ID 1, "
        r"contact rating ID 1, construction ID 15.",
    ):
        relay._get_application_construction_factor(1, 1, 15, 1)


@pytest.mark.unit
def test_get_application_construction_factor_invalid_application_id():
    """Raises a KeyError if passed an invalid application ID."""
    with pytest.raises(
        KeyError,
        match=r"_get_application_construction_factor: Invalid relay application ID 15, "
        r"contact rating ID 1, construction ID 1.",
    ):
        relay._get_application_construction_factor(1, 1, 1, 15)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_relay,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes_relay["hazard_rate_active"] = 0.0064130981
    test_attributes_relay["quality_id"] = 2
    test_attributes_relay["n_cycles"] = 0.5
    test_attributes_relay["subcategory_id"] = subcategory_id
    test_attributes_relay["type_id"] = 1
    _attributes = relay.calculate_part_stress(test_attributes_relay)

    assert isinstance(_attributes, dict)
    assert test_attributes_relay["piCYC"] == 0.1
    assert test_attributes_relay["piL"] == 0.9025
    assert test_attributes_relay["piF"] == 3.0

    if subcategory_id == 1:
        assert test_attributes_relay["piC"] == 1.0
        assert test_attributes_relay["hazard_rate_active"] == pytest.approx(0.001736346)
    else:
        assert test_attributes_relay["hazard_rate_active"] == pytest.approx(
            0.0064130981
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_relay")
def test_calculate_part_stress_missing_attribute_key(
    test_attributes_relay,
):
    """Raises a KeyError when a required attribute is missing."""
    test_attributes_relay.pop("n_cycles")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required relay attribute: "
        r"'n_cycles'.",
    ):
        relay.calculate_part_stress(test_attributes_relay)
