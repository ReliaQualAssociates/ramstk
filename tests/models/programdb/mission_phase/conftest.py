# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMissionPhaseRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_phase_1 = RAMSTKMissionPhaseRecord()
    _mission_phase_1.revision_id = 1
    _mission_phase_1.mission_id = 1
    _mission_phase_1.mission_phase_id = 1
    _mission_phase_1.description = "Phase #1 for mission #1"
    _mission_phase_1.name = "Start Up"
    _mission_phase_1.phase_start = 0.0
    _mission_phase_1.phase_end = 0.0

    _mission_phase_2 = RAMSTKMissionPhaseRecord()
    _mission_phase_2.revision_id = 1
    _mission_phase_2.mission_id = 1
    _mission_phase_2.mission_phase_id = 2
    _mission_phase_2.description = "Phase #2 for mission #1"
    _mission_phase_2.name = "Operation"
    _mission_phase_2.phase_start = 0.0
    _mission_phase_2.phase_end = 0.0

    _mission_phase_3 = RAMSTKMissionPhaseRecord()
    _mission_phase_3.revision_id = 1
    _mission_phase_3.mission_id = 1
    _mission_phase_3.mission_phase_id = 3
    _mission_phase_3.description = "Phase #3 for mission #1"
    _mission_phase_3.name = "Shut Down"
    _mission_phase_3.phase_start = 0.0
    _mission_phase_3.phase_end = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mission_phase_1,
        _mission_phase_2,
        _mission_phase_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "mission_phase_id": 1,
        "description": "",
        "name": "",
        "phase_start": 0.0,
        "phase_end": 0.0,
        "parent_id": 1,
        "record_id": 1,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKMissionPhaseRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
