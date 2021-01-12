# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstktype.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKType module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKType

ATTRIBUTES = {
    'code': 'PLN',
    'description': 'Planning',
    'type_type': 'incident'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKType():
    """Class for testing the RAMSTKType model."""
    @pytest.mark.integration
    def test_ramstktype_create(self, test_common_dao):
        """ __init__() should create an RAMSTKType model. """
        DUT = test_common_dao.session.query(RAMSTKType).first()

        assert isinstance(DUT, RAMSTKType)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_type'
        assert DUT.type_id == 1
        assert DUT.code == 'PLN'
        assert DUT.description == 'Planning'
        assert DUT.type_type == 'incident'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKType).first()

        _attributes = DUT.get_attributes()

        assert _attributes['code'] == 'PLN'
        assert _attributes['description'] == 'Planning'
        assert _attributes['type_type'] == 'incident'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKType).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKType).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Type Description'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKType).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
