# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtksiteinfo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RTKSiteInfo module algorithms and models."""

from datetime import date, timedelta

import pytest

from rtk.dao.commondb.RTKSiteInfo import RTKSiteInfo

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'site_id': 1,
    'product_key': '0000',
    'expire_on': date.today() + timedelta(30)
}


@pytest.mark.integration
def test_rtksiteinfo_create(test_common_dao):
    """ __init__() should create an RTKSiteInfo model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSiteInfo).first()

    assert isinstance(DUT, RTKSiteInfo)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_site_info'
    assert DUT.site_id == 1
    assert DUT.product_key == '0000'
    assert DUT.expire_on == date.today() + timedelta(30)


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSiteInfo).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSiteInfo).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKSiteInfo {0:d} "
                    "attributes.".format(DUT.site_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSiteInfo).first()

    ATTRIBUTES.pop('product_key')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'product_key' in attribute "
                    "dictionary passed to RTKSiteInfo.set_attributes().")

    ATTRIBUTES['product_key'] = '0000'
