# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKLoadHistoryRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
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
