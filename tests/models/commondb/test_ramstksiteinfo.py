# pylint: skip-file
# type: ignore
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
from mocks import MockDAO, mock_ramstk_siteinfo

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKSiteInfo


@pytest.fixture(scope='function')
def mock_common_dao(monkeypatch):
    DAO = MockDAO()
    DAO.table = mock_ramstk_siteinfo

    yield DAO


ATTRIBUTES = {
    'site_name': '',
    'product_key': '0000',
    'expire_on': date.today() + timedelta(30),
    'function_enabled': 0,
    'requirement_enabled': 0,
    'hardware_enabled': 0,
    'software_enabled': 0,
    'rcm_enabled': 0,
    'testing_enabled': 0,
    'incident_enabled': 0,
    'survival_enabled': 0,
    'vandv_enabled': 0,
    'hazard_enabled': 0,
    'stakeholder_enabled': 0,
    'allocation_enabled': 0,
    'similar_item_enabled': 0,
    'fmea_enabled': 0,
    'pof_enabled': 0,
    'rbd_enabled': 0,
    'fta_enabled': 0,
}


@pytest.mark.usefixtures('mock_common_dao')
class TestRAMSTKSiteInfo():
    """Class for testing the RAMSTKSiteInfo model."""
    @pytest.mark.unit
    def test_ramstksiteinfo_create(self, mock_common_dao):
        """__init__() should create an RAMSTKSiteInfo model."""
        DUT = mock_common_dao.do_select_all(RAMSTKSiteInfo)[0]

        assert isinstance(DUT, RAMSTKSiteInfo)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_site_info'
        assert DUT.site_id == 1
        assert DUT.site_name == 'DEMO SITE'
        assert DUT.product_key == 'DEMO'
        assert DUT.expire_on == date.today() + timedelta(30)
        assert DUT.function_enabled == 1
        assert DUT.requirement_enabled == 1
        assert DUT.hardware_enabled == 1
        assert DUT.software_enabled == 0
        assert DUT.rcm_enabled == 0
        assert DUT.testing_enabled == 0
        assert DUT.incident_enabled == 0
        assert DUT.survival_enabled == 0
        assert DUT.vandv_enabled == 1
        assert DUT.hazard_enabled == 1
        assert DUT.stakeholder_enabled == 1
        assert DUT.allocation_enabled == 1
        assert DUT.similar_item_enabled == 1
        assert DUT.fmea_enabled == 1
        assert DUT.pof_enabled == 1
        assert DUT.rbd_enabled == 0
        assert DUT.fta_enabled == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_common_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_common_dao.do_select_all(RAMSTKSiteInfo)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['site_id'] == 1
        assert _attributes['site_name'] == 'DEMO SITE'
        assert _attributes['product_key'] == 'DEMO'
        assert _attributes['expire_on'] == date.today() + timedelta(30)
        assert _attributes['function_enabled'] == 1
        assert _attributes['requirement_enabled'] == 1
        assert _attributes['hardware_enabled'] == 1
        assert _attributes['software_enabled'] == 0
        assert _attributes['rcm_enabled'] == 0
        assert _attributes['testing_enabled'] == 0
        assert _attributes['incident_enabled'] == 0
        assert _attributes['survival_enabled'] == 0
        assert _attributes['vandv_enabled'] == 1
        assert _attributes['hazard_enabled'] == 1
        assert _attributes['stakeholder_enabled'] == 1
        assert _attributes['allocation_enabled'] == 1
        assert _attributes['similar_item_enabled'] == 1
        assert _attributes['fmea_enabled'] == 1
        assert _attributes['pof_enabled'] == 1
        assert _attributes['rbd_enabled'] == 0
        assert _attributes['fta_enabled'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_common_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_common_dao.do_select_all(RAMSTKSiteInfo)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_common_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_common_dao.do_select_all(RAMSTKSiteInfo)[0]

        ATTRIBUTES['fmea_enabled'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['fmea_enabled'] == 0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_common_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_common_dao.do_select_all(RAMSTKSiteInfo)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
