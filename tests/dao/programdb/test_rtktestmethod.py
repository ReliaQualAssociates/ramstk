#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.programdb.test_rtktestmethod.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKTestMethod module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKTestMethod import RTKTestMethod

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'remarks': '',
    'test_id': 1,
    'boundary_conditions': u'',
    'load_id': 1,
    'description': u'Test Test Method'
}


@pytest.mark.integration
def test_rtkopstress_create(test_dao):
    """ __init__() should create an RTKTestMethod model."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKTestMethod).first()

    assert isinstance(DUT, RTKTestMethod)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_test_method'
    assert DUT.load_id == 1
    assert DUT.test_id == 1
    assert DUT.description == 'Test Test Method'
    assert DUT.boundary_conditions == ''
    assert DUT.remarks == ''


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKTestMethod).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['load_id'] == 1
    assert _attributes['test_id'] == 1
    assert _attributes['description'] == 'Test Test Method'
    assert _attributes['boundary_conditions'] == ''
    assert _attributes['remarks'] == ''


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKTestMethod).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKTestMethod {0:d} "
                    "attributes.".format(DUT.load_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKTestMethod).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RTKTestMethod.set_attributes().")

    ATTRIBUTES['description'] = 'Test Test Method'
