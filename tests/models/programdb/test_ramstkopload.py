# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkopload.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKOpLoad module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKOpLoad

ATTRIBUTES = {
    'damage_model': '',
    'description': 'Test Operating Load',
    'priority_id': 0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKOpLoad():
    """Class for testing the RAMSTKOpLoad model."""
    @pytest.mark.integration
    def test_ramstkopload_create(self, test_program_dao):
        """ __init__() should create an RAMSTKOpLoad model. """
        DUT = test_program_dao.session.query(RAMSTKOpLoad).filter(
            RAMSTKOpLoad.load_id == 1).first()

        assert isinstance(DUT, RAMSTKOpLoad)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_op_load'
        assert DUT.mechanism_id == 1
        assert DUT.load_id == 1
        assert DUT.description == 'Test Operating Load'
        assert DUT.damage_model == ''
        assert DUT.priority_id == 0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute:value pairs. """
        DUT = test_program_dao.session.query(RAMSTKOpLoad).filter(
            RAMSTKOpLoad.load_id == 1).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['mechanism_id'] == 1
        assert _attributes['load_id'] == 1
        assert _attributes['description'] == 'Test Operating Load'
        assert _attributes['damage_model'] == ''
        assert _attributes['priority_id'] == 0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKOpLoad).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKOpLoad).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKOpLoad).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
