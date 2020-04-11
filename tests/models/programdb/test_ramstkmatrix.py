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
    'column_id': 8,
    'column_item_id': 8,
    'matrix_type': 'fnctn_hrdwr',
    'parent_id': 0,
    'row_id': 8,
    'row_item_id': 3,
    'value': 0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMatrix():
    """Class for testing the RAMSTKMatrix model."""
    @pytest.mark.integration
    def test_ramstkmatrix_create(self, test_program_dao):
        """__init__() should create an RAMSTKMatrix model."""
        # Select the last row returned since the first row is deleted by
        # function module tests.  This would cause a problem when the test
        # suite is run.
        DUT = test_program_dao.do_select_all(RAMSTKMatrix,
                                             key=[RAMSTKMatrix.revision_id,
                                                  RAMSTKMatrix.matrix_type],
                                             value=[1, 'fnctn_hrdwr'],
                                             order=RAMSTKMatrix.row_id,
                                             _all=True)[-1]

        assert isinstance(DUT, RAMSTKMatrix)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_matrix'
        assert DUT.revision_id == 1
        assert DUT.matrix_id == 1
        assert DUT.column_id == 8
        assert DUT.matrix_type == 'fnctn_hrdwr'
        assert DUT.parent_id == 0
        assert DUT.row_id == 8
        assert DUT.value == 0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        # Select the last row returned since the first row is deleted by
        # function module tests.  This would cause a problem when the test
        # suite is run.
        DUT = test_program_dao.do_select_all(RAMSTKMatrix,
                                             key=[RAMSTKMatrix.revision_id,
                                                  RAMSTKMatrix.matrix_type],
                                             value=[1, 'fnctn_hrdwr'],
                                             order=RAMSTKMatrix.row_id,
                                             _all=True)[-1]

        _attributes = DUT.get_attributes()

        assert _attributes['column_id'] == 8
        assert _attributes['matrix_type'] == 'fnctn_hrdwr'
        assert _attributes['parent_id'] == 0
        assert _attributes['row_id'] == 8
        assert _attributes['value'] == 0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """set_attributes() should return a zero error code on success."""
        # Select the last row returned since the first row is deleted by
        # function module tests.  This would cause a problem when the test
        # suite is run.
        DUT = test_program_dao.do_select_all(RAMSTKMatrix,
                                             key=[RAMSTKMatrix.revision_id,
                                                  RAMSTKMatrix.matrix_type],
                                             value=[1, 'fnctn_hrdwr'],
                                             order=RAMSTKMatrix.row_id,
                                             _all=True)[-1]

        ATTRIBUTES.pop('revision_id')
        ATTRIBUTES.pop('matrix_id')
        ATTRIBUTES['value'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['value'] == 0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        # Select the last row returned since the first row is deleted by
        # function module tests.  This would cause a problem when the test
        # suite is run.
        DUT = test_program_dao.do_select_all(RAMSTKMatrix,
                                             key=[RAMSTKMatrix.revision_id,
                                                  RAMSTKMatrix.matrix_type],
                                             value=[1, 'fnctn_hrdwr'],
                                             order=RAMSTKMatrix.row_id,
                                             _all=True)[-1]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
