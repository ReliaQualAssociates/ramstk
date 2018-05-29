# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkstatus.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKStatus module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKStatus import RTKStatus

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'description': u'Incident has been initiated.',
    'name': u'Initiated',
    'status_type': u'incident',
    'status_id': 1
}


@pytest.mark.integration
def test_rtkstatus_create(test_common_dao):
    """ __init__() should create an RTKStatus model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStatus).first()

    assert isinstance(DUT, RTKStatus)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_status'
    assert DUT.status_id == 1
    assert DUT.name == 'Initiated'
    assert DUT.description == 'Incident has been initiated.'
    assert DUT.status_type == 'incident'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStatus).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStatus).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKStatus {0:d} "
                    "attributes.".format(DUT.status_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStatus).first()

    ATTRIBUTES.pop('name')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'name' in attribute "
                    "dictionary passed to RTKStatus.set_attributes().")

    ATTRIBUTES['name'] = ''
