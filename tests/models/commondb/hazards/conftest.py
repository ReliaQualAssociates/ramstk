# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardsRecord
from tests import MockDAO


@pytest.fixture
def mock_common_dao(monkeypatch):
    _hazards_1 = RAMSTKHazardsRecord()
    _hazards_1.hazard_id = 1
    _hazards_1.hazard_category = "Common Causes"
    _hazards_1.hazard_subcategory = "Fire"

    DAO = MockDAO()
    DAO.table = [
        _hazards_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "hazard_id": 1,
        "hazard_category": "Common Causes",
        "hazard_subcategory": "Fire",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
