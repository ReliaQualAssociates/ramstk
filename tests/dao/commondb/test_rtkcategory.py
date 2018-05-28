# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkcategory.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKCagtegory module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKCategory import RTKCategory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'category_type': u'hardware',
    'category_id': 1,
    'name': u'IC',
    'value': 1,
    'description': u'Integrated Circuit'
}


@pytest.mark.integration
def test_rtkcategory_create(test_common_dao):
    """ __init__() should create an RTKCategory model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCategory).first()

    assert isinstance(DUT, RTKCategory)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_category'
    assert DUT.category_id == 1
    assert DUT.name == 'IC'
    assert DUT.description == 'Integrated Circuit'
    assert DUT.cat_type == 'hardware'
    assert DUT.value == 1


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCategory).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCategory).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKCategory {0:d} "
                    "attributes.".format(DUT.category_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCategory).first()

    ATTRIBUTES.pop('category_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'category_type' in "
                    "attribute dictionary passed to "
                    "RTKCategory.set_attributes().")

    ATTRIBUTES['category_type'] = 'hardware'
