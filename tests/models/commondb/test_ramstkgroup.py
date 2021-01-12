# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKUser.py is part of The RAMSTK Project

#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKUser module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKGroup

ATTRIBUTES = {'description': 'Engineering, Design', 'group_type': 'workgroup'}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKGroup():
    """Class for testing the RAMSTKGroup model."""
    @pytest.mark.integration
    def test_ramstkworkgroup_create(self, test_common_dao):
        """ __init__() should create an RAMSTKGroup model. """
        DUT = test_common_dao.session.query(RAMSTKGroup).first()

        assert isinstance(DUT, RAMSTKGroup)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_group'
        assert DUT.group_id == 1
        assert DUT.description == 'Engineering, Design'
        assert DUT.group_type == 'workgroup'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKGroup).first()

        _attributes = DUT.get_attributes()
        assert _attributes['description'] == 'Engineering, Design'
        assert _attributes['group_type'] == 'workgroup'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKGroup).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKGroup).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Group Description'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKGroup).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
