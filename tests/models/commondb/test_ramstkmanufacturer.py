# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.TestRAMSTKManufacturer.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKManufacturer module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKManufacturer

ATTRIBUTES = {
    'cage_code': '13606',
    'description': 'Sprague',
    'location': 'New Hampshire'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKManufacturer():
    """Class for testing the RAMSTKManufacturer model."""
    @pytest.mark.integration
    def test_ramstkmanufacturer_create(self, test_common_dao):
        """ __init__() should create an RAMSTKManufacturer model. """
        DUT = test_common_dao.session.query(RAMSTKManufacturer).first()

        assert isinstance(DUT, RAMSTKManufacturer)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_manufacturer'
        assert DUT.manufacturer_id == 1
        assert DUT.description == 'Sprague'
        assert DUT.location == 'New Hampshire'
        assert DUT.cage_code == '13606'


    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKManufacturer).first()

        _attributes = DUT.get_attributes()

        assert _attributes['cage_code'] == '13606'
        assert _attributes['description'] == 'Sprague'
        assert _attributes['location'] == 'New Hampshire'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKManufacturer).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKManufacturer).first()

        ATTRIBUTES['location'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['location'] == 'unknown'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKManufacturer).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
