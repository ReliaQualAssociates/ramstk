# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMethodRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
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
