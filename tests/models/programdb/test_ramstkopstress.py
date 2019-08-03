# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkopstress.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKOpStress module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKOpStress

ATTRIBUTES = {
    'description': 'Test Operating Stress',
    'load_history': '',
    'measurable_parameter': '',
    'remarks': b'',
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKOpStress():
    """Class for testing the RAMSTKOpStress model."""
    @pytest.mark.integration
    def test_ramstkopstress_create(self, test_program_dao):
        """ __init__() should create an RAMSTKOpStress model."""
        DUT = test_program_dao.session.query(RAMSTKOpStress).first()

        assert isinstance(DUT, RAMSTKOpStress)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_op_stress'
        assert DUT.load_id == 1
        assert DUT.stress_id == 1
        assert DUT.description == 'Test Operating Stress'
        assert DUT.measurable_parameter == ''
        assert DUT.load_history == ''
        assert DUT.remarks == b''

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute:value pairs. """
        DUT = test_program_dao.session.query(RAMSTKOpStress).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKOpStress).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKOpStress).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKOpStress).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
