# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models import RAMSTKFMEARecord


@pytest.fixture
def mock_program_dao(monkeypatch):
    _fmea_1 = RAMSTKFMEARecord()
    _fmea_1.revision_id = 1
    _fmea_1.hardware_id = 1
    _fmea_1.mode_id = 6
    _fmea_1.mechanism_id = 3
    _fmea_1.cause_id = 3
    _fmea_1.control_id = 1
    _fmea_1.action_id = 1
    _fmea_1.mode_description = "Test FMEA Mode #6 for Hardware ID #1."
    _fmea_1.mechanism_description = "Test FMEA Mechanism #3 for Mode ID #6."
    _fmea_1.cause_description = "Test FMEA Cause #3 for Mechanism ID #3."
    _fmea_1.control_description = "Test FMEA Control #1 for Cause ID #3."
    _fmea_1.action_description = "Test FMEA Action #1 for Cause ID #3."
    _fmea_1.mission = "Big Mission"
    _fmea_1.mission_phase = "Phase 1"
    _fmea_1.effect_local = "Local Effect"
    _fmea_1.effect_next = "Next Effect"
    _fmea_1.effect_end = "End Effect"
    _fmea_1.detection_method = "Detection Method"
    _fmea_1.other_indications = "Other Indications"
    _fmea_1.isolation_method = "Isolation Method"
    _fmea_1.design_provisions = "Design Provisions"
    _fmea_1.operator_actions = "Operations Actions"
    _fmea_1.severity_class = "III"
    _fmea_1.hazard_rate_source = "MIL-HDBK-217FN2"
    _fmea_1.mode_probability = "Maybe?"
    _fmea_1.effect_probability = 1.0
    _fmea_1.hazard_rate_active = 0.000035
    _fmea_1.mode_ratio = 0.5
    _fmea_1.mode_hazard_rate = 0.0
    _fmea_1.mode_op_time = 1.0
    _fmea_1.mode_criticality = 0.5
    _fmea_1.type_id = 1
    _fmea_1.rpn_severity = 5
    _fmea_1.rpn_occurrence = 6
    _fmea_1.rpn_detection = 3
    _fmea_1.rpn = 90
    _fmea_1.action_category = ""
    _fmea_1.action_owner = "weibullguy"
    _fmea_1.action_due_date = date.today()
    _fmea_1.action_status = "Closed"
    _fmea_1.action_taken = "Basically just screwed around"
    _fmea_1.action_approved = 1
    _fmea_1.action_approve_date = date.today()
    _fmea_1.action_closed = 1
    _fmea_1.action_close_date = date.today()
    _fmea_1.rpn_severity_new = 5
    _fmea_1.rpn_occurrence_new = 3
    _fmea_1.rpn_detection_new = 3
    _fmea_1.rpn_new = 45
    _fmea_1.single_point = 1
    _fmea_1.pof_include = 1
    _fmea_1.remarks = "Say something about this failure mode."
    _fmea_1.hardware_description = "Capacitor Ceramic 10uF"

    _fmea_2 = RAMSTKFMEARecord()
    _fmea_2.revision_id = 1
    _fmea_2.hardware_id = 1
    _fmea_2.mode_id = 7
    _fmea_2.mechanism_id = 4
    _fmea_2.cause_id = 4
    _fmea_2.control_id = 2
    _fmea_2.action_id = 2
    _fmea_2.mode_description = "Test FMEA Mode #7 for Hardware ID #1."
    _fmea_2.mechanism_description = "Test FMEA Mechanism #4 for Mode ID #7."
    _fmea_2.cause_description = "Test FMEA Cause #4 for Mechanism ID #4."
    _fmea_2.control_description = "Test FMEA Control #2 for Cause ID #4."
    _fmea_2.action_description = "Test FMEA Action #2 for Cause ID #4."
    _fmea_2.mission = "Big Mission"
    _fmea_2.mission_phase = "Phase 1"
    _fmea_2.effect_local = "Local Effect"
    _fmea_2.effect_next = "Next Effect"
    _fmea_2.effect_end = "End Effect"
    _fmea_2.detection_method = "Detection Method"
    _fmea_2.other_indications = "Other Indications"
    _fmea_2.isolation_method = "Isolation Method"
    _fmea_2.design_provisions = "Design Provisions"
    _fmea_2.operator_actions = "Operations Actions"
    _fmea_2.severity_class = "III"
    _fmea_2.hazard_rate_source = "MIL-HDBK-217FN2"
    _fmea_2.mode_probability = "Maybe?"
    _fmea_2.effect_probability = 1.0
    _fmea_2.hazard_rate_active = 0.000035
    _fmea_2.mode_ratio = 0.5
    _fmea_2.mode_hazard_rate = 0.0
    _fmea_2.mode_op_time = 1.0
    _fmea_2.mode_criticality = 0.5
    _fmea_2.type_id = 1
    _fmea_2.rpn_severity = 5
    _fmea_2.rpn_occurrence = 6
    _fmea_2.rpn_detection = 3
    _fmea_2.rpn = 90
    _fmea_2.action_category = ""
    _fmea_2.action_owner = "weibullguy"
    _fmea_2.action_due_date = date.today()
    _fmea_2.action_status = "Closed"
    _fmea_2.action_taken = "Basically just screwed around"
    _fmea_2.action_approved = 1
    _fmea_2.action_approve_date = date.today()
    _fmea_2.action_closed = 1
    _fmea_2.action_close_date = date.today()
    _fmea_2.rpn_severity_new = 5
    _fmea_2.rpn_occurrence_new = 3
    _fmea_2.rpn_detection_new = 3
    _fmea_2.rpn_new = 45
    _fmea_2.single_point = 1
    _fmea_2.pof_include = 1
    _fmea_2.remarks = "Say something about this failure mode."
    _fmea_2.hardware_description = "Capacitor Ceramic 10uF"

    DAO = MockDAO()
    DAO.table = [
        _fmea_1,
        _fmea_2,
    ]

    yield DAO


@pytest.fixture
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "control_id": 1,
        "action_id": 1,
        "mode_description": "Test FMEA Mode #6 for Hardware ID #1.",
        "mechanism_description": "Test FMEA Mechanism #3 for Mode ID #6.",
        "cause_description": "Test FMEA Cause #3 for Mechanism ID #3.",
        "control_description": "Test FMEA Control #1 for Cause ID #3.",
        "action_description": "Test FMEA Action #1 for Cause ID #3.",
        "mission": "Big Mission",
        "mission_phase": "Phase 1",
        "effect_local": "Local Effect",
        "effect_next": "Next Effect",
        "effect_end": "End Effect",
        "detection_method": "Detection Method",
        "other_indications": "Other Indications",
        "isolation_method": "Isolation Method",
        "design_provisions": "Design Provisions",
        "operator_actions": "Operations Actions",
        "severity_class": "III",
        "hazard_rate_source": "MIL-HDBK-217FN2",
        "mode_probability": "Maybe?",
        "effect_probability": 1.0,
        "hazard_rate_active": 0.000035,
        "mode_ratio": 0.5,
        "mode_hazard_rate": 0.0,
        "mode_op_time": 1.0,
        "mode_criticality": 0.5,
        "type_id": 1,
        "rpn_severity": 5,
        "rpn_occurrence": 6,
        "rpn_detection": 3,
        "rpn": 90,
        "action_category": "",
        "action_owner": "weibullguy",
        "action_due_date": date.today(),
        "action_status": "Closed",
        "action_taken": "Basically just screwed around",
        "action_approved": 1,
        "action_approve_date": date.today(),
        "action_closed": 1,
        "action_close_date": date.today(),
        "rpn_severity_new": 5,
        "rpn_occurrence_new": 3,
        "rpn_detection_new": 3,
        "rpn_new": 45,
        "single_point": 1,
        "pof_include": 1,
        "remarks": "Say something about this failure mode.",
        "hardware_description": "Capacitor, Ceramic, 10uF",
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKFMEARecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
