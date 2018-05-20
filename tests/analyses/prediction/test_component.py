#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_component.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for the component module."""

import pytest

from rtk.analyses.data import HARDWARE_ATTRIBUTES, DORMANT_MULT
from rtk.analyses.prediction import Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_calculate_mil_217f_part_count(category_id):
    """calculate() should return a dictionary of updated values on success when calculating 217F part count."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['environment_dormant_id'] = 3
    ATTRIBUTES['category_id'] = category_id

    if category_id == 10:
        for subcategory_id in [1, 2, 3, 4]:
            ATTRIBUTES['subcategory_id'] = subcategory_id
            _attributes, _msg = Component.calculate(**ATTRIBUTES)
    else:
        _attributes, _msg = Component.calculate(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if category_id < 9:
        assert _msg == ''


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_calculate_mil_217f_part_stress(category_id):
    """calculate() should return a dictionary of updated values on success when calculating 217F part stress."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['environment_dormant_id'] = 3
    ATTRIBUTES['category_id'] = category_id

    if category_id == 10:
        for subcategory_id in [1, 2, 3, 4]:
            ATTRIBUTES['subcategory_id'] = subcategory_id
            _attributes, _msg = Component.calculate(**ATTRIBUTES)
    else:
        _attributes, _msg = Component.calculate(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    if category_id < 9:
        assert _msg == ''


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
@pytest.mark.parametrize("category_id", [1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("subcategory_id", [1, 2, 3, 4, 5, 6, 7, 8, 9])
@pytest.mark.parametrize("environment_active_id",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
@pytest.mark.parametrize("environment_dormant_id", [1, 2, 3, 4])
def test_calculate_dormant_hazard_rate(category_id, subcategory_id,
                                       environment_active_id,
                                       environment_dormant_id):
    """calculate_dormant_hazard_rate() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_active'] = 1.005887691
    ATTRIBUTES['category_id'] = category_id
    ATTRIBUTES['subcategory_id'] = subcategory_id
    ATTRIBUTES['environment_active_id'] = environment_active_id
    ATTRIBUTES['environment_dormant_id'] = environment_dormant_id

    try:
        if category_id == 2:
            # [1, 2] = diodes, else transistors.
            if subcategory_id in [1, 2]:
                dormant_mult = (DORMANT_MULT[category_id][
                    environment_active_id][environment_dormant_id][0])
            elif subcategory_id in [3, 4, 5, 6, 7, 8, 9]:
                dormant_mult = (DORMANT_MULT[category_id][
                    environment_active_id][environment_dormant_id][1])
            else:
                dormant_mult = 0.0
        else:
            dormant_mult = DORMANT_MULT[category_id][environment_active_id][
                environment_dormant_id]
    except KeyError:
        dormant_mult = 0.0

    _attributes, _msg = Component.do_calculate_dormant_hazard_rate(
        **ATTRIBUTES)

    assert isinstance(_attributes, dict)
    try:
        assert _msg == ''
    except AssertionError:
        assert _msg == ("RTK ERROR: Unknown active and/or dormant environment "
                        "ID for hardware item.  Hardware ID: 6, active "
                        "environment ID: {0:d}, and dormant environment ID: "
                        "{1:d}.\n").format(environment_active_id,
                                           environment_dormant_id)

    assert _attributes['hazard_rate_dormant'] == (
        ATTRIBUTES['hazard_rate_active'] * dormant_mult)


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_zero_mult_adj():
    """calculate() should return an error message when the multiplicative adjustment factor is <= 0.0."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['environment_dormant_id'] = 3
    ATTRIBUTES['category_id'] = 1
    ATTRIBUTES['mult_adj_factor'] = 0.0

    _attributes, _msg = Component.calculate(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ("RTK WARNING: Multiplicative adjustment factor is 0.0 "
                    "when calculating hardware item, hardware ID: 6.\n")


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_zero_duty_cycle():
    """calculate() should return an error message when the duty cycle factor is <= 0.0."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['environment_dormant_id'] = 3
    ATTRIBUTES['category_id'] = 1
    ATTRIBUTES['mult_adj_factor'] = 1.0
    ATTRIBUTES['duty_cycle'] = 0.0

    _attributes, _msg = Component.calculate(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ("RTK WARNING: Duty cycle is 0.0 when calculating "
                    "hardware item, hardware ID: 6.\n")


@pytest.mark.unit
@pytest.mark.hardware
@pytest.mark.calculation
def test_calculate_zero_quantity():
    """calculate() should return an error message when the quantity is < 1."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['environment_dormant_id'] = 3
    ATTRIBUTES['category_id'] = 1
    ATTRIBUTES['mult_adj_factor'] = 1.0
    ATTRIBUTES['duty_cycle'] = 1.0
    ATTRIBUTES['quantity'] = 0

    _attributes, _msg = Component.calculate(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _msg == ("RTK WARNING: Quantity is less than 1 when calculating "
                    "hardware item, hardware ID: 6.\n")
