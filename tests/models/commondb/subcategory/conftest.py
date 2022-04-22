# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSubCategoryRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _subcategory_1 = RAMSTKSubCategoryRecord()
    _subcategory_1.category_id = 1
    _subcategory_1.subcategory_id = 1
    _subcategory_1.description = "Linear"

    DAO = MockDAO()
    DAO.table = [
        _subcategory_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "description": "Linear",
    }
