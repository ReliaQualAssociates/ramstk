# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKProgramInfoRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    function_active: Any
    requirement_active: Any
    hardware_active: Any
    software_active: Any
    rcm_active: Any
    testing_active: Any
    incident_active: Any
    survival_active: Any
    vandv_active: Any
    hazard_active: Any
    stakeholder_active: Any
    allocation_active: Any
    similar_item_active: Any
    fmea_active: Any
    pof_active: Any
    rbd_active: Any
    fta_active: Any
    created_on: Any
    created_by: Any
    last_saved: Any
    last_saved_by: Any
    def get_attributes(self): ...
