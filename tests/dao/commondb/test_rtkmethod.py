# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkmethod.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKMethod module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKMethod import RTKMethod

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'method_type': u'detection',
    'method_id': 1,
    'name': u'Code Reviews',
    'description': u''
}


@pytest.mark.integration
def test_rtkmethod_create(test_common_dao):
    """ __init__() should create an RTKMethod model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMethod).first()

    assert isinstance(DUT, RTKMethod)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_method'
    assert DUT.method_id == 1
    assert DUT.description == ''
    assert DUT.name == 'Code Reviews'
    assert DUT.method_type == 'detection'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a dict of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMethod).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMethod).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKMethod {0:d} "
                    "attributes.".format(DUT.method_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMethod).first()

    ATTRIBUTES.pop('method_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'method_type' in attribute "
                    "dictionary passed to RTKMethod.set_attributes().")

    ATTRIBUTES['method_type'] = 'test'
