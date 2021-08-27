# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKFunctionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    function_id: Any
    availability_logistics: Any
    availability_mission: Any
    cost: Any
    function_code: Any
    hazard_rate_logistics: Any
    hazard_rate_mission: Any
    level: Any
    mmt: Any
    mcmt: Any
    mpmt: Any
    mtbf_logistics: Any
    mtbf_mission: Any
    mttr: Any
    name: Any
    parent_id: Any
    remarks: Any
    safety_critical: Any
    total_mode_count: Any
    total_part_count: Any
    type_id: Any
    hazard: relationship
    def get_attributes(self): ...
