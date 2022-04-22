# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKUserRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _user_1 = RAMSTKUserRecord()
    _user_1.user_id = 1
    _user_1.user_lname = "Sweetheart"
    _user_1.user_fname = "Monica"
    _user_1.user_email = "monica.sweetheart@myclub.com"
    _user_1.user_phone = "269-867-5309"
    _user_1.user_group_id = "10"

    DAO = MockDAO()
    DAO.table = [
        _user_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "user_id": 1,
        "user_lname": "Sweetheart",
        "user_fname": "Monica",
        "user_email": "monica.sweetheart@myclub.com",
        "user_phone": "269-867-5309",
        "user_group_id": "10",
    }
