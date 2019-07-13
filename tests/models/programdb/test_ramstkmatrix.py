# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkmatrix.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMatrix module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb.RAMSTKMatrix import RAMSTKMatrix

ATTRIBUTES = {
    'revision_id': 1,
    'matrix_id': 2,
    'column_id': 1,
    'column_item_id': 1,
    'matrix_type': 'rqrmnt_hrdwr',
    'parent_id': 0,
    'row_id': 1,
    'row_item_id': 1,
    'value': 0
}


@pytest.mark.integration
def test_ramstkmatrix_create(test_dao):
    """__init__() should create an RAMSTKMatrix model."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMatrix).first()

    assert isinstance(DUT, RAMSTKMatrix)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_matrix'
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
    """get_attributes() should return a tuple of attribute values."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMatrix).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """set_attributes() should return a zero error code on success."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMatrix).first()

    ATTRIBUTES.pop('revision_id')
    ATTRIBUTES.pop('matrix_id')
    ATTRIBUTES['value'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['value'] == 0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMatrix).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
