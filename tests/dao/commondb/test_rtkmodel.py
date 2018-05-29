# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkmodel.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKModel module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKModel import RTKModel

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
    """ __init__() should create an RTKModel model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKModel).first()

    assert isinstance(DUT, RTKModel)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_model'
    assert DUT.model_id == 1
    assert DUT.description == 'Adhesion Wear Model for Bearings'
    assert DUT.model_type == 'damage'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKModel).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKModel).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKModel {0:d} "
                    "attributes.".format(DUT.model_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKModel).first()

    ATTRIBUTES.pop('model_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'model_type' in attribute "
                    "dictionary passed to RTKModel.set_attributes().")

    ATTRIBUTES['model_type'] = 'damage'
