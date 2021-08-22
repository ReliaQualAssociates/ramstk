# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKMissionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    mission_id: Any
    description: Any
    mission_time: Any
    time_units: Any
    phase: Any
    is_mission: bool
    is_phase: bool
    is_env: bool
    def get_attributes(self): ...
