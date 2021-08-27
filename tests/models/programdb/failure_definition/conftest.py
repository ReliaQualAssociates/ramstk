# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKFailureDefinitionRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _definition_1 = RAMSTKFailureDefinitionRecord()
    _definition_1.revision_id = 1
    _definition_1.definition_id = 1
    _definition_1.definition = "Mock Failure Definition 1"

    _definition_2 = RAMSTKFailureDefinitionRecord()
    _definition_2.revision_id = 1
    _definition_2.definition_id = 2
    _definition_2.definition = "Mock Failure Definition 2"

    DAO = MockDAO()
    DAO.table = [
        _definition_1,
        _definition_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "definition_id": 1,
        "definition": "Failure Definition",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKFailureDefinitionRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
