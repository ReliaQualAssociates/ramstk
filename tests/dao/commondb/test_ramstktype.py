# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstktype.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKType module algorithms and models."""

import pytest

from ramstk.dao.commondb.RAMSTKType import RAMSTKType

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'type_id': 1,
    'code': 'PLN',
    'description': 'Planning',
    'type_type': 'incident'
}


@pytest.mark.integration
def test_ramstktype_create(test_common_dao):
    """ __init__() should create an RAMSTKType model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKType).first()

    assert isinstance(DUT, RAMSTKType)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_type'
    assert DUT.type_id == 1
    assert DUT.code == 'PLN'
    assert DUT.description == 'Planning'
    assert DUT.type_type == 'incident'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKType).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKType).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKType {0:d} "
                    "attributes.".format(DUT.type_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKType).first()

    ATTRIBUTES.pop('code')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'code' in attribute "
                    "dictionary passed to RAMSTKType.set_attributes().")

    ATTRIBUTES['code'] = 'CALC'
