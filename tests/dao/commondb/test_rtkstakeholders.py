# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkstakeholders.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKStakeholders module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKStakeholders import RTKStakeholders

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {'stakeholders_id': 1, 'stakeholder': 'Customer'}


@pytest.mark.integration
def test_rtkstakeholders_create(test_common_dao):
    """ __init__() should create an RTKStakeholders model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholders).first()

    assert isinstance(DUT, RTKStakeholders)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_stakeholders'
    assert DUT.stakeholders_id == 1
    assert DUT.stakeholder == 'Customer'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholders).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholders).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKStakeholders {0:d} "
                    "attributes.".format(DUT.stakeholders_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholders).first()

    ATTRIBUTES.pop('stakeholder')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'stakeholder' in attribute "
                    "dictionary passed to RTKStakeholders.set_attributes().")

    ATTRIBUTES['stakeholder'] = 'Customer'
