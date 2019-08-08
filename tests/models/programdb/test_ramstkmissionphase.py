# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkmissionphase.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKPhase module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMissionPhase

ATTRIBUTES = {
    'description': b'Test Mission Phase 1',
    'name': '',
    'phase_end': 0.0,
    'phase_start': 0.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMissionPhase():
    """Class for testing the RAMSTKMissionPhase model."""
    @pytest.mark.integration
    def test_ramstkmissionphase_create(self, test_program_dao):
        """ __init__() should create an RAMSTKPhase model. """
        DUT = test_program_dao.session.query(RAMSTKMissionPhase).first()

        assert isinstance(DUT, RAMSTKMissionPhase)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mission_phase'
        assert DUT.mission_id == 1
        assert DUT.phase_id == 1
        assert DUT.description == b'Test Mission Phase 1'
        assert DUT.name == ''
        assert DUT.phase_start == 0.0
        assert DUT.phase_end == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_program_dao.session.query(RAMSTKMissionPhase).first()

        _attributes = DUT.get_attributes()
        assert _attributes['description'] == b'Test Mission Phase 1'
        assert _attributes['name'] == ''
        assert _attributes['phase_start'] == 0.0
        assert _attributes['phase_end'] == 0.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKMissionPhase).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKMissionPhase).first()

        ATTRIBUTES['name'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['name'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKMissionPhase).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
