# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKGroupRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _group_1 = RAMSTKGroupRecord()
    _group_1.group_id = 1
    _group_1.group_type = "work"
    _group_1.description = "Engineering, RMS"

    DAO = MockDAO()
    DAO.table = [
        _group_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "group_id": 1,
        "group_type": "work",
        "description": "Engineering, RMS",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKGroupRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
