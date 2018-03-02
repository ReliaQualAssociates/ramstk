# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkallocation.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKAllocation module algorithms and models."""

import pytest

from rtk.dao.RTKAllocation import RTKAllocation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'availability_alloc': 0.9998,
    'env_factor': 6,
    'goal_measure_id': 1,
    'hazard_rate_alloc': 0.0,
    'hazard_rate_goal': 0.0,
    'included': 1,
    'int_factor': 3,
    'method_id': 1,
    'mtbf_alloc': 0.0,
    'mtbf_goal': 0.0,
    'n_sub_systems': 3,
    'n_sub_elements': 3,
    'parent_id': 1,
    'percent_weight_factor': 0.8,
    'reliability_alloc': 0.99975,
    'reliability_goal': 0.999,
    'op_time_factor': 5,
    'soa_factor': 2,
    'weight_factor': 1
}


@pytest.mark.integration
@pytest.mark.hardware
def test_rtkallocation_create(test_dao):
    """__init__ should create an RTKAllocation model."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAllocation).first()

    assert isinstance(DUT, RTKAllocation)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_allocation'
    assert DUT.hardware_id == 1
    assert DUT.availability_alloc == 0.0
    assert DUT.env_factor == 1
    assert DUT.goal_measure_id == 1
    assert DUT.hazard_rate_alloc == 0.0
    assert DUT.hazard_rate_goal == 0.0
    assert DUT.included == 1
    assert DUT.int_factor == 1
    assert DUT.method_id == 1
    assert DUT.mtbf_alloc == 0.0
    assert DUT.mtbf_goal == 0.0
    assert DUT.n_sub_systems == 1
    assert DUT.n_sub_elements == 1
    assert DUT.parent_id == 0
    assert DUT.percent_weight_factor == 0.0
    assert DUT.reliability_alloc == 0.0
    assert DUT.reliability_goal == 1.0
    assert DUT.op_time_factor == 1
    assert DUT.soa_factor == 1
    assert DUT.weight_factor == 1


@pytest.mark.integration
@pytest.mark.hardware
def test_get_attributes(test_dao):
    """get_attributes() should return a dict of attribute values."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAllocation).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['hardware_id'] == 1
    assert _attributes['availability_alloc'] == 0.0
    assert _attributes['env_factor'] == 1
    assert _attributes['goal_measure_id'] == 1
    assert _attributes['hazard_rate_alloc'] == 0.0
    assert _attributes['hazard_rate_goal'] == 0.0
    assert _attributes['included'] == 1
    assert _attributes['int_factor'] == 1
    assert _attributes['method_id'] == 1
    assert _attributes['mtbf_alloc'] == 0.0
    assert _attributes['mtbf_goal'] == 0.0
    assert _attributes['n_sub_systems'] == 1
    assert _attributes['n_sub_elements'] == 1
    assert _attributes['parent_id'] == 0
    assert _attributes['percent_weight_factor'] == 0.0
    assert _attributes['reliability_alloc'] == 0.0
    assert _attributes['reliability_goal'] == 1.0
    assert _attributes['op_time_factor'] == 1
    assert _attributes['soa_factor'] == 1
    assert _attributes['weight_factor'] == 1


@pytest.mark.integration
@pytest.mark.hardware
def test_set_attributes(test_dao):
    """set_attributes() should return a zero error code on success."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAllocation).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKAllocation 1 attributes.")


@pytest.mark.integration
@pytest.mark.hardware
def test_set_attributes_too_few_passed(test_dao):
    """set_attributes() should return a 40 error code when passed a dict with missing attributes."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAllocation).first()

    _error_code, _msg = DUT.set_attributes({
        'availability_alloc': 0.9998,
        'goal_measure_id': 1,
        'hazard_rate_alloc': 0.0,
        'hazard_rate_goal': 0.0,
        'included': 1,
        'int_factor': 3,
        'method_id': 1,
        'mtbf_alloc': 0.0,
        'mtbf_goal': 0.0,
        'n_sub_systems': 3,
        'n_sub_elements': 3,
        'parent_id': 1,
        'percent_weight_factor': 0.8,
        'reliability_alloc': 0.99975,
        'reliability_goal': 0.999,
        'op_time_factor': 5,
        'soa_factor': 2,
        'weight_factor': 1
    })

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'env_factor' in attribute "
                    "dictionary passed to RTKAllocation.set_attributes().")
