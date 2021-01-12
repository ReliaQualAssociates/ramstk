# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkstakeholders.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing RAMSTKStakeholders module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKStakeholders

ATTRIBUTES = {'stakeholder': 'Customer'}


@pytest.mark.usefixtures('test_common_dao')
class TestRAMSTKStakeholders():
    """Class for testing the RAMSTKStakeholders model."""
    @pytest.mark.integration
    def test_ramstkstakeholders_create(self, test_common_dao):
        """ __init__() should create an RAMSTKStakeholders model. """
        DUT = test_common_dao.session.query(RAMSTKStakeholders).first()

        assert isinstance(DUT, RAMSTKStakeholders)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_stakeholders'
        assert DUT.stakeholders_id == 1
        assert DUT.stakeholder == 'Customer'

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKStakeholders).first()

        _attributes = DUT.get_attributes()

        assert _attributes['stakeholders_id'] == 1
        assert _attributes['stakeholder'] == 'Customer'

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKStakeholders).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKStakeholders).first()

        ATTRIBUTES['stakeholder'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['stakeholder'] == 'Stakeholder'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKStakeholders).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
