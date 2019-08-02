# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstksiteinfo.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKSiteInfo module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKSiteInfo

ATTRIBUTES = {
    'product_key': '0000',
    'expire_on': date.today() + timedelta(30),
    'function_enabled': 0,
    'requirement_enabled': 0,
    'hardware_enabled': 0,
    'vandv_enabled': 0,
    'fmea_enabled': 0
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKSiteInfo():
    """Class for testing the RAMSTKSiteInfo model."""
    @pytest.mark.integration
    def test_ramstksiteinfo_create(self, test_common_dao):
        """ __init__() should create an RAMSTKSiteInfo model. """
        DUT = test_common_dao.session.query(RAMSTKSiteInfo).first()

        assert isinstance(DUT, RAMSTKSiteInfo)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_site_info'
        assert DUT.site_id == 1
        assert DUT.product_key == '0000'
        assert DUT.expire_on == date(2019, 8, 20)
        assert DUT.function_enabled == 0
        assert DUT.requirement_enabled == 0
        assert DUT.hardware_enabled == 0
        assert DUT.vandv_enabled == 0
        assert DUT.fmea_enabled == 0

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_common_dao.session.query(RAMSTKSiteInfo).first()

        _attributes = DUT.get_attributes()
        assert _attributes['site_id'] == 1
        assert _attributes['product_key'] == '0000'
        assert _attributes['expire_on'] == date(2019, 8, 20)
        assert _attributes['function_enabled'] == 0
        assert _attributes['requirement_enabled'] == 0
        assert _attributes['hardware_enabled'] == 0
        assert _attributes['vandv_enabled'] == 0
        assert _attributes['fmea_enabled'] == 0

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKSiteInfo).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKSiteInfo).first()

        ATTRIBUTES['fmea_enabled'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['fmea_enabled'] == 0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKSiteInfo).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
