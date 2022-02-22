# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKManufacturerRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _manufacturer_1 = RAMSTKManufacturerRecord()
    _manufacturer_1.manufacturer_id = 1
    _manufacturer_1.cage_code = "47278"
    _manufacturer_1.description = "Eaton"
    _manufacturer_1.location = "Cleveland, OH"

    DAO = MockDAO()
    DAO.table = [
        _manufacturer_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "manufacturer_id": 1,
        "cage_code": "47278",
        "description": "Eaton",
        "location": "Cleveland, OH",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKManufacturerRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
