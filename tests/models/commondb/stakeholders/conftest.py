# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholdersRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _stakeholders_1 = RAMSTKStakeholdersRecord()
    _stakeholders_1.stakeholders_id = 1
    _stakeholders_1.stakeholder = "Customer"

    DAO = MockDAO()
    DAO.table = [
        _stakeholders_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "stakeholders_id": 1,
        "stakeholder": "Customer",
    }
