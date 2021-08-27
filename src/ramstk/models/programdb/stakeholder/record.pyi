# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKStakeholderRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    stakeholder_id: Any
    customer_rank: Any
    description: Any
    group: Any
    improvement: Any
    overall_weight: Any
    planned_rank: Any
    priority: Any
    requirement_id: Any
    stakeholder: Any
    user_float_1: Any
    user_float_2: Any
    user_float_3: Any
    user_float_4: Any
    user_float_5: Any
    def get_attributes(self): ...
