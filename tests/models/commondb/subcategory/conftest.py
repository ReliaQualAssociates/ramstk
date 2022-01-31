# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKSubCategoryRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _subcategory_1 = RAMSTKSubCategoryRecord()
    _subcategory_1.category_id = 1
    _subcategory_1.subcategory_id = 1
    _subcategory_1.description = "Linear"

    DAO = MockDAO()
    DAO.table = [
        _subcategory_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "description": "Linear",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKSubCategoryRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
