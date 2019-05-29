#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.programdb.test_ramstktestmethod.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKTestMethod module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKTestMethod import RAMSTKTestMethod

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'remarks': '',
    'test_id': 1,
    'boundary_conditions': u'',
    'load_id': 1,
    'description': u'Test Test Method'
}


@pytest.mark.integration
def test_ramstkopstress_create(test_dao):
    """ __init__() should create an RAMSTKTestMethod model."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKTestMethod).first()

    assert isinstance(DUT, RAMSTKTestMethod)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_test_method'
    assert DUT.load_id == 1
    assert DUT.test_id == 1
    assert DUT.description == 'Test Test Method'
    assert DUT.boundary_conditions == ''
    assert DUT.remarks == ''


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKTestMethod).first()

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
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKTestMethod).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKTestMethod {0:d} "
                    "attributes.".format(DUT.load_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKTestMethod).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKTestMethod.set_attributes().")

    ATTRIBUTES['description'] = 'Test Test Method'
