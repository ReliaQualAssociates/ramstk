# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkmethod.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMethod module algorithms and models."""

import pytest

from ramstk.dao.commondb.RAMSTKMethod import RAMSTKMethod

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'method_type': u'detection',
    'method_id': 1,
    'name': u'Code Reviews',
    'description': u''
}


@pytest.mark.integration
def test_ramstkmethod_create(test_common_dao):
    """ __init__() should create an RAMSTKMethod model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMethod).first()

    assert isinstance(DUT, RAMSTKMethod)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_method'
    assert DUT.method_id == 1
    assert DUT.description == ''
    assert DUT.name == 'Code Reviews'
    assert DUT.method_type == 'detection'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a dict of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMethod).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMethod).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMethod {0:d} "
                    "attributes.".format(DUT.method_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMethod).first()

    ATTRIBUTES.pop('method_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'method_type' in attribute "
                    "dictionary passed to RAMSTKMethod.set_attributes().")

    ATTRIBUTES['method_type'] = 'test'
