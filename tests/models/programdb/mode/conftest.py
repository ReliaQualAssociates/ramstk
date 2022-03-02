# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModeRecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mode_1 = RAMSTKModeRecord()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ""
    _mode_1.mission = "Default Mission"
    _mode_1.other_indications = ""
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ""
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ""
    _mode_1.detection_method = ""
    _mode_1.operator_actions = ""
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ""
    _mode_1.severity_class = ""
    _mode_1.description = "Test Failure Mode #1"
    _mode_1.mission_phase = ""
    _mode_1.mode_probability = ""
    _mode_1.remarks = ""
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ""
    _mode_1.effect_end = ""
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.8

    _mode_2 = RAMSTKModeRecord()
    _mode_2.revision_id = 1
    _mode_2.hardware_id = 1
    _mode_2.mode_id = 2
    _mode_2.effect_local = ""
    _mode_2.mission = "Default Mission"
    _mode_2.other_indications = ""
    _mode_2.mode_criticality = 0.0
    _mode_2.single_point = 0
    _mode_2.design_provisions = ""
    _mode_2.type_id = 0
    _mode_2.rpn_severity_new = 1
    _mode_2.effect_next = ""
    _mode_2.detection_method = ""
    _mode_2.operator_actions = ""
    _mode_2.critical_item = 0
    _mode_2.hazard_rate_source = ""
    _mode_2.severity_class = ""
    _mode_2.description = "Test Failure Mode #2"
    _mode_2.mission_phase = ""
    _mode_2.mode_probability = ""
    _mode_2.remarks = ""
    _mode_2.mode_ratio = 0.0
    _mode_2.mode_hazard_rate = 0.0
    _mode_2.rpn_severity = 1
    _mode_2.isolation_method = ""
    _mode_2.effect_end = ""
    _mode_2.mode_op_time = 0.0
    _mode_2.effect_probability = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mode_1,
        _mode_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 1,
        "critical_item": 0,
        "description": "",
        "design_provisions": "",
        "detection_method": "",
        "effect_end": "",
        "effect_local": "",
        "effect_next": "",
        "effect_probability": 0.0,
        "hazard_rate_source": "",
        "isolation_method": "",
        "mission": "Default Mission",
        "mission_phase": "",
        "mode_criticality": 0.0,
        "mode_hazard_rate": 0.0,
        "mode_op_time": 0.0,
        "mode_probability": "",
        "mode_ratio": 0.0,
        "operator_actions": "",
        "other_indications": "",
        "remarks": "",
        "rpn_severity": 1,
        "rpn_severity_new": 1,
        "severity_class": "",
        "single_point": 0,
        "type_id": 0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKModeRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
