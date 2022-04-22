# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from tests import MockDAO


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
