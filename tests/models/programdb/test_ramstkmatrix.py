# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkmatrix.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMatrix module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMatrix

ATTRIBUTES = {
    'revision_id': 1,
    'matrix_id': 1,
    'column_id': 1,
    'column_item_id': 1,
    'matrix_type': 'fnctn_hrdwr',
    'parent_id': 0,
    'row_id': 1,
    'row_item_id': 1,
    'value': 0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMatrix():
    """Class for testing the RAMSTKMatrix model."""
    @pytest.mark.integration
    def test_ramstkmatrix_create(self, test_program_dao):
        """__init__() should create an RAMSTKMatrix model."""
        DUT = test_program_dao.session.query(RAMSTKMatrix).first()

        assert isinstance(DUT, RAMSTKMatrix)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_matrix'
        assert DUT.revision_id == 1
        assert DUT.matrix_id == 1
        assert DUT.column_id == 1
        assert DUT.column_item_id == 1
        assert DUT.matrix_type == 'fnctn_hrdwr'
        assert DUT.parent_id == 0
        assert DUT.row_id == 1
        assert DUT.row_item_id == 1
        assert DUT.value == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = test_program_dao.session.query(RAMSTKMatrix).first()

        assert DUT.get_attributes() == ATTRIBUTES

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = test_program_dao.session.query(RAMSTKMatrix).first()

        ATTRIBUTES.pop('revision_id')
        ATTRIBUTES.pop('matrix_id')
        ATTRIBUTES['value'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['value'] == 0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKMatrix).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
