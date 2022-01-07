# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord
from ramstk.utilities import none_to_default as none_to_default

class RAMSTKRequirementRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    requirement_id: int
    derived: bool
    description: str
    figure_number: str
    owner: str
    page_number: str
    parent_id: int
    priority: int
    requirement_code: str
    specification: str
    requirement_type: str
    validated: bool
    validated_date: str
    q_clarity_0: bool
    q_clarity_1: bool
    q_clarity_2: bool
    q_clarity_3: bool
    q_clarity_4: bool
    q_clarity_5: bool
    q_clarity_6: bool
    q_clarity_7: bool
    q_clarity_8: bool
    q_complete_0: bool
    q_complete_1: bool
    q_complete_2: bool
    q_complete_3: bool
    q_complete_4: bool
    q_complete_5: bool
    q_complete_6: bool
    q_complete_7: bool
    q_complete_8: bool
    q_complete_9: bool
    q_consistent_1: bool
    q_consistent_2: bool
    q_consistent_3: bool
    q_consistent_4: bool
    q_consistent_5: bool
    q_consistent_6: bool
    q_consistent_7: bool
    q_consistent_8: bool
    q_verifiable_0: bool
    q_verifiable_1: bool
    q_verifiable_2: bool
    q_verifiable_3: bool
    q_verifiable_4: bool
    q_verifiable_5: bool
    def get_attributes(self) -> Dict[str, Any]: ...
    def create_code(self, prefix: str) -> None: ...
