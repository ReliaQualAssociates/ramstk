# Standard Library Imports
from typing import Dict, Tuple, Union

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKFMEARecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, int, str]]
    __tablename__: str
    __table_args__: Tuple[Dict[str, bool]]
    revision_id: int
    hardware_id: int
    mode_id: int
    mechanism_id: int
    cause_id: int
    control_id: int
    action_id: int
    mode_description: str
    mechanism_description: str
    cause_description: str
    control_description: str
    action_description: str
    mission: str
    mission_phase: str
    effect_local: str
    effect_next: str
    effect_end: str
    detection_method: str
    other_indications: str
    isolation_method: str
    design_provisions: str
    operator_actions: str
    severity_class: str
    hazard_rate_source: str
    mode_probability: float
    effect_probability: float
    hazard_rate_active: float
    mode_ratio: float
    mode_hazard_rate: float
    mode_op_time: float
    mode_criticality: float
    type_id: int
    rpn_severity: int
    rpn_occurrence: int
    rpn_detection: int
    rpn: int
    action_category: str
    action_owner: str
    action_due_date: str
    action_status: str
    action_taken: str
    action_approved: int
    action_approve_date: str
    action_closed: int
    action_close_date: str
    rpn_severity_new: int
    rpn_occurrence_new: int
    rpn_detection_new: int
    rpn_new: int
    single_point: int
    pof_include: int
    remarks: str
    hardware_description: str
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
