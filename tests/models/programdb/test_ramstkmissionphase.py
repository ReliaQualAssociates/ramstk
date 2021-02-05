# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkmissionphase.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKPhase module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMissionPhase


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_phase_1 = RAMSTKMissionPhase()
    _mission_phase_1.mission_id = 1
    _mission_phase_1.phase_id = 1
    _mission_phase_1.description = 'Phase #1 for test mission #1'
    _mission_phase_1.name = ''
    _mission_phase_1.phase_start = 0.0
    _mission_phase_1.phase_end = 0.0

    _mission_phase_2 = RAMSTKMissionPhase()
    _mission_phase_2.mission_id = 1
    _mission_phase_2.phase_id = 2
    _mission_phase_2.description = 'Phase #2 for test mission #1'
    _mission_phase_2.name = ''
    _mission_phase_2.phase_start = 0.0
    _mission_phase_2.phase_end = 0.0

    _mission_phase_3 = RAMSTKMissionPhase()
    _mission_phase_3.mission_id = 1
    _mission_phase_3.phase_id = 3
    _mission_phase_3.description = 'Phase #3 for test mission #1'
    _mission_phase_3.name = ''
    _mission_phase_3.phase_start = 0.0
    _mission_phase_3.phase_end = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mission_phase_1,
        _mission_phase_2,
        _mission_phase_3,
    ]

    yield DAO


ATTRIBUTES = {
    'description': 'Test Mission Phase 1',
    'name': '',
    'phase_end': 0.0,
    'phase_start': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKMissionPhase():
    """Class for testing the RAMSTKMissionPhase model."""
    @pytest.mark.integration
    def test_ramstkmissionphase_create(self, mock_program_dao):
        """__init__() should create an RAMSTKPhase model."""
        DUT = mock_program_dao.do_select_all(RAMSTKMissionPhase)[0]

        assert isinstance(DUT, RAMSTKMissionPhase)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mission_phase'
        assert DUT.mission_id == 1
        assert DUT.phase_id == 1
        assert DUT.description == 'Phase #1 for test mission #1'
        assert DUT.name == ''
        assert DUT.phase_start == 0.0
        assert DUT.phase_end == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attributes values on
        success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMissionPhase)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['description'] == 'Phase #1 for test mission #1'
        assert _attributes['name'] == ''
        assert _attributes['phase_start'] == 0.0
        assert _attributes['phase_end'] == 0.0

    @pytest.mark.integration
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMissionPhase)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKMissionPhase)[0]

        ATTRIBUTES['name'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['name'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKMissionPhase)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
