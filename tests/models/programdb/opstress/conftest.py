# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKOpStressRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opstress_1 = RAMSTKOpStressRecord()
    _opstress_1.revision_id = 1
    _opstress_1.hardware_id = 1
    _opstress_1.mode_id = 1
    _opstress_1.mechanism_id = 1
    _opstress_1.opload_id = 1
    _opstress_1.stress_id = 1
    _opstress_1.description = "Test Operating Stress #1"
    _opstress_1.load_history = 2
    _opstress_1.measurable_parameter = 0
    _opstress_1.remarks = ""

    _opstress_2 = RAMSTKOpStressRecord()
    _opstress_2.revision_id = 1
    _opstress_2.hardware_id = 1
    _opstress_2.mode_id = 1
    _opstress_2.mechanism_id = 1
    _opstress_2.opload_id = 1
    _opstress_2.stress_id = 2
    _opstress_2.description = "Test Operating Stress #2"
    _opstress_2.load_history = 1
    _opstress_2.measurable_parameter = 1
    _opstress_2.remarks = ""

    DAO = MockDAO()
    DAO.table = [
        _opstress_1,
        _opstress_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "opload_id": 3,
        "stress_id": 3,
        "description": "",
        "load_history": 4,
        "measurable_parameter": 2,
        "remarks": "",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKOpStressRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
