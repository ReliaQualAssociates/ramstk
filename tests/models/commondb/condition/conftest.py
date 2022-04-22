# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKConditionRecord
from tests import MockDAO


@pytest.fixture
def mock_common_dao(monkeypatch):
    _condition_1 = RAMSTKConditionRecord()
    _condition_1.condition_id = 1
    _condition_1.description = "Cavitation"
    _condition_1.condition_type = "operating"

    DAO = MockDAO()
    DAO.table = [
        _condition_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "condition_id": 1,
        "condition_type": "operating",
        "description": "Cavitation",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
