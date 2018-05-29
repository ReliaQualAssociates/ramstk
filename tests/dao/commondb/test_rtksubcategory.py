# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtksubcategory.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKSubCategory module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKSubCategory import RTKSubCategory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {'category_id': 1, 'subcategory_id': 1, 'description': 'Linear'}


@pytest.mark.integration
def test_rtksubcategory_create(test_common_dao):
    """ __init__() should create an RTKSubCategory model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSubCategory).first()

    assert isinstance(DUT, RTKSubCategory)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_subcategory'
    assert DUT.category_id == 1
    assert DUT.subcategory_id == 1
    assert DUT.description == 'Linear'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSubCategory).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSubCategory).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKSubCategory {0:d} "
                    "attributes.".format(DUT.subcategory_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSubCategory).first()

    ATTRIBUTES.pop('category_id')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'category_id' in attribute "
                    "dictionary passed to RTKSubCategory.set_attributes().")

    ATTRIBUTES['category_id'] = 1
