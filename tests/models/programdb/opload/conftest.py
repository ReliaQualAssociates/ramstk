# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpLoadRecord
from tests import MockDAO


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opload_1 = RAMSTKOpLoadRecord()
    _opload_1.revision_id = 1
    _opload_1.hardware_id = 1
    _opload_1.mode_id = 6
    _opload_1.mechanism_id = 2
    _opload_1.opload_id = 1
    _opload_1.damage_model = 3
    _opload_1.description = "Test Operating Load #1"
    _opload_1.priority_id = 0

    _opload_2 = RAMSTKOpLoadRecord()
    _opload_2.revision_id = 1
    _opload_2.hardware_id = 1
    _opload_2.mode_id = 6
    _opload_2.mechanism_id = 2
    _opload_2.opload_id = 2
    _opload_2.damage_model = 1
    _opload_2.description = "Test Operating Load #2"
    _opload_2.priority_id = 0

    DAO = MockDAO()
    DAO.table = [
        _opload_1,
        _opload_2,
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
        "description": "",
        "damage_model": 2,
        "priority_id": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
