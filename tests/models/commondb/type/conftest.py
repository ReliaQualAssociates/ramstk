# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTypeRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _type_1 = RAMSTKTypeRecord()
    _type_1.type_id = 1
    _type_1.type_type = "incident"
    _type_1.code = "PLN"
    _type_1.description = "Planning"

    DAO = MockDAO()
    DAO.table = [
        _type_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "type_id": 1,
        "type_type": "incident",
        "code": "PLN",
        "description": "Planning",
    }
