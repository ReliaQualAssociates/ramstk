# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _cause_1 = RAMSTKCauseRecord()
    _cause_1.revision_id = 1
    _cause_1.mode_id = 6
    _cause_1.mechanism_id = 3
    _cause_1.cause_id = 1
    _cause_1.description = "Test Failure Cause #1 for Mechanism ID 3"
    _cause_1.rpn = 0
    _cause_1.rpn_new = 0
    _cause_1.rpn_detection = 3
    _cause_1.rpn_detection_new = 3
    _cause_1.rpn_occurrence_new = 6
    _cause_1.rpn_occurrence = 4

    _cause_2 = RAMSTKCauseRecord()
    _cause_2.revision_id = 1
    _cause_2.hardware_id = 1
    _cause_2.mode_id = 6
    _cause_2.mechanism_id = 3
    _cause_2.cause_id = 2
    _cause_2.description = "Test Failure Cause #2 for Mechanism ID 3"
    _cause_2.rpn = 0
    _cause_2.rpn_detection = 6
    _cause_2.rpn_detection_new = 3
    _cause_2.rpn_new = 0
    _cause_2.rpn_occurrence = 6
    _cause_2.rpn_occurrence_new = 4

    DAO = MockDAO()
    DAO.table = [
        _cause_1,
        _cause_2,
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
        "description": "Test Failure Cause #1 for Mechanism ID 3",
        "rpn": 0,
        "rpn_detection": 10,
        "rpn_detection_new": 10,
        "rpn_new": 0,
        "rpn_occurrence": 10,
        "rpn_occurrence_new": 10,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKCauseRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
