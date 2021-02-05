# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkfailuredefinition.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKFailureDefinition module algorithms and
models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO, mock_ramstk_failuredefinition

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKFailureDefinition


@pytest.fixture(scope='function')
def mock_program_dao(monkeypatch):
    DAO = MockDAO()
    DAO.table = mock_ramstk_failuredefinition

    yield DAO


ATTRIBUTES = {'definition': 'Failure Definition'}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKFailureDefinition:
    """Class for testing the RAMSTKFailureDefinition model."""
    @pytest.mark.unit
    def test_ramstkfailuredefinition_create(self, mock_program_dao):
        """__init__() should create an RAMSTKFailureDefinition model."""
        DUT = mock_program_dao.do_select_all(RAMSTKFailureDefinition)[0]

        assert isinstance(DUT, RAMSTKFailureDefinition)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_failure_definition'
        assert DUT.revision_id == 1
        assert DUT.definition_id == 1
        assert DUT.definition == 'Mock Failure Definition 1'

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKFailureDefinition)[1]

        _attributes = DUT.get_attributes()

        assert _attributes['definition'] == 'Mock Failure Definition 2'

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKFailureDefinition)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKFailureDefinition)[0]

        ATTRIBUTES['definition'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['definition'] == 'Failure Definition'

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKFailureDefinition)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
