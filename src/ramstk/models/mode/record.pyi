# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKModeRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    mode_id: Any
    critical_item: Any
    description: Any
    design_provisions: Any
    detection_method: Any
    effect_end: Any
    effect_local: Any
    effect_next: Any
    effect_probability: Any
    hazard_rate_source: Any
    isolation_method: Any
    mission: Any
    mission_phase: Any
    mode_criticality: Any
    mode_hazard_rate: Any
    mode_op_time: Any
    mode_probability: Any
    mode_ratio: Any
    operator_actions: Any
    other_indications: Any
    remarks: Any
    rpn_severity: Any
    rpn_severity_new: Any
    severity_class: Any
    single_point: Any
    type_id: Any
    mechanism: Any
    is_mode: bool
    is_mechanism: bool
    is_cause: bool
    is_control: bool
    is_action: bool
    is_opload: bool
    is_opstress: bool
    is_testmethod: bool
    def get_attributes(self): ...
