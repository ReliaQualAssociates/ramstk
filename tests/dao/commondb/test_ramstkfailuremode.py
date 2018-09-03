# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.TestRAMSTKFailureMode.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKFailureMode module algorithms and models. """

import pytest

from rtk.dao.commondb.RAMSTKFailureMode import RAMSTKFailureMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'mode_id': 3,
    'description': u'Parameter Change',
    'subcategory_id': 24,
    'source': u'FMD-97',
    'category_id': 3,
    'mode_ratio': 0.2
}


@pytest.mark.integration
def test_rtkfailuremode_create(test_common_dao):
    """ __init__() should create an RAMSTKFailureMode model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureMode).first()

    assert isinstance(DUT, RAMSTKFailureMode)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_failure_mode'
    assert DUT.category_id == 3
    assert DUT.subcategory_id == 24
    assert DUT.mode_id == 3
    assert DUT.description == 'Parameter Change'
    assert DUT.mode_ratio == 0.2
    assert DUT.source == 'FMD-97'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureMode).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureMode).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKFailureMode {0:d} "
                    "attributes.".format(DUT.mode_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureMode).first()

    ATTRIBUTES.pop('mode_ratio')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'mode_ratio' in attribute "
                    "dictionary passed to RAMSTKFailureMode.set_attributes().")

    ATTRIBUTES['mode_ratio'] = 0.2
