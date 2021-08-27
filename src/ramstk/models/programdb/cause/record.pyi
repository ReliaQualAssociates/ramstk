# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKCauseRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    mode_id: Any
    mechanism_id: Any
    cause_id: Any
    description: Any
    rpn: Any
    rpn_detection: Any
    rpn_detection_new: Any
    rpn_new: Any
    rpn_occurrence: Any
    rpn_occurrence_new: Any
    mechanism: relationship
    control: relationship
    action: relationship
    is_mode: bool
    is_mechanism: bool
    is_cause: bool
    is_control: bool
    is_action: bool
    def get_attributes(self): ...
