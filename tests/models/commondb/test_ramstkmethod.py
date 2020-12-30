# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkmethod.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKMethod module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKMethod

ATTRIBUTES = {
    'description': '',
    'method_type': 'detection',
    'name': 'Code Reviews'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKMethod():
    """Class for testing the RAMSTKMethod model."""
    @pytest.mark.integration
    def test_ramstkmethod_create(self, test_common_dao):
        """ __init__() should create an RAMSTKMethod model. """
        DUT = test_common_dao.session.query(RAMSTKMethod).first()

        assert isinstance(DUT, RAMSTKMethod)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_method'
        assert DUT.method_id == 1
        assert DUT.description == ''
        assert DUT.name == 'Code Reviews'
        assert DUT.method_type == 'detection'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a dict of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKMethod).first()

        _attributes = DUT.get_attributes()

        assert _attributes['description'] == ''
        assert _attributes['method_type'] == 'detection'
        assert _attributes['name'] == 'Code Reviews'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKMethod).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKMethod).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Method Description'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKMethod).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
