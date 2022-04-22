# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardsRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _hazards_1 = RAMSTKHazardsRecord()
    _hazards_1.hazard_id = 1
    _hazards_1.hazard_category = "Common Causes"
    _hazards_1.hazard_subcategory = "Fire"

    DAO = MockDAO()
    DAO.table = [
        _hazards_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "hazard_id": 1,
        "hazard_category": "Common Causes",
        "hazard_subcategory": "Fire",
    }
