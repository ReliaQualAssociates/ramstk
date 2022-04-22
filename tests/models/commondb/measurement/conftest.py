# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMeasurementRecord
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    _measurement_1 = RAMSTKMeasurementRecord()
    _measurement_1.measurement_id = 1
    _measurement_1.measurement_type = "unit"
    _measurement_1.code = "CBT"
    _measurement_1.description = "Cubic Butt Ton"

    DAO = MockDAO()
    DAO.table = [
        _measurement_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "measurement_id": 1,
        "code": "CBT",
        "description": "Cubic Butt Ton",
        "measurement_type": "unit",
    }
