# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtktype.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKType module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKType import RTKType

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


ATTRIBUTES = {'type_id':1, 'code':'Type Code', 'description':'PLN', 'type_type':'unknown'}


@pytest.mark.integration
def test_rtktype_create(test_common_dao):
    """ __init__() should create an RTKType model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKType).first()

    assert isinstance(DUT, RTKType)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_type'
    assert DUT.type_id == 1
    assert DUT.code == 'Type Code'
    assert DUT.description == 'PLN'
    assert DUT.type_type == 'unknown'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKType).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKType).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKType {0:d} "
                               "attributes.".format(DUT.type_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKType).first()

    ATTRIBUTES.pop('code')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'code' in attribute "
                    "dictionary passed to RTKType.set_attributes().")

    ATTRIBUTES['code'] = 'CALC'
