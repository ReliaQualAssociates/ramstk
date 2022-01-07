# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKMissionRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_1 = RAMSTKMissionRecord()
    _mission_1.revision_id = 1
    _mission_1.mission_id = 1
    _mission_1.description = "Test mission #1"
    _mission_1.mission_time = 100.0
    _mission_1.time_units = "hours"

    _mission_2 = RAMSTKMissionRecord()
    _mission_2.revision_id = 1
    _mission_2.mission_id = 2
    _mission_2.description = "Test mission #2"
    _mission_2.mission_time = 24.0
    _mission_2.time_units = "hours"

    DAO = MockDAO()
    DAO.table = [
        _mission_1,
        _mission_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "description": "New mission",
        "mission_time": 24.0,
        "time_units": "hours",
        "parent_id": 1,
        "record_id": 1,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKMissionRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
