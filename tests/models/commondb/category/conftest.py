# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCategoryRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _category_1 = RAMSTKCategoryRecord()
    _category_1.category_id = 1
    _category_1.category_type = "hardware"
    _category_1.name = "IC"
    _category_1.value = 1
    _category_1.description = "Integrated Circuit"
    _category_1.harsh_ir_limit = 0.8
    _category_1.mild_ir_limit = 0.9
    _category_1.harsh_pr_limit = 1.0
    _category_1.mild_pr_limit = 1.0
    _category_1.harsh_vr_limit = 1.0
    _category_1.mild_vr_limit = 1.0
    _category_1.harsh_deltat_limit = 0.0
    _category_1.mild_deltat_limit = 0.0
    _category_1.harsh_maxt_limit = 125.0
    _category_1.mild_maxt_limit = 125.0

    DAO = MockDAO()
    DAO.table = [
        _category_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "category_id": 1,
        "category_type": "hardware",
        "name": "IC",
        "value": 1,
        "description": "Integrated Circuit",
        "harsh_ir_limit": 0.8,
        "mild_ir_limit": 0.9,
        "harsh_pr_limit": 1.0,
        "mild_pr_limit": 1.0,
        "harsh_vr_limit": 1.0,
        "mild_vr_limit": 1.0,
        "harsh_deltat_limit": 0.0,
        "mild_deltat_limit": 0.0,
        "harsh_maxt_limit": 125.0,
        "mild_maxt_limit": 125.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKCategoryRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
