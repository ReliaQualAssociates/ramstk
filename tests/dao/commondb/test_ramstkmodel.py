# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkmodel.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKModel module algorithms and models."""

import pytest

from rtk.dao.commondb.RAMSTKModel import RAMSTKModel

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'model_type': u'damage',
    'model_id': 1,
    'description': u'Adhesion Wear Model for Bearings'
}


@pytest.mark.integration
def test_rtkmodel_create(test_common_dao):
    """ __init__() should create an RAMSTKModel model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKModel).first()

    assert isinstance(DUT, RAMSTKModel)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_model'
    assert DUT.model_id == 1
    assert DUT.description == 'Adhesion Wear Model for Bearings'
    assert DUT.model_type == 'damage'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKModel).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKModel).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKModel {0:d} "
                    "attributes.".format(DUT.model_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKModel).first()

    ATTRIBUTES.pop('model_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'model_type' in attribute "
                    "dictionary passed to RAMSTKModel.set_attributes().")

    ATTRIBUTES['model_type'] = 'damage'
