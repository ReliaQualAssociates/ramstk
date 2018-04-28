#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkopload.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKOpLoad module algorithms and models."""

import pytest

from rtk.dao.RTKOpLoad import RTKOpLoad

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'priority_id': 0,
    'damage_model': 0,
    'load_id': 1,
    'mechanism_id': 1,
    'description': u'Test Operating Load'
}


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
@pytest.mark.pof
def test_rtkopload_create(test_dao):
    """ __init__() should create an RTKOpLoad model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpLoad).first()

    assert isinstance(DUT, RTKOpLoad)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_op_load'
    assert DUT.mechanism_id == 1
    assert DUT.load_id == 1
    assert DUT.description == 'Test Operating Load'
    assert DUT.damage_model == 0
    assert DUT.priority_id == 0


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
@pytest.mark.pof
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpLoad).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['mechanism_id'] == 1
    assert _attributes['load_id'] == 1
    assert _attributes['description'] == 'Test Operating Load'
    assert _attributes['damage_model'] == 0
    assert _attributes['priority_id'] == 0


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
@pytest.mark.pof
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpLoad).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKOpLoad {0:d} "
                    "attributes.".format(DUT.load_id))


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
@pytest.mark.pof
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKOpLoad).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RTKOpLoad.set_attributes().")

    ATTRIBUTES['description'] = 'Test Operating Load'
