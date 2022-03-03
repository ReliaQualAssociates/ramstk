# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramInfoRecord


@pytest.fixture(scope="function")
def mock_program_dao(monkeypatch):
    _program_1 = RAMSTKProgramInfoRecord()
    _program_1.revision_id = 1
    _program_1.function_active = 1
    _program_1.requirement_active = 1
    _program_1.hardware_active = 1
    _program_1.software_active = 0
    _program_1.rcm_active = 0
    _program_1.testing_active = 0
    _program_1.incident_active = 0
    _program_1.survival_active = 0
    _program_1.vandv_active = 1
    _program_1.hazard_active = 1
    _program_1.stakeholder_active = 1
    _program_1.allocation_active = 1
    _program_1.similar_item_active = 1
    _program_1.fmea_active = 1
    _program_1.pof_active = 1
    _program_1.rbd_active = 0
    _program_1.fta_active = 0
    _program_1.created_on = date.today()
    _program_1.created_by = ""
    _program_1.last_saved = date.today()
    _program_1.last_saved_by = ""

    DAO = MockDAO()
    DAO.table = [
        _program_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "function_active": 1,
        "requirement_active": 1,
        "hardware_active": 1,
        "software_active": 0,
        "rcm_active": 0,
        "testing_active": 0,
        "incident_active": 0,
        "survival_active": 0,
        "vandv_active": 1,
        "hazard_active": 1,
        "stakeholder_active": 1,
        "allocation_active": 1,
        "similar_item_active": 1,
        "fmea_active": 1,
        "pof_active": 1,
        "rbd_active": 0,
        "fta_active": 0,
        "created_on": date.today(),
        "created_by": "",
        "last_saved": date.today(),
        "last_saved_by": "",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKProgramInfoRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
