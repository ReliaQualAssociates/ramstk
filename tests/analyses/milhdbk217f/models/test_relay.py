# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_relay.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the relay module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import relay

ATTRIBUTES = {
    'category_id': 6,
    'subcategory_id': 1,
    'environment_active_id': 3,
    'quality_id': 1,
    'type_id': 3,
    'technology_id': 2,
    'current_ratio': 0.38,
    'contact_rating_id': 2,
    'construction_id': 1,
    'application_id': 1,
    'contact_form_id': 1,
    'temperature_active': 38.2,
    'n_cycles': 58,
    'piQ': 1.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_get_part_count_lambda_b(subcategory_id, type_id,
                                 environment_active_id):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = relay.get_part_count_lambda_b(
        subcategory_id=subcategory_id,
        type_id=type_id,
        environment_active_id=environment_active_id)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert _lambda_b == [
            0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5,
            10.0, 0.0
        ][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_subcategory():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _lambda_b = relay.get_part_count_lambda_b(subcategory_id=1.3,
                                                  type_id=1,
                                                  environment_active_id=2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_type():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _lambda_b = relay.get_part_count_lambda_b(subcategory_id=1,
                                                  type_id=11,
                                                  environment_active_id=2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _lambda_b = relay.get_part_count_lambda_b(subcategory_id=1,
                                                  type_id=1,
                                                  environment_active_id=21)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count():
    """calculate_part_count() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = relay.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 2.1


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("quality_id", [1, 7])
@pytest.mark.parametrize("n_cycles", [0.5, 100.0, 1103.4])
def test_calculate_cycling_factor(quality_id, n_cycles):
    """calculate_cycling_factor() should return a float value for piCYC on success or 0.0 if passed an unknown combination of arguments."""
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
@pytest.mark.calculation
@pytest.mark.parametrize("technology_id", [1, 2, 3, 4])
def test_calculate_load_stress_factor(technology_id):
    """calculate_load_stress_factor() should return a float value for piL on success."""
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
@pytest.mark.calculation
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
@pytest.mark.calculation
def test_get_environment_factor_no_subcategory():
    """get_environment_factor() should raise a KeyError if passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _pi_e = relay.get_environment_factor(12, 1, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_environment_factor_no_environment():
    """get_environment_factor() should raise an IndexError if passed an unknown active environment ID."""
    with pytest.raises(IndexError):
        _pi_e = relay.get_environment_factor(1, 1, 21)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("quality_id", [1, 7])
def test_get_application_construction_factor(quality_id):
    """get_application_construction_factor() should return a float value for piF on success."""
    _pi_f = relay.get_application_construction_factor(quality_id, 1, 1, 1)

    assert isinstance(_pi_f, float)
    assert _pi_f == {1: 4.0, 7: 8.0}[quality_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_construction_factor_no_contact_rating():
    """get_application_construction_factor() should raise a KeyError if passed an unknown contact rating ID."""
    with pytest.raises(KeyError):
        _pi_f = relay.get_application_construction_factor(1, 15, 1, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_construction_factor_no_construction():
    """get_application_construction_factor() should raise a KeyError if passed an unknown construction ID."""
    with pytest.raises(KeyError):
        _pi_f = relay.get_application_construction_factor(1, 1, 15, 1)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_construction_factor_no_application():
    """get_application_construction_factor() should raise a KeyError if passed an unknown application ID."""
    with pytest.raises(KeyError):
        _pi_f = relay.get_application_construction_factor(1, 1, 1, 15)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
@pytest.mark.parametrize("type_id", [1, 2])
def test_calculate_part_stress_lambda_b(subcategory_id, type_id):
    """calculate_part_stress_lambda_b() should return a float value for the base hazard rate on success."""
    _lambda_b = relay.calculate_part_stress_lambda_b(subcategory_id, type_id,
                                                     38.2)

    assert isinstance(_lambda_b, float)
    if subcategory_id == 1 and type_id == 1:
        assert _lambda_b == pytest.approx(0.0064130981)
    elif subcategory_id == 1 and type_id == 2:
        assert _lambda_b == pytest.approx(0.0061869201)
    elif subcategory_id == 2:
        assert _lambda_b == [0.4, 0.5, 0.5][type_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2])
def test_calculate_part_stress(subcategory_id):
    """calculate_part_stress() should return the attributes with updated values on success."""
    ATTRIBUTES['type_id'] = 1
    ATTRIBUTES['subcategory_id'] = subcategory_id
    _attributes = relay.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
