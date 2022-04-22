# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKConditionRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _condition_1 = RAMSTKConditionRecord()
    _condition_1.condition_id = 1
    _condition_1.description = "Cavitation"
    _condition_1.condition_type = "operating"

    DAO = MockDAO()
    DAO.table = [
        _condition_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "condition_id": 1,
        "condition_type": "operating",
        "description": "Cavitation",
    }
