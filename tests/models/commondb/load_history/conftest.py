# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKLoadHistoryRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _history_1 = RAMSTKLoadHistoryRecord()
    _history_1.history_id = 1
    _history_1.description = "Histogram"

    DAO = MockDAO()
    DAO.table = [
        _history_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "history_id": 1,
        "description": "Histogram",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKLoadHistoryRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
