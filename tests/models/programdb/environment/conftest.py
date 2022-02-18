# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKEnvironmentRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _environment_1 = RAMSTKEnvironmentRecord()
    _environment_1.revision_id = 1
    _environment_1.mission_id = 1
    _environment_1.mission_phase_id = 1
    _environment_1.environment_id = 1
    _environment_1.name = "Condition Name"
    _environment_1.units = "Units"
    _environment_1.minimum = 0.0
    _environment_1.maximum = 0.0
    _environment_1.mean = 0.0
    _environment_1.variance = 0.0
    _environment_1.ramp_rate = 0.0
    _environment_1.low_dwell_time = 0.0
    _environment_1.high_dwell_time = 0.0

    _environment_2 = RAMSTKEnvironmentRecord()
    _environment_2.revision_id = 1
    _environment_2.mission_id = 1
    _environment_2.mission_phase_id = 1
    _environment_2.environment_id = 2
    _environment_2.name = "Condition Name"
    _environment_2.units = "Units"
    _environment_2.minimum = 0.0
    _environment_2.maximum = 0.0
    _environment_2.mean = 0.0
    _environment_2.variance = 0.0
    _environment_2.ramp_rate = 0.0
    _environment_2.low_dwell_time = 0.0
    _environment_2.high_dwell_time = 0.0

    _environment_3 = RAMSTKEnvironmentRecord()
    _environment_3.revision_id = 1
    _environment_3.mission_id = 1
    _environment_3.mission_phase_id = 1
    _environment_3.environment_id = 3
    _environment_3.name = "Condition Name"
    _environment_3.units = "Units"
    _environment_3.minimum = 0.0
    _environment_3.maximum = 0.0
    _environment_3.mean = 0.0
    _environment_3.variance = 0.0
    _environment_3.ramp_rate = 0.0
    _environment_3.low_dwell_time = 0.0
    _environment_3.high_dwell_time = 0.0

    DAO = MockDAO()
    DAO.table = [
        _environment_1,
        _environment_2,
        _environment_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "mission_id": 1,
        "mission_phase_id": 1,
        "environment_id": 1,
        "name": "Condition Name",
        "units": "Units",
        "minimum": 0.0,
        "maximum": 0.0,
        "mean": 0.0,
        "variance": 0.0,
        "ramp_rate": 0.0,
        "low_dwell_time": 0.0,
        "high_dwell_time": 0.0,
        "parent_id": 1,
        "record_id": 1,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKEnvironmentRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
