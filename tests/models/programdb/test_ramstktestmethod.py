# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstktestmethod.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKTestMethod module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKTestMethod

ATTRIBUTES = {
    'remarks': '',
    'boundary_conditions': '',
    'description': 'Test Test Method'
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKTestMethod():
    @pytest.mark.integration
    def test_ramstkopstress_create(self, test_program_dao):
        """ __init__() should create an RAMSTKTestMethod model."""
        DUT = test_program_dao.session.query(RAMSTKTestMethod).filter(
            RAMSTKTestMethod.test_id == 1).first()

        assert isinstance(DUT, RAMSTKTestMethod)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_test_method'
        assert DUT.load_id == 1
        assert DUT.test_id == 1
        assert DUT.description == 'Kick his ass'
        assert DUT.boundary_conditions == ''
        assert DUT.remarks == 'Doyle Rowland'

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute:value pairs. """
        DUT = test_program_dao.session.query(RAMSTKTestMethod).filter(
            RAMSTKTestMethod.test_id == 1).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['load_id'] == 1
        assert _attributes['test_id'] == 1
        assert _attributes['description'] == 'Kick his ass'
        assert _attributes['boundary_conditions'] == ''
        assert _attributes['remarks'] == 'Doyle Rowland'

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKTestMethod).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKTestMethod).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKTestMethod).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
