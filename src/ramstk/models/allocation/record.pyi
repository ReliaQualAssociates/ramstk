# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKAllocationRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    availability_alloc: Any
    duty_cycle: Any
    env_factor: Any
    goal_measure_id: Any
    hazard_rate_alloc: Any
    hazard_rate_goal: Any
    included: Any
    int_factor: Any
    allocation_method_id: Any
    mission_time: Any
    mtbf_alloc: Any
    mtbf_goal: Any
    n_sub_systems: Any
    n_sub_elements: Any
    parent_id: Any
    percent_weight_factor: Any
    reliability_alloc: Any
    reliability_goal: Any
    op_time_factor: Any
    soa_factor: Any
    weight_factor: Any
    def get_attributes(self): ...
