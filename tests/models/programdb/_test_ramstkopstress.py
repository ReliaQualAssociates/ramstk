#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.programdb.test_ramstkopstress.py is part of The RAMSTK Project

#
# All rights reserved.
"""Test class for testing the RAMSTKOpStress module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.dao.programdb.RAMSTKOpStress import RAMSTKOpStress

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'description': 'Test Operating Stress',
    'load_id': 1,
    'load_history': '',
    'measurable_parameter': '',
    'remarks': b'',
    'stress_id': 1
}


@pytest.mark.integration
def test_ramstkopstress_create(test_dao):
    """ __init__() should create an RAMSTKOpStress model."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpStress).first()

    assert isinstance(DUT, RAMSTKOpStress)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_op_stress'
    assert DUT.load_id == 1
    assert DUT.stress_id == 1
    assert DUT.description == 'Test Operating Stress'
    assert DUT.measurable_parameter == ''
    assert DUT.load_history == ''
    assert DUT.remarks == b''


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpStress).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['load_id'] == 1
    assert _attributes['stress_id'] == 1
    assert _attributes['description'] == 'Test Operating Stress'
    assert _attributes['load_history'] == ''
    assert _attributes['measurable_parameter'] == ''
    assert _attributes['remarks'] == b''


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpStress).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKOpStress {0:d} "
                    "attributes.".format(DUT.stress_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKOpStress).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKOpStress.set_attributes().")

    ATTRIBUTES['description'] = 'Test Operating Stress'
