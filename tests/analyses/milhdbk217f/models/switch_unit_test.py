# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_switch.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the switch module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f.models import switch


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 5])
def test_get_part_count_lambda_b(subcategory_id):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
    _lambda_b = switch.get_part_count_lambda_b(subcategory_id, 3, 1)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.018, 5: 1.7}[subcategory_id]


@pytest.mark.unit
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    subcategory ID."""
    with pytest.raises(KeyError):
        switch.get_part_count_lambda_b(
            27,
            3,
            1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_construction():
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    construction ID."""
    with pytest.raises(KeyError):
        switch.get_part_count_lambda_b(
            5,
            3,
            -1,
        )


@pytest.mark.unit
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active
    environment ID."""
    with pytest.raises(IndexError):
        switch.get_part_count_lambda_b(
            2,
            33,
            1,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_count(
    test_attributes_switch,
):
    """calculate_part_count() should return a float value for the base hazard rate on
    success."""
    test_attributes_switch["subcategory_id"] = 1
    test_attributes_switch["environment_active_id"] = 3
    _lambda_b = switch.calculate_part_count(**test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.018


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 5, 31])
@pytest.mark.parametrize("construction_id", [1, 2])
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    construction_id,
):
    """calculate_part_stress_lambda_b() should return a float value for the part stress
    base hazard rate on success."""
    _lambda_b = switch.calculate_part_stress_lambda_b(
        subcategory_id,
        1,
        construction_id,
        1,
        8,
    )

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and construction_id == 1:
        assert _lambda_b == 0.00045
    elif subcategory_id == 1 and construction_id == 2:
        assert _lambda_b == 0.0027
    elif subcategory_id == 2 and construction_id == 1:
        assert _lambda_b == pytest.approx(0.1036)
    elif subcategory_id == 2 and construction_id == 2:
        assert _lambda_b == 0.1072
    elif subcategory_id == 4:
        assert _lambda_b == 0.5027
    elif subcategory_id == 5:
        assert _lambda_b == 0.02
    elif subcategory_id == 31:
        assert _lambda_b == 0.0


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_quality():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown
    quality ID."""
    with pytest.raises(IndexError):
        switch.calculate_part_stress_lambda_b(
            1,
            21,
            1,
            1,
            8,
        )


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_application():
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown
    application ID."""
    with pytest.raises(IndexError):
        switch.calculate_part_stress_lambda_b(
            5,
            1,
            1,
            21,
            8,
        )


@pytest.mark.unit
def test_calculate_part_stress_lambda_b_no_construction():
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown
    construction ID."""
    with pytest.raises(KeyError):
        switch.calculate_part_stress_lambda_b(
            1,
            1,
            41,
            1,
            8,
        )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
@pytest.mark.parametrize("subcategory_id", [1, 2, 5])
def test_calculate_part_stress(
    subcategory_id,
    test_attributes_switch,
):
    """calculate_part_stress() should return the switch attributes dict with updated
    values."""
    test_attributes_switch["subcategory_id"] = subcategory_id
    test_attributes_switch["construction_id"] = 1
    _attributes = switch.calculate_part_stress(**test_attributes_switch)

    assert isinstance(_attributes, dict)
    if subcategory_id == 1:
        assert _attributes["lambda_b"] == 0.00045
        assert _attributes["piCYC"] == 2.3
        assert _attributes["piL"] == pytest.approx(1.372187594)
        assert _attributes["piC"] == 1.7
        assert _attributes["hazard_rate_active"] == pytest.approx(0.004828728)
    elif subcategory_id == 2:
        assert _attributes["lambda_b"] == pytest.approx(0.10360)
        assert _attributes["piCYC"] == 2.3
        assert _attributes["piL"] == pytest.approx(1.372187594)
        assert _attributes["hazard_rate_active"] == pytest.approx(0.65392972)
    elif subcategory_id == 5:
        assert _attributes["lambda_b"] == 0.02
        assert _attributes["piC"] == 3.0
        assert _attributes["piU"] == 1.0
        assert _attributes["hazard_rate_active"] == pytest.approx(0.156)


@pytest.mark.unit
def test_calculate_load_stress_resistive():
    """calculate_load_stress() should return a float when calculating resistive load
    stress."""
    _pi_l = switch.calculate_load_stress_factor(1, 0.2)

    assert _pi_l == pytest.approx(1.064494459)


@pytest.mark.unit
def test_calculate_load_stress_inductive():
    """calculate_load_stress() should return a float when calculating inductive load
    stress."""
    _pi_l = switch.calculate_load_stress_factor(2, 0.2)

    assert _pi_l == pytest.approx(1.284025417)


@pytest.mark.unit
def test_calculate_load_stress_capacitive():
    """calculate_load_stress() should return a float when calculating capacitive load
    stress."""
    _pi_l = switch.calculate_load_stress_factor(3, 0.2)

    assert _pi_l == pytest.approx(2.718281828)


@pytest.mark.unit
def test_calculate_load_stress_nothing():
    """calculate_load_stress() should return 0.0 when calculating load stress for
    unknown load type."""
    _pi_l = switch.calculate_load_stress_factor(13, 0.2)

    assert _pi_l == 0.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_picyc_one(
    test_attributes_switch,
):
    """calculate_part_stress() should set piCYC=1.0 when n_cycles < 1.0."""
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["n_cycles"] = 0.05
    _attributes = switch.calculate_part_stress(**test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["piCYC"] == 1.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_base(
    test_attributes_switch,
):
    """calculate_part_stress() should return an active h(t)=0.0 for subcategories>5."""
    test_attributes_switch["piE"] = 6
    test_attributes_switch["subcategory_id"] = 6
    _attributes = switch.calculate_part_stress(**test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["hazard_rate_active"] == 0.0


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_construction_id(subcategory_id):
    """should return the default construction ID for the selected subcategory ID."""
    _construction_id = switch._set_default_construction_id(0, subcategory_id)

    assert (
        _construction_id
        == {
            1: 1,
            2: 1,
            3: 0,
            4: 0,
            5: 0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_contact_form_id(subcategory_id):
    """should return the default contact form ID for the selected subcategory ID."""
    _contact_form_id = switch._set_default_contact_form_id(0, subcategory_id)

    assert (
        _contact_form_id
        == {
            1: 2,
            2: 0,
            3: 0,
            4: 0,
            5: 3,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_cycle_rate(subcategory_id):
    """should return the default cycling rate for the selected subcategory ID."""
    _n_cycles = switch._set_default_cycle_rate(0.0, subcategory_id)

    assert (
        _n_cycles
        == {
            1: 1.0,
            2: 1.0,
            3: 30.0,
            4: 1.0,
            5: 0.0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [1, 2, 3, 4, 5],
)
def test_set_default_active_contacts(subcategory_id):
    """should return the default active contacts for the selected subcategory ID."""
    _n_elements = switch._set_default_active_contacts(0.0, subcategory_id)

    assert (
        _n_elements
        == {
            1: 0,
            2: 1,
            3: 24,
            4: 6,
            5: 0,
        }[subcategory_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_set_default_values(test_attributes_switch):
    """should set default values for each parameter <= 0.0."""
    test_attributes_switch["application_id"] = -1
    test_attributes_switch["construction_id"] = 0
    test_attributes_switch["contact_form_id"] = -2
    test_attributes_switch["current_ratio"] = -0.4
    test_attributes_switch["n_cycles"] = 0.0
    test_attributes_switch["n_elements"] = 0
    test_attributes_switch["quality_id"] = 0
    test_attributes_switch["subcategory_id"] = 2
    _attributes = switch.set_default_values(**test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 1
    assert _attributes["construction_id"] == 1
    assert _attributes["contact_form_id"] == 0
    assert _attributes["current_ratio"] == 0.5
    assert _attributes["n_cycles"] == 1.0
    assert _attributes["n_elements"] == 1
    assert _attributes["quality_id"] == 1


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_set_default_values_none_needed(test_attributes_switch):
    """should set default values for each parameter <= 0.0."""
    test_attributes_switch["application_id"] = 3
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["contact_form_id"] = 2
    test_attributes_switch["current_ratio"] = 0.4
    test_attributes_switch["n_cycles"] = 0.3
    test_attributes_switch["n_elements"] = 12
    test_attributes_switch["quality_id"] = 2
    test_attributes_switch["subcategory_id"] = 2
    _attributes = switch.set_default_values(**test_attributes_switch)

    assert isinstance(_attributes, dict)
    assert _attributes["application_id"] == 3
    assert _attributes["construction_id"] == 1
    assert _attributes["contact_form_id"] == 2
    assert _attributes["current_ratio"] == 0.4
    assert _attributes["n_cycles"] == 0.3
    assert _attributes["n_elements"] == 12
    assert _attributes["quality_id"] == 2
