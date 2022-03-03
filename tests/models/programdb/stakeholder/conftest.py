# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholderRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _stakeholder_1 = RAMSTKStakeholderRecord()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = "Stakeholder Input"
    _stakeholder_1.group = ""
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ""
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    _stakeholder_2 = RAMSTKStakeholderRecord()
    _stakeholder_2.revision_id = 1
    _stakeholder_2.requirement_id = 1
    _stakeholder_2.stakeholder_id = 2
    _stakeholder_2.customer_rank = 1
    _stakeholder_2.description = "Stakeholder Input"
    _stakeholder_2.group = ""
    _stakeholder_2.improvement = 0.0
    _stakeholder_2.overall_weight = 0.0
    _stakeholder_2.planned_rank = 1
    _stakeholder_2.priority = 1
    _stakeholder_2.stakeholder = ""
    _stakeholder_2.user_float_1 = 1.0
    _stakeholder_2.user_float_2 = 1.0
    _stakeholder_2.user_float_3 = 1.0
    _stakeholder_2.user_float_4 = 1.0
    _stakeholder_2.user_float_5 = 1.0

    DAO = MockDAO()
    DAO.table = [
        _stakeholder_1,
        _stakeholder_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "stakeholder_id": 1,
        "customer_rank": 1,
        "description": "Stakeholder Input",
        "group": "",
        "improvement": 0.0,
        "overall_weight": 0.0,
        "planned_rank": 1,
        "priority": 1,
        "requirement_id": 0,
        "stakeholder": "",
        "user_float_1": 1.0,
        "user_float_2": 1.0,
        "user_float_3": 1.0,
        "user_float_4": 1.0,
        "user_float_5": 1.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKStakeholderRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
