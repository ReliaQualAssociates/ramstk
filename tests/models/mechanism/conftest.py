# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKMechanismRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mechanism_1 = RAMSTKMechanismRecord()
    _mechanism_1.revision_id = 1
    _mechanism_1.hardware_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 1
    _mechanism_1.description = "Test Failure Mechanism #1"
    _mechanism_1.rpn = 100
    _mechanism_1.rpn_new = 100
    _mechanism_1.rpn_detection = 10
    _mechanism_1.rpn_detection_new = 10
    _mechanism_1.rpn_occurrence_new = 10
    _mechanism_1.rpn_occurrence = 10
    _mechanism_1.pof_include = 1

    _mechanism_2 = RAMSTKMechanismRecord()
    _mechanism_2.revision_id = 1
    _mechanism_2.hardware_id = 1
    _mechanism_2.mode_id = 6
    _mechanism_2.mechanism_id = 2
    _mechanism_2.description = "Test Failure Mechanism #2"
    _mechanism_2.rpn = 100
    _mechanism_2.rpn_new = 100
    _mechanism_2.rpn_detection = 10
    _mechanism_2.rpn_detection_new = 10
    _mechanism_2.rpn_occurrence_new = 10
    _mechanism_2.rpn_occurrence = 10
    _mechanism_2.pof_include = 1

    DAO = MockDAO()
    DAO.table = [
        _mechanism_1,
        _mechanism_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "description": "",
        "pof_include": 1,
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
    dut = mock_program_dao.do_select_all(RAMSTKMechanismRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
