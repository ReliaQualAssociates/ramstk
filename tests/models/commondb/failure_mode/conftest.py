# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureModeRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _failure_mode_1 = RAMSTKFailureModeRecord()
    _failure_mode_1.category_id = 1
    _failure_mode_1.subcategory_id = 1
    _failure_mode_1.mode_id = 1
    _failure_mode_1.description = "Short (pin-to-pin)"
    _failure_mode_1.mode_ratio = 0.65
    _failure_mode_1.source = "FMD-97"

    DAO = MockDAO()
    DAO.table = [
        _failure_mode_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "mode_id": 1,
        "description": "Short (pin-to-pin)",
        "mode_ratio": 0.65,
        "source": "FMD-97",
    }
