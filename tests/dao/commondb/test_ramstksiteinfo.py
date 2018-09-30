# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstksiteinfo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKSiteInfo module algorithms and models."""

from datetime import date, timedelta

import pytest

from ramstk.dao.commondb.RAMSTKSiteInfo import RAMSTKSiteInfo

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'site_id': 1,
    'product_key': '0000',
    'expire_on': date.today() + timedelta(30),
    'function_enabled': 0,
    'requirement_enabled': 0,
    'hardware_enabled': 0,
    'vandv_enabled': 0,
    'fmea_enabled': 0
}


@pytest.mark.integration
def test_ramstksiteinfo_create(test_common_dao):
    """ __init__() should create an RAMSTKSiteInfo model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSiteInfo).first()

    assert isinstance(DUT, RAMSTKSiteInfo)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_site_info'
    assert DUT.site_id == 1
    assert DUT.product_key == '0000'
    assert DUT.expire_on == date.today() + timedelta(30)


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSiteInfo).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSiteInfo).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKSiteInfo attributes.")


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSiteInfo).first()

    ATTRIBUTES.pop('product_key')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'product_key' in attribute "
                    "dictionary passed to RAMSTKSiteInfo.set_attributes().")

    ATTRIBUTES['product_key'] = '0000'
