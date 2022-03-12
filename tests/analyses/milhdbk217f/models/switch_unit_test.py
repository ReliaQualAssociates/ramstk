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
@pytest.mark.usefixtures("test_attributes_switch")
@pytest.mark.parametrize("subcategory_id", [1, 5])
def test_get_part_count_lambda_b(
    subcategory_id,
    test_attributes_switch,
):
    """get_part_count_lambda_b() should return a float value for the base hazard rate
    on success."""
    test_attributes_switch["subcategory_id"] = subcategory_id
    test_attributes_switch["environment_active_id"] = 3
    test_attributes_switch["construction_id"] = 1
    _lambda_b = switch.get_part_count_lambda_b(test_attributes_switch)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == {1: 0.018, 5: 1.7}[subcategory_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_no_subcategory(
    test_attributes_switch,
):
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    subcategory ID."""
    test_attributes_switch["subcategory_id"] = 27
    with pytest.raises(KeyError):
        switch.get_part_count_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_no_construction(
    test_attributes_switch,
):
    """get_part_count_lambda_b() should raise a KeyError if passed an unknown
    construction ID."""
    test_attributes_switch["subcategory_id"] = 5
    test_attributes_switch["environment_active_id"] = 3
    test_attributes_switch["construction_id"] = -1
    with pytest.raises(KeyError):
        switch.get_part_count_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_get_part_count_lambda_b_no_environment(
    test_attributes_switch,
):
    """get_part_count_lambda_b() should raise an IndexError if passed an unknown active
    environment ID."""
    test_attributes_switch["subcategory_id"] = 2
    test_attributes_switch["environment_active_id"] = 33
    test_attributes_switch["construction_id"] = 1
    with pytest.raises(IndexError):
        switch.get_part_count_lambda_b(test_attributes_switch)


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
@pytest.mark.usefixtures("test_attributes_switch")
@pytest.mark.parametrize("subcategory_id", [1, 2, 4, 5, 31])
@pytest.mark.parametrize("construction_id", [1, 2])
def test_calculate_part_stress_lambda_b(
    subcategory_id,
    construction_id,
    test_attributes_switch,
):
    """calculate_part_stress_lambda_b() should return a float value for the part stress
    base hazard rate on success."""
    test_attributes_switch["subcategory_id"] = subcategory_id
    test_attributes_switch["quality_id"] = 1
    test_attributes_switch["construction_id"] = construction_id
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["n_elements"] = 8
    _attributes = switch.calculate_part_stress_lambda_b(test_attributes_switch)

    assert isinstance(_attributes["lambda_b"], float)
    if subcategory_id == 1 and construction_id == 1:
        assert _attributes["lambda_b"] == 0.00045
    elif subcategory_id == 1 and construction_id == 2:
        assert _attributes["lambda_b"] == 0.0027
    elif subcategory_id == 2 and construction_id == 1:
        assert _attributes["lambda_b"] == pytest.approx(0.1036)
    elif subcategory_id == 2 and construction_id == 2:
        assert _attributes["lambda_b"] == 0.1072
    elif subcategory_id == 4:
        assert _attributes["lambda_b"] == 0.5027
    elif subcategory_id == 5:
        assert _attributes["lambda_b"] == 0.02
    elif subcategory_id == 31:
        assert _attributes["lambda_b"] == 0.0


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_no_quality(
    test_attributes_switch,
):
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown
    quality ID."""
    test_attributes_switch["subcategory_id"] = 1
    test_attributes_switch["quality_id"] = 21
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["n_elements"] = 8
    with pytest.raises(IndexError):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_no_application(
    test_attributes_switch,
):
    """calculate_part_stress_lambda_b() should raise an IndexError if passed an unknown
    application ID."""
    test_attributes_switch["subcategory_id"] = 5
    test_attributes_switch["quality_id"] = 1
    test_attributes_switch["construction_id"] = 1
    test_attributes_switch["application_id"] = 21
    test_attributes_switch["n_elements"] = 8
    with pytest.raises(IndexError):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_part_stress_lambda_b_no_construction(
    test_attributes_switch,
):
    """calculate_part_stress_lambda_b() should raise a KeyError if passed an unknown
    construction ID."""
    test_attributes_switch["subcategory_id"] = 1
    test_attributes_switch["quality_id"] = 1
    test_attributes_switch["construction_id"] = 41
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["n_elements"] = 8
    with pytest.raises(KeyError):
        switch.calculate_part_stress_lambda_b(test_attributes_switch)


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
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_load_stress_resistive(
    test_attributes_switch,
):
    """calculate_load_stress() should return a float when calculating resistive load
    stress."""
    test_attributes_switch["application_id"] = 1
    test_attributes_switch["current_ratio"] = 0.2
    _attributes = switch.calculate_load_stress_factor(test_attributes_switch)

    assert _attributes["piL"] == pytest.approx(1.064494459)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_load_stress_inductive(
    test_attributes_switch,
):
    """calculate_load_stress() should return a float when calculating inductive load
    stress."""
    test_attributes_switch["application_id"] = 2
    test_attributes_switch["current_ratio"] = 0.2
    _attributes = switch.calculate_load_stress_factor(test_attributes_switch)

    assert _attributes["piL"] == pytest.approx(1.284025417)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_load_stress_capacitive(
    test_attributes_switch,
):
    """calculate_load_stress() should return a float when calculating capacitive load
    stress."""
    test_attributes_switch["application_id"] = 3
    test_attributes_switch["current_ratio"] = 0.2
    _attributes = switch.calculate_load_stress_factor(test_attributes_switch)

    assert _attributes["piL"] == pytest.approx(2.718281828)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_switch")
def test_calculate_load_stress_nothing(
    test_attributes_switch,
):
    """calculate_load_stress() should return 0.0 when calculating load stress for
    unknown load type."""
    test_attributes_switch["application_id"] = 13
    test_attributes_switch["current_ratio"] = 0.2
    _attributes = switch.calculate_load_stress_factor(test_attributes_switch)

    assert _attributes["piL"] == 0.0


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
