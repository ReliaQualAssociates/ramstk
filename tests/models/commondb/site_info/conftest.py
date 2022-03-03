# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSiteInfoRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _site_1 = RAMSTKSiteInfoRecord()
    _site_1.site_id = 1
    _site_1.site_name = "DEMO SITE"
    _site_1.product_key = "DEMO"
    _site_1.expire_on = date.today() + timedelta(30)
    _site_1.function_enabled = 1
    _site_1.requirement_enabled = 1
    _site_1.hardware_enabled = 1
    _site_1.software_enabled = 0
    _site_1.rcm_enabled = 0
    _site_1.testing_enabled = 0
    _site_1.incident_enabled = 0
    _site_1.survival_enabled = 0
    _site_1.vandv_enabled = 1
    _site_1.hazard_enabled = 1
    _site_1.stakeholder_enabled = 1
    _site_1.allocation_enabled = 1
    _site_1.similar_item_enabled = 1
    _site_1.fmea_enabled = 1
    _site_1.pof_enabled = 1
    _site_1.rbd_enabled = 0
    _site_1.fta_enabled = 0

    DAO = MockDAO()
    DAO.table = [
        _site_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "site_id": 1,
        "site_name": "",
        "product_key": "",
        "expire_on": date.today() + timedelta(30),
        "function_enabled": 0,
        "requirement_enabled": 0,
        "hardware_enabled": 0,
        "software_enabled": 0,
        "rcm_enabled": 0,
        "testing_enabled": 0,
        "incident_enabled": 0,
        "survival_enabled": 0,
        "vandv_enabled": 0,
        "hazard_enabled": 0,
        "stakeholder_enabled": 0,
        "allocation_enabled": 0,
        "similar_item_enabled": 0,
        "fmea_enabled": 0,
        "pof_enabled": 0,
        "rbd_enabled": 0,
        "fta_enabled": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKSiteInfoRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
