# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKHazardRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    function_id: Any
    hazard_id: Any
    potential_hazard: Any
    potential_cause: Any
    assembly_effect: Any
    assembly_severity: Any
    assembly_probability: Any
    assembly_hri: Any
    assembly_mitigation: Any
    assembly_severity_f: Any
    assembly_probability_f: Any
    assembly_hri_f: Any
    function_1: Any
    function_2: Any
    function_3: Any
    function_4: Any
    function_5: Any
    remarks: Any
    result_1: Any
    result_2: Any
    result_3: Any
    result_4: Any
    result_5: Any
    system_effect: Any
    system_severity: Any
    system_probability: Any
    system_hri: Any
    system_mitigation: Any
    system_severity_f: Any
    system_probability_f: Any
    system_hri_f: Any
    user_blob_1: Any
    user_blob_2: Any
    user_blob_3: Any
    user_float_1: Any
    user_float_2: Any
    user_float_3: Any
    user_int_1: Any
    user_int_2: Any
    user_int_3: Any
    def get_attributes(self): ...
