# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkstatus.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKStatus module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKStatus

ATTRIBUTES = {
    'description': 'Incident has been initiated.',
    'name': 'Initiated',
    'status_type': 'incident'
}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKStatus():
    """Class for testing the RAMSTKStatus model."""
    @pytest.mark.integration
    def test_ramstkstatus_create(self, test_common_dao):
        """ __init__() should create an RAMSTKStatus model. """
        DUT = test_common_dao.session.query(RAMSTKStatus).first()

        assert isinstance(DUT, RAMSTKStatus)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_status'
        assert DUT.status_id == 1
        assert DUT.name == 'Initiated'
        assert DUT.description == 'Incident has been initiated.'
        assert DUT.status_type == 'incident'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKStatus).first()

        _attributes = DUT.get_attributes()

        assert _attributes['description'] == 'Incident has been initiated.'
        assert _attributes['name'] == 'Initiated'
        assert _attributes['status_type'] == 'incident'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKStatus).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKStatus).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Status Decription'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKStatus).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
