#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkopload.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKOpLoad module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKOpLoad import RAMSTKOpLoad

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'priority_id': 0,
    'damage_model': '',
    'load_id': 1,
    'mechanism_id': 1,
    'description': u'Test Operating Load'
}


@pytest.mark.integration
def test_ramstkopload_create(test_dao):
    """ __init__() should create an RAMSTKOpLoad model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpLoad).first()

    assert isinstance(DUT, RAMSTKOpLoad)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_op_load'
    assert DUT.mechanism_id == 1
    assert DUT.load_id == 1
    assert DUT.description == 'Test Operating Load'
    assert DUT.damage_model == ''
    assert DUT.priority_id == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpLoad).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['mechanism_id'] == 1
    assert _attributes['load_id'] == 1
    assert _attributes['description'] == 'Test Operating Load'
    assert _attributes['damage_model'] == ''
    assert _attributes['priority_id'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpLoad).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKOpLoad {0:d} "
                    "attributes.".format(DUT.load_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpLoad).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKOpLoad.set_attributes().")

    ATTRIBUTES['description'] = 'Test Operating Load'
