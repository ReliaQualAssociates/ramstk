# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKStatusRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _status_1 = RAMSTKStatusRecord()
    _status_1.status_id = 1
    _status_1.status_type = "action"
    _status_1.name = "Initiated"
    _status_1.description = "Action has been initiated."

    DAO = MockDAO()
    DAO.table = [
        _status_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "status_id": 1,
        "status_type": "action",
        "name": "Initiated",
        "description": "Action has been initiated.",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKStatusRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
