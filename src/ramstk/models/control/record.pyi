# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKControlRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    mode_id: Any
    mechanism_id: Any
    cause_id: Any
    control_id: Any
    description: Any
    type_id: Any
    cause: Any
    is_mode: bool
    is_mechanism: bool
    is_cause: bool
    is_control: bool
    is_action: bool
    def get_attributes(self): ...
