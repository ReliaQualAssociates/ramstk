# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKOpStressRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    mode_id: Any
    mechanism_id: Any
    load_id: Any
    stress_id: Any
    description: Any
    load_history: Any
    measurable_parameter: Any
    remarks: Any
    op_load: Any
    is_mode: bool
    is_mechanism: bool
    is_opload: bool
    is_opstress: bool
    is_testmethod: bool
    def get_attributes(self): ...
