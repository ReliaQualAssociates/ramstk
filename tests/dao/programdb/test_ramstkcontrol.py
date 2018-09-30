# -*- coding: utf-8 -*-
#
#       tests._dao.programdb.test_ramstkcontrol.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKControl module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKControl import RAMSTKControl

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'cause_id': 1,
    'description': 'Test Control',
    'control_id': 1,
    'type_id': 'Detection'
}


@pytest.mark.integration
def test_ramstkcontrol_create(test_dao):
    """
    __init__() should create an RAMSTKControl model.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKControl).first()

    assert isinstance(DUT, RAMSTKControl)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_control'
    assert DUT.cause_id == 1
    assert DUT.control_id == 1
    assert DUT.description == 'Test Functional FMEA Control #1 for Cause ID 1'
    assert DUT.type_id == ''


@pytest.mark.integration
def test_get_attributes(test_dao):
    """
    get_attributes() should return a dictionary of attribute key:value pairs.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKControl).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['cause_id'] == 1
    assert _attributes['control_id'] == 1
    assert _attributes['description'] == ('Test Functional FMEA Control #1 '
                                          'for Cause ID 1')
    assert _attributes['type_id'] == ''


@pytest.mark.integration
def test_set_attributes(test_dao):
    """
    set_attributes() should return a zero error code on success
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKControl).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == "RAMSTK SUCCESS: Updating RAMSTKControl 1 attributes."


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """
    set_attributes() should return a 40 error code when passed a dict with a missing key.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKControl).first()

    ATTRIBUTES.pop('type_id')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'type_id' in attribute "
                    "dictionary passed to RAMSTKControl.set_attributes().")

    ATTRIBUTES['type_id'] = ''
