# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKStakeholdersRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
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


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKStakeholdersRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
