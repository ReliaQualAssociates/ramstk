#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKManufacturer.py is part of The RAMSTK Project

#
# All rights reserved.
"""Test class for testing the RAMSTKManufacturer module algorithms and models."""

import pytest

from ramstk.dao.commondb.RAMSTKManufacturer import RAMSTKManufacturer

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'manufacturer_id': 1,
    'cage_code': '13606',
    'description': 'Sprague',
    'location': 'New Hampshire'
}


@pytest.mark.integration
def test_ramstkmanufacturer_create(test_common_dao):
    """ __init__() should create an RAMSTKManufacturer model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKManufacturer).first()

    assert isinstance(DUT, RAMSTKManufacturer)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_manufacturer'
    assert DUT.manufacturer_id == 1
    assert DUT.description == 'Sprague'
    assert DUT.location == 'New Hampshire'
    assert DUT.cage_code == '13606'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKManufacturer).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKManufacturer).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKManufacturer {0:d} "
                    "attributes.".format(DUT.manufacturer_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKManufacturer).first()

    ATTRIBUTES.pop('location')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'location' in attribute "
                    "dictionary passed to RAMSTKManufacturer.set_attributes().")
