# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKTestMethodRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    mode_id: Any
    mechanism_id: Any
    load_id: Any
    test_id: Any
    description: Any
    boundary_conditions: Any
    remarks: Any
    op_load: relationship
    is_mode: bool
    is_mechanism: bool
    is_opload: bool
    is_opstress: bool
    is_testmethod: bool
    def get_attributes(self): ...
