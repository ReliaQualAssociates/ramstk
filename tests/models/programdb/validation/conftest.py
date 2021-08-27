# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKValidationRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _validation_1 = RAMSTKValidationRecord()
    _validation_1.revision_id = 1
    _validation_1.validation_id = 1
    _validation_1.acceptable_maximum = 30.0
    _validation_1.acceptable_mean = 20.0
    _validation_1.acceptable_minimum = 10.0
    _validation_1.acceptable_variance = 0.0
    _validation_1.confidence = 95.0
    _validation_1.cost_average = 0.0
    _validation_1.cost_ll = 0.0
    _validation_1.cost_maximum = 0.0
    _validation_1.cost_mean = 0.0
    _validation_1.cost_minimum = 0.0
    _validation_1.cost_ul = 0.0
    _validation_1.cost_variance = 0.0
    _validation_1.date_end = date.today() + timedelta(days=30)
    _validation_1.date_start = date.today()
    _validation_1.description = ""
    _validation_1.measurement_unit = 0
    _validation_1.name = "PRF-0001"
    _validation_1.status = 0.0
    _validation_1.task_type = 0
    _validation_1.task_specification = ""
    _validation_1.time_average = 0.0
    _validation_1.time_ll = 0.0
    _validation_1.time_maximum = 0.0
    _validation_1.time_mean = 0.0
    _validation_1.time_minimum = 0.0
    _validation_1.time_ul = 0.0
    _validation_1.time_variance = 0.0

    _validation_2 = RAMSTKValidationRecord()
    _validation_2.revision_id = 1
    _validation_2.validation_id = 2
    _validation_2.acceptable_maximum = 30.0
    _validation_2.acceptable_mean = 20.0
    _validation_2.acceptable_minimum = 10.0
    _validation_2.acceptable_variance = 0.0
    _validation_2.confidence = 95.0
    _validation_2.cost_average = 0.0
    _validation_2.cost_ll = 0.0
    _validation_2.cost_maximum = 0.0
    _validation_2.cost_mean = 0.0
    _validation_2.cost_minimum = 0.0
    _validation_2.cost_ul = 0.0
    _validation_2.cost_variance = 0.0
    _validation_2.date_end = date.today() + timedelta(days=20)
    _validation_2.date_start = date.today() - timedelta(days=10)
    _validation_2.description = ""
    _validation_2.measurement_unit = 0
    _validation_2.name = ""
    _validation_2.status = 0.0
    _validation_2.task_type = 5
    _validation_2.task_specification = ""
    _validation_2.time_average = 0.0
    _validation_2.time_ll = 0.0
    _validation_2.time_maximum = 0.0
    _validation_2.time_mean = 0.0
    _validation_2.time_minimum = 0.0
    _validation_2.time_ul = 0.0
    _validation_2.time_variance = 0.0

    _validation_3 = RAMSTKValidationRecord()
    _validation_3.revision_id = 1
    _validation_3.validation_id = 3
    _validation_3.acceptable_maximum = 30.0
    _validation_3.acceptable_mean = 20.0
    _validation_3.acceptable_minimum = 10.0
    _validation_3.acceptable_variance = 0.0
    _validation_3.confidence = 95.0
    _validation_3.cost_average = 0.0
    _validation_3.cost_ll = 0.0
    _validation_3.cost_maximum = 0.0
    _validation_3.cost_mean = 0.0
    _validation_3.cost_minimum = 0.0
    _validation_3.cost_ul = 0.0
    _validation_3.cost_variance = 0.0
    _validation_3.date_end = date.today() + timedelta(days=30)
    _validation_3.date_start = date.today()
    _validation_3.description = ""
    _validation_3.measurement_unit = 0
    _validation_3.name = ""
    _validation_3.status = 0.0
    _validation_3.task_type = 5
    _validation_3.task_specification = ""
    _validation_3.time_average = 20.0
    _validation_3.time_ll = 19.0
    _validation_3.time_maximum = 40.0
    _validation_3.time_mean = 34.0
    _validation_3.time_minimum = 12.0
    _validation_3.time_ul = 49.0
    _validation_3.time_variance = 0.0

    DAO = MockDAO()
    DAO.table = [
        _validation_1,
        _validation_2,
        _validation_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "validation_id": 1,
        "acceptable_maximum": 0.0,
        "acceptable_mean": 0.0,
        "acceptable_minimum": 0.0,
        "acceptable_variance": 0.0,
        "confidence": 95.0,
        "cost_average": 0.0,
        "cost_ll": 0.0,
        "cost_maximum": 0.0,
        "cost_mean": 0.0,
        "cost_minimum": 0.0,
        "cost_ul": 0.0,
        "cost_variance": 0.0,
        "date_end": date.today() + timedelta(days=30),
        "date_start": date.today(),
        "description": "",
        "measurement_unit": "",
        "name": "New Validation Task",
        "status": 0.0,
        "task_type": "",
        "task_specification": "",
        "time_average": 0.0,
        "time_ll": 0.0,
        "time_maximum": 0.0,
        "time_mean": 0.0,
        "time_minimum": 0.0,
        "time_ul": 0.0,
        "time_variance": 0.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKValidationRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
