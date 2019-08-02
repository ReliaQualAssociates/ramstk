# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkmodel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKModel module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKModel

ATTRIBUTES = {
    'description': 'Adhesion Wear Model for Bearings',
    'model_type': 'damage'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKModel():
    """Class for testing the RAMSTKModel model."""
    @pytest.mark.integration
    def test_ramstkmodel_create(self, test_common_dao):
        """ __init__() should create an RAMSTKModel model. """
        DUT = test_common_dao.session.query(RAMSTKModel).first()

        assert isinstance(DUT, RAMSTKModel)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_model'
        assert DUT.model_id == 1
        assert DUT.description == 'Adhesion Wear Model for Bearings'
        assert DUT.model_type == 'damage'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKModel).first()

        _attributes = DUT.get_attributes()

        assert _attributes['description'] == 'Adhesion Wear Model for Bearings'
        assert _attributes['model_type'] == 'damage'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKModel).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKModel).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Model Description'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKModel).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
