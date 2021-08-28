# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKSiteInfoRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    site_id: Any
    site_name: Any
    product_key: Any
    expire_on: Any
    function_enabled: Any
    requirement_enabled: Any
    hardware_enabled: Any
    software_enabled: Any
    rcm_enabled: Any
    testing_enabled: Any
    incident_enabled: Any
    survival_enabled: Any
    vandv_enabled: Any
    hazard_enabled: Any
    stakeholder_enabled: Any
    allocation_enabled: Any
    similar_item_enabled: Any
    fmea_enabled: Any
    pof_enabled: Any
    rbd_enabled: Any
    fta_enabled: Any
    def get_attributes(self): ...
