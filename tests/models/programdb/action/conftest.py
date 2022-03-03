# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKActionRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _action_1 = RAMSTKActionRecord()
    _action_1.revision_id = 1
    _action_1.hardware_id = 1
    _action_1.mode_id = 6
    _action_1.mechanism_id = 3
    _action_1.cause_id = 3
    _action_1.action_id = 1
    _action_1.action_recommended = "Test FMEA Action #1 for Cause ID #3."
    _action_1.action_category = "Detection"
    _action_1.action_owner = ""
    _action_1.action_due_date = date.today() + timedelta(days=30)
    _action_1.action_status = ""
    _action_1.action_taken = ""
    _action_1.action_approved = 0
    _action_1.action_approve_date = date.today() + timedelta(days=30)
    _action_1.action_closed = 0
    _action_1.action_close_date = date.today() + timedelta(days=30)

    _action_2 = RAMSTKActionRecord()
    _action_2.revision_id = 1
    _action_2.hardware_id = 1
    _action_2.mode_id = 6
    _action_2.mechanism_id = 3
    _action_2.cause_id = 3
    _action_2.action_id = 2
    _action_2.action_recommended = "Test FMEA Action #2 for Cause ID #3."
    _action_2.action_category = "Detection"
    _action_2.action_owner = ""
    _action_2.action_due_date = date.today() + timedelta(days=23)
    _action_2.action_status = ""
    _action_2.action_taken = ""
    _action_2.action_approved = 0
    _action_2.action_approve_date = date.today() + timedelta(days=23)
    _action_2.action_closed = 0
    _action_2.action_close_date = date.today() + timedelta(days=22)

    DAO = MockDAO()
    DAO.table = [
        _action_1,
        _action_2,
    ]

    yield DAO


@pytest.fixture
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "action_id": 1,
        "action_recommended": "Test FMEA Action #1 for Cause ID #3.",
        "action_category": "",
        "action_owner": "weibullguy",
        "action_due_date": date.today(),
        "action_status": "Closed",
        "action_taken": "Basically just screwed around",
        "action_approved": 1,
        "action_approve_date": date.today(),
        "action_closed": 1,
        "action_close_date": date.today(),
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKActionRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
