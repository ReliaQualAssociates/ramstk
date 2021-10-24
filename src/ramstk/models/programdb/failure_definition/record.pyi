# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKFailureDefinitionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Any]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    definition_id: int
    definition: str
    def get_attributes(self) -> Dict[str, Any]: ...
