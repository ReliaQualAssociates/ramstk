# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModelRecord
from tests import MockDAO


@pytest.fixture
def mock_common_dao(monkeypatch):
    _model_1 = RAMSTKModelRecord()
    _model_1.model_id = 1
    _model_1.model_type = "damage"
    _model_1.description = "Trump, Donald"

    DAO = MockDAO()
    DAO.table = [
        _model_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "model_id": 1,
        "model_type": "damage",
        "description": "Trump, Donald",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
