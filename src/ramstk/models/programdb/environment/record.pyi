# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKEnvironmentRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    mission_id: int
    phase_id: int
    environment_id: int
    name: str
    units: str
    minimum: float
    maximum: float
    mean: float
    variance: float
    ramp_rate: float
    low_dwell_time: float
    high_dwell_time: float
    phase: relationship
    is_mission: bool
    is_phase: bool
    is_env: bool
    def get_attributes(self) -> Dict[str, Any]: ...
