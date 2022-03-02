# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRequirementRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _requirement_1 = RAMSTKRequirementRecord()
    _requirement_1.revision_id = 1
    _requirement_1.requirement_id = 1
    _requirement_1.derived = 0
    _requirement_1.description = ""
    _requirement_1.figure_number = ""
    _requirement_1.owner = 0
    _requirement_1.page_number = ""
    _requirement_1.parent_id = 0
    _requirement_1.priority = 0
    _requirement_1.requirement_code = "REL.1"
    _requirement_1.specification = ""
    _requirement_1.requirement_type = 0
    _requirement_1.validated = 0
    _requirement_1.validated_date = date.today()
    _requirement_1.q_clarity_0 = 0
    _requirement_1.q_clarity_1 = 0
    _requirement_1.q_clarity_2 = 0
    _requirement_1.q_clarity_3 = 0
    _requirement_1.q_clarity_4 = 0
    _requirement_1.q_clarity_5 = 0
    _requirement_1.q_clarity_6 = 0
    _requirement_1.q_clarity_7 = 0
    _requirement_1.q_clarity_8 = 0
    _requirement_1.q_complete_0 = 0
    _requirement_1.q_complete_1 = 0
    _requirement_1.q_complete_2 = 0
    _requirement_1.q_complete_3 = 0
    _requirement_1.q_complete_4 = 0
    _requirement_1.q_complete_5 = 0
    _requirement_1.q_complete_6 = 0
    _requirement_1.q_complete_7 = 0
    _requirement_1.q_complete_8 = 0
    _requirement_1.q_complete_9 = 0
    _requirement_1.q_consistent_0 = 0
    _requirement_1.q_consistent_1 = 0
    _requirement_1.q_consistent_2 = 0
    _requirement_1.q_consistent_3 = 0
    _requirement_1.q_consistent_4 = 0
    _requirement_1.q_consistent_5 = 0
    _requirement_1.q_consistent_6 = 0
    _requirement_1.q_consistent_7 = 0
    _requirement_1.q_consistent_8 = 0
    _requirement_1.q_verifiable_0 = 0
    _requirement_1.q_verifiable_1 = 0
    _requirement_1.q_verifiable_2 = 0
    _requirement_1.q_verifiable_3 = 0
    _requirement_1.q_verifiable_4 = 0
    _requirement_1.q_verifiable_5 = 0

    _requirement_2 = RAMSTKRequirementRecord()
    _requirement_2.revision_id = 1
    _requirement_2.requirement_id = 2
    _requirement_2.derived = 1
    _requirement_2.description = "Derived requirement #1 for base requirement #1."
    _requirement_2.figure_number = ""
    _requirement_2.owner = 0
    _requirement_2.page_number = ""
    _requirement_2.parent_id = 1
    _requirement_2.priority = 0
    _requirement_2.requirement_code = "REL.1.1"
    _requirement_2.specification = ""
    _requirement_2.requirement_type = 0
    _requirement_2.validated = 0
    _requirement_2.validated_date = date.today()
    _requirement_2.q_clarity_0 = 0
    _requirement_2.q_clarity_1 = 0
    _requirement_2.q_clarity_2 = 0
    _requirement_2.q_clarity_3 = 0
    _requirement_2.q_clarity_4 = 0
    _requirement_2.q_clarity_5 = 0
    _requirement_2.q_clarity_6 = 0
    _requirement_2.q_clarity_7 = 0
    _requirement_2.q_clarity_8 = 0
    _requirement_2.q_complete_0 = 0
    _requirement_2.q_complete_1 = 0
    _requirement_2.q_complete_2 = 0
    _requirement_2.q_complete_3 = 0
    _requirement_2.q_complete_4 = 0
    _requirement_2.q_complete_5 = 0
    _requirement_2.q_complete_6 = 0
    _requirement_2.q_complete_7 = 0
    _requirement_2.q_complete_8 = 0
    _requirement_2.q_complete_9 = 0
    _requirement_2.q_consistent_0 = 0
    _requirement_2.q_consistent_1 = 0
    _requirement_2.q_consistent_2 = 0
    _requirement_2.q_consistent_3 = 0
    _requirement_2.q_consistent_4 = 0
    _requirement_2.q_consistent_5 = 0
    _requirement_2.q_consistent_6 = 0
    _requirement_2.q_consistent_7 = 0
    _requirement_2.q_consistent_8 = 0
    _requirement_2.q_verifiable_0 = 0
    _requirement_2.q_verifiable_1 = 0
    _requirement_2.q_verifiable_2 = 0
    _requirement_2.q_verifiable_3 = 0
    _requirement_2.q_verifiable_4 = 0
    _requirement_2.q_verifiable_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _requirement_1,
        _requirement_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "requirement_id": 1,
        "derived": 0,
        "description": "New Requirement",
        "figure_number": "",
        "owner": 0,
        "page_number": "",
        "parent_id": 0,
        "priority": 0,
        "requirement_code": "",
        "specification": "",
        "requirement_type": 0,
        "validated": 0,
        "validated_date": date.today(),
        "q_clarity_0": 0,
        "q_clarity_1": 0,
        "q_clarity_2": 0,
        "q_clarity_3": 0,
        "q_clarity_4": 0,
        "q_clarity_5": 0,
        "q_clarity_6": 0,
        "q_clarity_7": 0,
        "q_clarity_8": 0,
        "q_complete_0": 0,
        "q_complete_1": 0,
        "q_complete_2": 0,
        "q_complete_3": 0,
        "q_complete_4": 0,
        "q_complete_5": 0,
        "q_complete_6": 0,
        "q_complete_7": 0,
        "q_complete_8": 0,
        "q_complete_9": 0,
        "q_consistent_0": 0,
        "q_consistent_1": 0,
        "q_consistent_2": 0,
        "q_consistent_3": 0,
        "q_consistent_4": 0,
        "q_consistent_5": 0,
        "q_consistent_6": 0,
        "q_consistent_7": 0,
        "q_consistent_8": 0,
        "q_verifiable_0": 0,
        "q_verifiable_1": 0,
        "q_verifiable_2": 0,
        "q_verifiable_3": 0,
        "q_verifiable_4": 0,
        "q_verifiable_5": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKRequirementRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
