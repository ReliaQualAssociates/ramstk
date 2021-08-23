# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord
from ramstk.utilities import none_to_default as none_to_default

class RAMSTKRequirementRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    requirement_id: Any
    derived: Any
    description: Any
    figure_number: Any
    owner: Any
    page_number: Any
    parent_id: Any
    priority: Any
    requirement_code: Any
    specification: Any
    requirement_type: Any
    validated: Any
    validated_date: Any
    q_clarity_0: Any
    q_clarity_1: Any
    q_clarity_2: Any
    q_clarity_3: Any
    q_clarity_4: Any
    q_clarity_5: Any
    q_clarity_6: Any
    q_clarity_7: Any
    q_clarity_8: Any
    q_complete_0: Any
    q_complete_1: Any
    q_complete_2: Any
    q_complete_3: Any
    q_complete_4: Any
    q_complete_5: Any
    q_complete_6: Any
    q_complete_7: Any
    q_complete_8: Any
    q_complete_9: Any
    q_consistent_0: Any
    q_consistent_1: Any
    q_consistent_2: Any
    q_consistent_3: Any
    q_consistent_4: Any
    q_consistent_5: Any
    q_consistent_6: Any
    q_consistent_7: Any
    q_consistent_8: Any
    q_verifiable_0: Any
    q_verifiable_1: Any
    q_verifiable_2: Any
    q_verifiable_3: Any
    q_verifiable_4: Any
    q_verifiable_5: Any
    def get_attributes(self): ...
    def create_code(self, prefix: str) -> None: ...
