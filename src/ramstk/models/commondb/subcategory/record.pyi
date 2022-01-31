# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKSubCategoryRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, str]
    __tablename__: str
    __table_args__: Dict[str, bool]
    category_id: int
    subcategory_id: int
    description: str
    category: relationship
    mode: relationship
    def get_attributes(self) -> Dict[str, Union[int, str]]: ...
