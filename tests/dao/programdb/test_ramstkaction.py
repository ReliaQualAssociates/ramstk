# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkaction.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKAction module algorithms and models."""

from datetime import date, timedelta

import pytest

from ramstk.dao.programdb.RAMSTKAction import RAMSTKAction

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'action_due_date': date.today() + timedelta(days=30),
    'action_approve_date': date.today() + timedelta(days=30),
    'action_status': '',
    'action_closed': 0,
    'action_taken': '',
    'action_close_date': date.today() + timedelta(days=30),
    'action_recommended': 'Recommended action for Failure Cause #1',
    'action_category': '',
    'action_owner': '',
    'cause_id': 1,
    'action_id': 1,
    'action_approved': 0
}


@pytest.mark.integration
def test_ramstkaction_create(test_dao):
    """
    __init__() should create an RAMSTKAction model.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKAction).first()

    assert isinstance(DUT, RAMSTKAction)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_action'
    assert DUT.cause_id == 1
    assert DUT.action_id == 1
    assert DUT.action_recommended == (
        'Test Functional FMEA Recommended Action #1 for Cause ID 1')
    assert DUT.action_category == ''
    assert DUT.action_owner == ''
    assert DUT.action_due_date == date.today() + timedelta(days=30)
    assert DUT.action_status == ''
    assert DUT.action_taken == ''
    assert DUT.action_approved == 0
    assert DUT.action_approve_date == date.today() + timedelta(days=30)
    assert DUT.action_closed == 0
    assert DUT.action_close_date == date.today() + timedelta(days=30)


@pytest.mark.integration
def test_get_attributes(test_dao):
    """
    get_attributes() should return a dict of attribute:value pairs.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKAction).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)


@pytest.mark.integration
def test_set_attributes(test_dao):
    """
    set_attributes() should return a zero error code on success.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKAction).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKAction {0:d} "
                    "attributes.".format(DUT.action_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """
    set_attributes() should return a 40 error code when passed a dict with a missing key.
    """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKAction).first()

    ATTRIBUTES.pop('action_taken')
    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'action_taken' in attribute "
                    "dictionary passed to RAMSTKAction.set_attributes().")

    ATTRIBUTES['action_taken'] = ''
