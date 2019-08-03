# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkuser.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKUser module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKUser

ATTRIBUTES = {
    'user_lname': 'Tester',
    'user_fname': 'Johnny',
    'user_email': 'tester.johnny@reliaqual.com',
    'user_phone': '+1.269.867.5309',
    'user_group_id': '1'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKUser():
    """Class for testing the RAMSTKUser model."""
    @pytest.mark.integration
    def test_ramstkuser_create(self, test_common_dao):
        """ __init__() should create an RAMSTKUser model. """
        DUT = test_common_dao.session.query(RAMSTKUser).first()

        assert isinstance(DUT, RAMSTKUser)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_user'
        assert DUT.user_id == 1
        assert DUT.user_lname == 'Tester'
        assert DUT.user_fname == 'Johnny'
        assert DUT.user_email == 'tester.johnny@reliaqual.com'
        assert DUT.user_phone == '+1.269.867.5309'
        assert DUT.user_group_id == '1'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKUser).first()

        _attributes = DUT.get_attributes()

        assert _attributes['user_lname'] == 'Tester'
        assert _attributes['user_fname'] == 'Johnny'
        assert _attributes['user_email'] == 'tester.johnny@reliaqual.com'
        assert _attributes['user_phone'] == '+1.269.867.5309'
        assert _attributes['user_group_id'] == '1'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKUser).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKUser).first()

        ATTRIBUTES['user_lname'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['user_lname'] == 'Last Name'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKUser).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
