# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkuser.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKUser module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKUser

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'user_id': 1,
    'user_lname': 'Tester',
    'user_fname': 'Johnny',
    'user_email': 'tester.johnny@reliaqual.com',
    'user_phone': '+1.269.867.5309',
    'user_group_id': '1'
}


@pytest.mark.integration
def test_ramstkuser_create(test_common_dao):
    """ __init__() should create an RAMSTKUser model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKUser).first()

    assert isinstance(DUT, RAMSTKUser)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_user'
    assert DUT.user_id == 1
    assert DUT.user_lname == 'Tester'
    assert DUT.user_fname == 'Johnny'
    assert DUT.user_email == 'tester.johnny@reliaqual.com'
    assert DUT.user_phone == '+1.269.867.5309'
    assert DUT.user_group_id == '1'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKUser).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKUser).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKUser {0:d} "
                    "attributes.".format(DUT.user_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKUser).first()

    ATTRIBUTES.pop('user_lname')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'user_lname' in attribute "
                    "dictionary passed to RAMSTKUser.set_attributes().")

    ATTRIBUTES['user_lname'] = 'Tester'
