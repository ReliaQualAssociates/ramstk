# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkcontrol.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKControl module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKControl

ATTRIBUTES = {
    'description': 'Test Control',
    'type_id': 'Detection'
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKControl():
    """Class for testing the RAMSTKControl model."""
    @pytest.mark.integration
    def test_ramstkcontrol_create(self, test_program_dao):
        """
        __init__() should create an RAMSTKControl model.
        """
        DUT = test_program_dao.session.query(RAMSTKControl).first()

        assert isinstance(DUT, RAMSTKControl)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_control'
        assert DUT.cause_id == 1
        assert DUT.control_id == 1
        assert DUT.description == 'Test Functional FMEA Control #1 for Cause ID 1'
        assert DUT.type_id == 'Detection'


    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """
        get_attributes() should return a dictionary of attribute key:value pairs.
        """
        DUT = test_program_dao.session.query(RAMSTKControl).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['cause_id'] == 1
        assert _attributes['control_id'] == 1
        assert _attributes['description'] == ('Test Functional FMEA Control #1 '
                                              'for Cause ID 1')
        assert _attributes['type_id'] == 'Detection'


    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """
        set_attributes() should return a zero error code on success
        """
        DUT = test_program_dao.session.query(RAMSTKControl).first()

        assert DUT.set_attributes(ATTRIBUTES) is None


    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKControl).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''


    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKControl).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
