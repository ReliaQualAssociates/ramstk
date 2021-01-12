# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkaction.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKAction module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKAction

ATTRIBUTES = {
    'action_due_date': date(2019, 8, 20),
    'action_approve_date': date(2019, 8, 20),
    'action_status': '',
    'action_closed': 0,
    'action_taken': '',
    'action_close_date': date(2019, 8, 20),
    'action_recommended': 'Recommended action for Failure Cause #1',
    'action_category': '',
    'action_owner': '',
    'action_approved': 0,
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKAction():
    """Class for testing the RAMSTKAction model."""
    @pytest.mark.integration
    def test_ramstkaction_create(self, test_program_dao):
        """__init__() should create an RAMSTKAction model."""
        DUT = test_program_dao.session.query(RAMSTKAction).first()
        assert isinstance(DUT, RAMSTKAction)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_action'
        assert DUT.cause_id == 1
        assert DUT.action_id == 1
        assert DUT.action_recommended == (
            'Test FMEA Recommended Action #1 for Cause ID 2.')
        assert DUT.action_category == ''
        assert DUT.action_owner == ''
        assert DUT.action_due_date == date(2019, 8, 20)
        assert DUT.action_status == ''
        assert DUT.action_taken == ''
        assert DUT.action_approved == 0
        assert DUT.action_approve_date == date(2019, 8, 20)
        assert DUT.action_closed == 0
        assert DUT.action_close_date == date(2019, 8, 20)

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = test_program_dao.session.query(RAMSTKAction).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = test_program_dao.session.query(RAMSTKAction).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKAction).first()

        ATTRIBUTES['action_status'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['action_recommended'] == ('Recommended '
                                                              'action for '
                                                              'Failure Cause '
                                                              '#1')
        assert DUT.get_attributes()['action_status'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKAction).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
