#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkenvironment.py is part of The RAMSTK Project
#
# All rights reserved.
""" Test class for testing the RAMSTKEnvironment module algorithms and models. """

import pytest

from rtk.dao.programdb.RAMSTKEnvironment import RAMSTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'environment_id': 1,
    'low_dwell_time': 0.0,
    'minimum': 0.0,
    'ramp_rate': 0.0,
    'high_dwell_time': 0.0,
    'name': 'Condition Name',
    'maximum': 0.0,
    'units': u'Units',
    'variance': 0.0,
    'phase_id': 1,
    'mean': 0.0
}


@pytest.mark.integration
def test_rtkenvironment_create(test_dao):
    """ __init__() should create an RAMSTKEnvironment model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKEnvironment).first()

    assert isinstance(DUT, RAMSTKEnvironment)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_environment'
    assert DUT.phase_id == 1
    assert DUT.environment_id == 1
    assert DUT.name == 'Condition Name'
    assert DUT.units == 'Units'
    assert DUT.minimum == 0.0
    assert DUT.maximum == 0.0
    assert DUT.mean == 0.0
    assert DUT.variance == 0.0
    assert DUT.ramp_rate == 0.0
    assert DUT.low_dwell_time == 0.0
    assert DUT.high_dwell_time == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKEnvironment).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKEnvironment).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKEnvironment {0:d} "
                    "attributes.".format(DUT.environment_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 10 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKEnvironment).first()

    ATTRIBUTES.pop('variance')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'variance' in attribute "
                    "dictionary passed to RAMSTKEnvironment.set_attributes().")
