# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkmechanism.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKMechanism module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMechanism

ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 10,
    'rpn_occurrence': 10,
    'description': 'Test Failure Mechanism #1',
    'rpn_detection_new': 10,
    'rpn_detection': 10,
    'rpn': 0,
    'pof_include': 1
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMechanism():
    """Class for testing the RAMSTKMechanism model."""
    @pytest.mark.integration
    def test_ramstkmechanism_create(self, test_program_dao):
        """ __init__() should create an RAMSTKMechanism model. """
        DUT = test_program_dao.session.query(RAMSTKMechanism).first()

        assert isinstance(DUT, RAMSTKMechanism)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mechanism'
        assert DUT.mode_id == 6
        assert DUT.mechanism_id == 3
        assert DUT.description == 'New Failure Mechanism'
        assert DUT.pof_include == 1
        assert DUT.rpn == 100
        assert DUT.rpn_detection == 10
        assert DUT.rpn_detection_new == 10
        assert DUT.rpn_new == 100
        assert DUT.rpn_occurrence == 10
        assert DUT.rpn_occurrence_new == 10

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute:value pairs. """
        DUT = test_program_dao.session.query(RAMSTKMechanism).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['mode_id'] == 6
        assert _attributes['mechanism_id'] == 3
        assert _attributes['description'] == ('New Failure Mechanism')
        assert _attributes['pof_include'] == 1
        assert _attributes['rpn'] == 100
        assert _attributes['rpn_detection'] == 10
        assert _attributes['rpn_detection_new'] == 10
        assert _attributes['rpn_new'] == 100
        assert _attributes['rpn_occurrence'] == 10
        assert _attributes['rpn_occurrence_new'] == 10

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKMechanism).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKMechanism).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKMechanism).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
