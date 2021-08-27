# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKRevisionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    availability_logistics: Any
    availability_mission: Any
    cost: Any
    cost_failure: Any
    cost_hour: Any
    hazard_rate_active: Any
    hazard_rate_dormant: Any
    hazard_rate_logistics: Any
    hazard_rate_mission: Any
    hazard_rate_software: Any
    mmt: Any
    mcmt: Any
    mpmt: Any
    mtbf_logistics: Any
    mtbf_mission: Any
    mttr: Any
    name: Any
    reliability_logistics: Any
    reliability_mission: Any
    remarks: Any
    total_part_count: Any
    revision_code: Any
    program_time: Any
    program_time_sd: Any
    program_cost: Any
    program_cost_sd: Any
    failures: relationship
    mission: relationship
    function: relationship
    requirement: relationship
    stakeholder: relationship
    hardware: relationship
    validation: relationship
    hazard: relationship
    program_status: relationship
    def get_attributes(self): ...
