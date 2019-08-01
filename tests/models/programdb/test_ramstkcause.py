# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkcause.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKCause module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKCause

ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 0,
    'description': 'Test Failure Cause #1',
    'rpn_occurrence': 0,
    'rpn_detection_new': 0,
    'rpn_detection': 0,
    'rpn': 0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKCause():
    """Class for testing the RAMSTKCause model."""
    @pytest.mark.integration
    def test_ramstkcause_create(self, test_program_dao):
        """ __init__() should create an RAMSTKCause model. """
        DUT = test_program_dao.session.query(RAMSTKCause).first()

        assert isinstance(DUT, RAMSTKCause)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_cause'
        assert DUT.mode_id == 1
        assert DUT.cause_id == 1
        assert DUT.description == 'Test Functional FMEA Cause #1 for Mode ID 1'
        assert DUT.rpn == 0
        assert DUT.rpn_detection == 2
        assert DUT.rpn_detection_new == 1
        assert DUT.rpn_new == 0
        assert DUT.rpn_occurrence == 8
        assert DUT.rpn_occurrence_new == 5

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKCause).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['mode_id'] == 1
        assert _attributes['mechanism_id'] == -1
        assert _attributes['cause_id'] == 1
        assert _attributes['description'] == (
            'Test Functional FMEA Cause #1 for '
            'Mode ID 1')
        assert _attributes['rpn'] == 0
        assert _attributes['rpn_detection'] == 2
        assert _attributes['rpn_detection_new'] == 1
        assert _attributes['rpn_new'] == 0
        assert _attributes['rpn_occurrence'] == 8
        assert _attributes['rpn_occurrence_new'] == 5

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKCause).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKCause).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKCause).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
