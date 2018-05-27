# -*- coding: utf-8 -*-
#
#       tests.dao.progrmdb.test_rtkprogramstatus.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKProgramStatus module algorithms and models."""

from datetime import date

import pytest

from rtk.dao.programdb.RTKProgramStatus import RTKProgramStatus

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'cost_remaining': 0.0,
    'date_status': date.today(),
    'time_remaining': 0.0,
    'revision_id': 1,
    'status_id': 1
}


@pytest.mark.unit
def test_rtkprogramstatus_create(test_dao):
    """ __init__() should create an RTKProgramStatus model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramStatus).first()

    assert isinstance(DUT, RTKProgramStatus)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_program_status'
    assert DUT.revision_id == 1
    assert DUT.status_id == 1
    assert DUT.cost_remaining == 0.0
    assert DUT.date_status == date.today()
    assert DUT.time_remaining == 0.0


@pytest.mark.unit
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramStatus).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.unit
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramStatus).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKProgramStatus {0:d} "
                    "attributes.".format(DUT.revision_id))


@pytest.mark.unit
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramStatus).first()

    ATTRIBUTES.pop('time_remaining')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'time_remaining' in "
                    "attribute dictionary passed to "
                    "RTKProgramStatus.set_attributes().")

    ATTRIBUTES['time_remaining'] = 0.0
