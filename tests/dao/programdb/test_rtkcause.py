#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkcause.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKCause module algorithms and models. """

import pytest

from rtk.Utilities import OutOfRangeError
from rtk.dao.programdb.RTKCause import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 0,
    'cause_id': 1,
    'description': 'Test Failure Cause #1',
    'rpn_occurrence': 0,
    'rpn_detection_new': 0,
    'rpn_detection': 0,
    'mechanism_id': 1,
    'mode_id': 1,
    'rpn': 0
}


@pytest.mark.integration
def test_rtkcause_create(test_dao):
    """ __init__() should create an RTKCause model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    assert isinstance(DUT, RTKCause)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_cause'
    assert DUT.mode_id == 1
    assert DUT.cause_id == 1
    assert DUT.description == 'Test Functional FMEA Cause #1 for Mode ID 1'
    assert DUT.rpn == 0
    assert DUT.rpn_detection == 0
    assert DUT.rpn_detection_new == 0
    assert DUT.rpn_new == 0
    assert DUT.rpn_occurrence == 0
    assert DUT.rpn_occurrence_new == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)
    assert _attributes['mode_id'] == 1
    assert _attributes['mechanism_id'] == -1
    assert _attributes['cause_id'] == 1
    assert _attributes['description'] == ('Test Functional FMEA Cause #1 for '
                                          'Mode ID 1')
    assert _attributes['rpn'] == 0
    assert _attributes['rpn_detection'] == 0
    assert _attributes['rpn_detection_new'] == 0
    assert _attributes['rpn_new'] == 0
    assert _attributes['rpn_occurrence'] == 0
    assert _attributes['rpn_occurrence_new'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKCause {0:d} "
                    "attributes.".format(DUT.cause_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RTKCause.set_attributes().")

    ATTRIBUTES['description'] = 'Test Failure Cause #1'


@pytest.mark.integration
def test_calculate_rpn_out_of_range_severity_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < severity inputs < 0. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 0, 1)
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 11, 1)
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 0)
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 11)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_occurrence_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < occurrence inputs < 0. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    DUT.rpn_occurrence = 0
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 1)
    DUT.rpn_occurrence = 11
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 1)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_new_occurrence_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < new occurrence inputs < 0. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    DUT.rpn_occurrence_new = 0
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 1)
    DUT.rpn_occurrence_new = 11
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 1)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_detection_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < detection inputs < 0. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    DUT.rpn_detection = 0
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 10)
    DUT.rpn_detection = 11
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 10)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_new_detection_inputs(test_dao):
    """ calculate_rpn raises OutOfRangeError for 11 < new detection inputs < 0. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCause).first()

    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 10)
    DUT.rpn_detection_new = 11
    pytest.raises(OutOfRangeError, DUT.calculate_rpn, 1, 10)
