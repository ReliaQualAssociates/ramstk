# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkaction.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKAction module algorithms and models."""

from datetime import date, timedelta

import pytest

from rtk.dao.RTKAction import RTKAction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

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
def test_rtkaction_create(test_dao):
    """
    __init__() should create an RTKAction model.
    """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAction).first()

    assert isinstance(DUT, RTKAction)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_action'
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
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAction).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)


@pytest.mark.integration
def test_set_attributes(test_dao):
    """
    set_attributes() should return a zero error code on success.
    """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAction).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKAction {0:d} "
                    "attributes.".format(DUT.action_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """
    set_attributes() should return a 40 error code when passed a dict with a missing key.
    """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKAction).first()

    ATTRIBUTES.pop('action_taken')
    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'action_taken' in attribute "
                    "dictionary passed to RTKAction.set_attributes().")

    ATTRIBUTES['action_taken'] = ''
