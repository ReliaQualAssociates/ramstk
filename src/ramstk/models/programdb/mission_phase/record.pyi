# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKMissionPhaseRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    mission_id: int
    phase_id: int
    description: str
    name: str
    phase_start: float
    phase_end: float
    mission: relationship
    environment: relationship
    is_mission: bool
    is_phase: bool
    is_env: bool
    def get_attributes(self) -> Dict[str, Any]: ...
