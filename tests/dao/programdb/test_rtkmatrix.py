# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkmatrix.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKMatrix module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKMatrix import RTKMatrix

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'matrix_id': 2,
    'column_id': 1,
    'column_item_id': 1,
    'matrix_type': 'rqrmnt_hrdwr',
    'parent_id': 0,
    'row_id': 1,
    'row_item_id': 1,
    'value': 0.0
}


@pytest.mark.integration
def test_rtkmatrix_create(test_dao):
    """ __init__() should create an RTKMatrix model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMatrix).first()

    assert isinstance(DUT, RTKMatrix)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_matrix'
    assert DUT.revision_id == 1
    assert DUT.matrix_id == 2
    assert DUT.column_id == 1
    assert DUT.column_item_id == 1
    assert DUT.matrix_type == 'rqrmnt_hrdwr'
    assert DUT.parent_id == 0
    assert DUT.row_id == 1
    assert DUT.row_item_id == 1
    assert DUT.value == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMatrix).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMatrix).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKMatrix {0:d} "
                    "attributes.".format(DUT.matrix_id))


@pytest.mark.integration
def test_set_attributes_mission_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMatrix).first()

    ATTRIBUTES.pop('matrix_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'matrix_type' in attribute "
                    "dictionary passed to RTKMatrix.set_attributes().")

    ATTRIBUTES['matrix_type'] = 'rqrmnt_hrdwr'
