# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModelRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _model_1 = RAMSTKModelRecord()
    _model_1.model_id = 1
    _model_1.model_type = "damage"
    _model_1.description = "Trump, Donald"

    DAO = MockDAO()
    DAO.table = [
        _model_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "model_id": 1,
        "model_type": "damage",
        "description": "Trump, Donald",
    }
