# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkhazards.py is part of The RAMSTK Project

#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKHazard module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKHazards

ATTRIBUTES = {
    'hazard_category': 'Acceleration/Gravity',
    'hazard_subcategory': 'Falls'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKSiteInfo():
    """Class for testing the RAMSTKSiteInfo model."""
    @pytest.mark.integration
    def test_ramstkhazards_create(self, test_common_dao):
        """ __init__() should create an RAMSTKHazard model. """
        DUT = test_common_dao.session.query(RAMSTKHazards).first()

        assert isinstance(DUT, RAMSTKHazards)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_hazards'
        assert DUT.hazard_id == 1
        assert DUT.hazard_category == 'Acceleration/Gravity'
        assert DUT.hazard_subcategory == 'Falls'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKHazards).first()

        _attributes = DUT.get_attributes()
        assert _attributes['hazard_category'] == 'Acceleration/Gravity'
        assert _attributes['hazard_subcategory'] == 'Falls'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKHazards).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKHazards).first()

        ATTRIBUTES['hazard_category'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['hazard_category'] == 'Hazard Category'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKHazards).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
