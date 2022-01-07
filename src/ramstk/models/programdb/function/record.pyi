# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKFunctionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    function_id: int
    availability_logistics: float
    availability_mission: float
    cost: float
    function_code: str
    hazard_rate_logistics: float
    hazard_rate_mission: float
    level: int
    mmt: float
    mcmt: float
    mpmt: float
    mtbf_logistics: float
    mtbf_mission: float
    mttr: float
    name: str
    parent_id: int
    remarks: str
    safety_critical: bool
    total_mode_count: int
    total_part_count: int
    type_id: int
    hazard: relationship
    def get_attributes(self) -> Dict[str, Any]: ...
