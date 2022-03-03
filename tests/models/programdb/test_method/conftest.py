# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTestMethodRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _test_method_1 = RAMSTKTestMethodRecord()
    _test_method_1.revision_id = 1
    _test_method_1.hardware_id = 1
    _test_method_1.mode_id = 1
    _test_method_1.mechanism_id = 1
    _test_method_1.opload_id = 1
    _test_method_1.test_method_id = 1
    _test_method_1.description = "Test Test Method #1"
    _test_method_1.boundary_conditions = "Waters"
    _test_method_1.remarks = ""

    _test_method_2 = RAMSTKTestMethodRecord()
    _test_method_2.revision_id = 1
    _test_method_2.hardware_id = 1
    _test_method_2.mode_id = 1
    _test_method_2.mechanism_id = 1
    _test_method_2.opload_id = 1
    _test_method_2.test_method_id = 2
    _test_method_2.description = "Test Test Method #2"
    _test_method_2.boundary_conditions = "Sands"
    _test_method_2.remarks = ""

    DAO = MockDAO()
    DAO.table = [
        _test_method_1,
        _test_method_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 1,
        "mechanism_id": 1,
        "opload_id": 1,
        "test_method_id": 1,
        "description": "",
        "boundary_conditions": "",
        "remarks": "",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKTestMethodRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
