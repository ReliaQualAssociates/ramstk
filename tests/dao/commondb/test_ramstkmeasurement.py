# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkmeasurement.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMeasurement module algorithms and models."""

import pytest

from rtk.dao.commondb.RAMSTKMeasurement import RAMSTKMeasurement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'measurement_id': 11,
    'code': 'CN',
    'description': 'Contamination, Concentration',
    'measurement_type': 'damage'
}


@pytest.mark.integration
def test_rtkmeasurement_create(test_common_dao):
    """ __init__() should create an RAMSTKMeasurement model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMeasurement).filter(
        RAMSTKMeasurement.measurement_type == 'damage').first()

    assert isinstance(DUT, RAMSTKMeasurement)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_measurement'
    assert DUT.measurement_id == 11
    assert DUT.code == 'CN'
    assert DUT.description == 'Contamination, Concentration'
    assert DUT.measurement_type == 'damage'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMeasurement).filter(
        RAMSTKMeasurement.measurement_type == 'damage').first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMeasurement).filter(
        RAMSTKMeasurement.measurement_type == 'damage').first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMeasurement {0:d} "
                    "attributes.".format(DUT.measurement_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMeasurement).filter(
        RAMSTKMeasurement.measurement_type == 'damage').first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKMeasurement.set_attributes().")

    ATTRIBUTES['description'] = 'Contamination, Concentration'
