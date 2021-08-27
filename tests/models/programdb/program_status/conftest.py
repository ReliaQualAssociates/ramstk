# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKProgramStatusRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _status_1 = RAMSTKProgramStatusRecord()
    _status_1.revision_id = 1
    _status_1.status_id = 1
    _status_1.cost_remaining = 284.98
    _status_1.date_status = date.today() - timedelta(days=1)
    _status_1.time_remaining = 125.0

    _status_2 = RAMSTKProgramStatusRecord()
    _status_2.revision_id = 1
    _status_2.status_id = 2
    _status_2.cost_remaining = 212.32
    _status_2.date_status = date.today()
    _status_2.time_remaining = 112.5

    DAO = MockDAO()
    DAO.table = [
        _status_1,
        _status_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "status_id": 1,
        "cost_remaining": 0.0,
        "date_status": date.today(),
        "time_remaining": 0.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKProgramStatusRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
