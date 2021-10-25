# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKHazardRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    function_id: int
    hazard_id: int
    potential_hazard: str
    potential_cause: str
    assembly_effect: str
    assembly_severity: str
    assembly_probability: str
    assembly_hri: int
    assembly_mitigation: str
    assembly_severity_f: str
    assembly_probability_f: str
    assembly_hri_f: int
    function_1: str
    function_2: str
    function_3: str
    function_4: str
    function_5: str
    remarks: str
    result_1: float
    result_2: float
    result_3: float
    result_4: float
    result_5: float
    system_effect: str
    system_severity: str
    system_probability: str
    system_hri: int
    system_mitigation: str
    system_severity_f: str
    system_probability_f: str
    system_hri_f: int
    user_blob_1: str
    user_blob_2: str
    user_blob_3: str
    user_float_1: float
    user_float_2: float
    user_float_3: float
    user_int_1: int
    user_int_2: int
    user_int_3: int
    def get_attributes(self) -> Dict[str, Any]: ...
