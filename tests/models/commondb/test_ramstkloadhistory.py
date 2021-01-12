# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkloadhistory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing RAMSTKLoadHistory module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKLoadHistory

ATTRIBUTES = {'description': 'Load History Description'}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKLoadHistory():
    """Class for testing the RAMSTKLoadHistory model."""
    @pytest.mark.integration
    def test_ramstkloadhistory_create(self, test_common_dao):
        """ __init__() should create an RAMSTKLoadHistory model."""
        DUT = test_common_dao.session.query(RAMSTKLoadHistory).first()

        assert isinstance(DUT, RAMSTKLoadHistory)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_load_history'
        assert DUT.history_id == 1
        assert DUT.description == 'Cycle Counts'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a dict of attribute:value pairs. """
        DUT = test_common_dao.session.query(RAMSTKLoadHistory).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['history_id'] == 1
        assert _attributes['description'] == 'Cycle Counts'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKLoadHistory).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKLoadHistory).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes(
        )['description'] == 'Load History Description'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKLoadHistory).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
