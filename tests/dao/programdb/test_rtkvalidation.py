#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkvalidation.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKValidation module algorithms and models."""

from datetime import date, timedelta

import pytest

from rtk.dao.programdb.RTKValidation import RTKValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'cost_minimum': 0.0,
    'validation_id': 1,
    'confidence': 95.0,
    'task_specification': u'',
    'date_start': date.today(),
    'acceptable_variance': 0.0,
    'task_type': u'',
    'measurement_unit': u'',
    'cost_average': 0.0,
    'date_end': date.today() + timedelta(days=30),
    'time_maximum': 0.0,
    'description': 'Test Validation',
    'time_variance': 0.0,
    'acceptable_minimum': 0.0,
    'cost_variance': 0.0,
    'time_minimum': 0.0,
    'acceptable_mean': 0.0,
    'time_mean': 0.0,
    'acceptable_maximum': 0.0,
    'status': 0.0,
    'cost_maximum': 0.0,
    'time_average': 0.0,
    'cost_mean': 0.0,
    'revision_id': 1,
    'cost_ll': 0.0,
    'cost_ul': 0.0,
    'time_ll': 0.0,
    'time_ul': 0.0,
    'name': ''
}


@pytest.mark.integration
def test_rtkvalidation_create(test_dao):
    """ __init__() should create an RTKValidation model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()

    assert isinstance(DUT, RTKValidation)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_validation'
    assert DUT.revision_id == 1
    assert DUT.validation_id == 1
    assert DUT.acceptable_maximum == 0.0
    assert DUT.acceptable_mean == 0.0
    assert DUT.acceptable_minimum == 0.0
    assert DUT.acceptable_variance == 0.0
    assert DUT.confidence == 95.0
    assert DUT.cost_average == 0.0
    assert DUT.cost_ll == 0.0
    assert DUT.cost_maximum == 0.0
    assert DUT.cost_mean == 0.0
    assert DUT.cost_minimum == 0.0
    assert DUT.cost_ul == 0.0
    assert DUT.cost_variance == 0.0
    assert DUT.date_end == date.today() + timedelta(days=30)
    assert DUT.date_start == date.today()
    assert DUT.description == 'Test Validation'
    assert DUT.measurement_unit == ''
    assert DUT.name == ''
    assert DUT.status == 0.0
    assert DUT.task_type == ''
    assert DUT.task_specification == ''
    assert DUT.time_average == 0.0
    assert DUT.time_ll == 0.0
    assert DUT.time_maximum == 0.0
    assert DUT.time_mean == 0.0
    assert DUT.time_minimum == 0.0
    assert DUT.time_ul == 0.0
    assert DUT.time_variance == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKValidation {0:d} "
                    "attributes.".format(DUT.validation_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()
    ATTRIBUTES.pop('status')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'status' in attribute "
                    "dictionary passed to RTKValidation.set_attributes().")

    ATTRIBUTES['status'] = 0.0


@pytest.mark.integration
def test_calculate_task_time(test_dao):
    """ calculate() returns False on successfully calculating tasks times. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()

    DUT.time_minimum = 25.2
    DUT.time_average = 36.8
    DUT.time_maximum = 44.1

    assert not DUT.calculate_task_time()
    assert DUT.time_ll == pytest.approx(29.90944678)
    assert DUT.time_mean == pytest.approx(36.08333333)
    assert DUT.time_ul == pytest.approx(42.2572199)
    assert DUT.time_variance == pytest.approx(9.9225)


@pytest.mark.integration
def test_calculate_task_cost(test_dao):
    """ calculate() returns False on successfully calculating tasks costs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKValidation).first()

    DUT.cost_minimum = 252.00
    DUT.cost_average = 368.00
    DUT.cost_maximum = 441.00
    DUT.confidence = 0.95

    assert not DUT.calculate_task_cost()
    assert DUT.cost_ll == pytest.approx(299.09446782)
    assert DUT.cost_mean == pytest.approx(360.83333333)
    assert DUT.cost_ul == pytest.approx(422.5721988)
    assert DUT.cost_variance == pytest.approx(992.25)
