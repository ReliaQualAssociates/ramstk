# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKFailureDefinitionRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, str]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    function_id: int
    definition_id: int
    definition: str
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
