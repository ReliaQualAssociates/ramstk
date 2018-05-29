# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkhazards.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKHazard module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKHazards import RTKHazards

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'category': u'Acceleration/Gravity',
    'hazard_id': 1,
    'subcategory': u'Falls'
}


@pytest.mark.integration
def test_rtkhazards_create(test_common_dao):
    """ __init__() should create an RTKHazard model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKHazards).first()

    assert isinstance(DUT, RTKHazards)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_hazards'
    assert DUT.hazard_id == 1
    assert DUT.category == 'Acceleration/Gravity'
    assert DUT.subcategory == 'Falls'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKHazards).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKHazards).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKHazard {0:d} "
                    "attributes.".format(DUT.hazard_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKHazards).first()

    ATTRIBUTES.pop('category')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'category' in attribute "
                    "dictionary passed to RTKHazards.set_attributes().")
