# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMethodRecord
from tests import MockDAO


@pytest.fixture
def mock_common_dao(monkeypatch):
    _method_1 = RAMSTKMethodRecord()
    _method_1.method_id = 1
    _method_1.method_type = "detection"
    _method_1.name = "Sniff"
    _method_1.description = "Smell Test"

    DAO = MockDAO()
    DAO.table = [
        _method_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "method_id": 1,
        "method_type": "detection",
        "name": "Sniff",
        "description": "Smell Test",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
