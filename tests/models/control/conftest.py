# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKControlRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _control_1 = RAMSTKControlRecord()
    _control_1.revision_id = 1
    _control_1.hardware_id = 1
    _control_1.mode_id = 6
    _control_1.mechanism_id = 3
    _control_1.cause_id = 3
    _control_1.control_id = 1
    _control_1.description = "Test FMEA Control #1 for Cause ID #3."
    _control_1.type_id = "Detection"

    _control_2 = RAMSTKControlRecord()
    _control_2.revision_id = 1
    _control_2.hardware_id = 1
    _control_2.mode_id = 6
    _control_2.mechanism_id = 3
    _control_2.cause_id = 3
    _control_2.control_id = 2
    _control_2.description = "Test FMEA Control #2 for Cause ID #3."
    _control_2.type_id = "Prevention"

    DAO = MockDAO()
    DAO.table = [
        _control_1,
        _control_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "control_id": 3,
        "description": "",
        "type_id": "",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKControlRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
