# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkfailuredefinition.py is part of The
#       RAMSTK Project
#
# All rights reserved.
""" Test class for testing the RAMSTKFailureDefinition module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKFailureDefinition

ATTRIBUTES = {
    'definition': b'Failure Definition'
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKFailureDefinition():
    """Class for testing the RAMSTKFailureDefinition model."""
    @pytest.mark.integration
    def test_ramstkfailuredefinition_create(self, test_program_dao):
        """ __init__() should create an RAMSTKFailureDefinition model. """
        DUT = test_program_dao.session.query(RAMSTKFailureDefinition).first()

        assert isinstance(DUT, RAMSTKFailureDefinition)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_failure_definition'
        assert DUT.revision_id == 1
        assert DUT.definition_id == 1
        assert DUT.definition == b'Failure Definition'

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKFailureDefinition).first()

        _attributes = DUT.get_attributes()

        assert _attributes['definition'] == b'Failure Definition'

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKFailureDefinition).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKFailureDefinition).first()

        ATTRIBUTES['definition'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['definition'] == b'Failure Definition'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKFailureDefinition).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
