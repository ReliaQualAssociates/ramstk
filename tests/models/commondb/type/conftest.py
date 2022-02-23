# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKTypeRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
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


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKTypeRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
