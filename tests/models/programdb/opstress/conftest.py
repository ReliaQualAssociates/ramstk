# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpStressRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _opstress_1 = RAMSTKOpStressRecord()
    _opstress_1.revision_id = 1
    _opstress_1.hardware_id = 1
    _opstress_1.mode_id = 1
    _opstress_1.mechanism_id = 1
    _opstress_1.opload_id = 1
    _opstress_1.opstress_id = 1
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
    _opstress_2.opstress_id = 2
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
        "opstress_id": 3,
        "description": "",
        "load_history": 4,
        "measurable_parameter": 2,
        "remarks": "",
    }
