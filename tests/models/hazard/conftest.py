# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKHazardRecord

TEST_PROBS = {
    "A": "Level A - Frequent",
    "B": "Level B - Reasonably Probable",
    "C": "Level C - Occasional",
}


@pytest.fixture
def mock_program_dao(monkeypatch):
    _hazard_1 = RAMSTKHazardRecord()
    _hazard_1.revision_id = 1
    _hazard_1.function_id = 1
    _hazard_1.hazard_id = 1
    _hazard_1.assembly_effect = ""
    _hazard_1.assembly_hri = 20
    _hazard_1.assembly_hri_f = 4
    _hazard_1.assembly_mitigation = ""
    _hazard_1.assembly_probability = TEST_PROBS["A"]
    _hazard_1.assembly_probability_f = TEST_PROBS["B"]
    _hazard_1.assembly_severity = "Major"
    _hazard_1.assembly_severity_f = "Medium"
    _hazard_1.function_1 = "uf1*uf2"
    _hazard_1.function_2 = "res1/ui1"
    _hazard_1.function_3 = ""
    _hazard_1.function_4 = ""
    _hazard_1.function_5 = ""
    _hazard_1.potential_cause = ""
    _hazard_1.potential_hazard = ""
    _hazard_1.remarks = ""
    _hazard_1.result_1 = 0.0
    _hazard_1.result_2 = 0.0
    _hazard_1.result_3 = 0.0
    _hazard_1.result_4 = 0.0
    _hazard_1.result_5 = 0.0
    _hazard_1.system_effect = ""
    _hazard_1.system_hri = 20
    _hazard_1.system_hri_f = 20
    _hazard_1.system_mitigation = ""
    _hazard_1.system_probability = TEST_PROBS["A"]
    _hazard_1.system_probability_f = TEST_PROBS["C"]
    _hazard_1.system_severity = "Medium"
    _hazard_1.system_severity_f = "Medium"
    _hazard_1.user_blob_1 = ""
    _hazard_1.user_blob_2 = ""
    _hazard_1.user_blob_3 = ""
    _hazard_1.user_float_1 = 1.5
    _hazard_1.user_float_2 = 0.8
    _hazard_1.user_float_3 = 0.0
    _hazard_1.user_int_1 = 2
    _hazard_1.user_int_2 = 0
    _hazard_1.user_int_3 = 0

    DAO = MockDAO()
    DAO.table = [
        _hazard_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "function_id": 1,
        "hazard_id": 1,
        "potential_hazard": "",
        "potential_cause": "",
        "assembly_effect": "",
        "assembly_severity": "Major",
        "assembly_probability": TEST_PROBS["A"],
        "assembly_hri": 20,
        "assembly_mitigation": "",
        "assembly_severity_f": "Major",
        "assembly_probability_f": TEST_PROBS["A"],
        "assembly_hri_f": 20,
        "function_1": "",
        "function_2": "",
        "function_3": "",
        "function_4": "",
        "function_5": "",
        "remarks": "",
        "result_1": 0.0,
        "result_2": 0.0,
        "result_3": 0.0,
        "result_4": 0.0,
        "result_5": 0.0,
        "system_effect": "",
        "system_severity": "Major",
        "system_probability": TEST_PROBS["A"],
        "system_hri": 20,
        "system_mitigation": "",
        "system_severity_f": "Major",
        "system_probability_f": TEST_PROBS["A"],
        "system_hri_f": 20,
        "user_blob_1": "",
        "user_blob_2": "",
        "user_blob_3": "",
        "user_float_1": 0.0,
        "user_float_2": 0.0,
        "user_float_3": 0.0,
        "user_int_1": 0,
        "user_int_2": 0,
        "user_int_3": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKHazardRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
