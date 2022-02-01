# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKFailureModeRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, str]]
    __tablename__: str
    __table_args__: Dict[str, bool]
    category_id: int
    subcategory_id: int
    mode_id: int
    description: str
    mode_ratio: float
    source: str
    category: relationship
    subcategory: relationship
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
