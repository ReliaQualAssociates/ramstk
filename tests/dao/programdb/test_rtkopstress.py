#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.programdb.test_rtkopstress.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKOpStress module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKOpStress import RTKOpStress

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'description': u'Test Operating Stress',
    'load_id': 1,
    'load_history': '',
    'measurable_parameter': '',
    'remarks': '',
    'stress_id': 1
}


@pytest.mark.integration
def test_rtkopstress_create(test_dao):
    """ __init__() should create an RTKOpStress model."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpStress).first()

    assert isinstance(DUT, RTKOpStress)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_op_stress'
    assert DUT.load_id == 1
    assert DUT.stress_id == 1
    assert DUT.description == 'Test Operating Stress'
    assert DUT.measurable_parameter == ''
    assert DUT.load_history == ''
    assert DUT.remarks == ''


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpStress).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['load_id'] == 1
    assert _attributes['stress_id'] == 1
    assert _attributes['description'] == 'Test Operating Stress'
    assert _attributes['load_history'] == ''
    assert _attributes['measurable_parameter'] == ''
    assert _attributes['remarks'] == ''


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpStress).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKOpStress {0:d} "
                    "attributes.".format(DUT.stress_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpStress).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RTKOpStress.set_attributes().")

    ATTRIBUTES['description'] = 'Test Operating Stress'
