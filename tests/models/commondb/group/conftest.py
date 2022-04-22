# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKGroupRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _group_1 = RAMSTKGroupRecord()
    _group_1.group_id = 1
    _group_1.group_type = "work"
    _group_1.description = "Engineering, RMS"

    DAO = MockDAO()
    DAO.table = [
        _group_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "group_id": 1,
        "group_type": "work",
        "description": "Engineering, RMS",
    }
