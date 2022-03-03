# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRPNRecord


@pytest.fixture
def mock_common_dao(monkeypatch):
    _rpn_1 = RAMSTKRPNRecord()
    _rpn_1.rpn_id = 1
    _rpn_1.rpn_type = "severity"
    _rpn_1.name = "Very Minor"
    _rpn_1.value = 1
    _rpn_1.description = "System operable with minimal interference."

    _rpn_2 = RAMSTKRPNRecord()
    _rpn_2.rpn_id = 11
    _rpn_2.rpn_type = "occurrence"
    _rpn_2.name = "Remote"
    _rpn_2.value = 1
    _rpn_2.description = "Failure rate is 1 in 1,500,000."

    _rpn_3 = RAMSTKRPNRecord()
    _rpn_3.rpn_id = 21
    _rpn_3.rpn_type = "detection"
    _rpn_3.name = "Almost Certain"
    _rpn_3.value = 1
    _rpn_3.description = (
        "Design control will almost certainly detect a potential "
        "mechanism/cause and subsequent failure mode."
    )

    DAO = MockDAO()
    DAO.table = [
        _rpn_1,
        _rpn_2,
        _rpn_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "rpn_id": 1,
        "rpn_type": "severity",
        "name": "Very Minor",
        "value": 1,
        "description": "System operable with minimal interference.",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_common_dao):
    """Get a record model instance for each test function."""
    dut = mock_common_dao.do_select_all(RAMSTKRPNRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
