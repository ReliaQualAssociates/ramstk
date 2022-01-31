# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKCategoryRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, int, str]]
    __tablename__: str
    __table_args__: Dict[str, bool]
    category_id: int
    name: str
    description: str
    category_type: int
    value: int
    harsh_ir_limit: float
    mild_ir_limit: float
    harsh_pr_limit: float
    mild_pr_limit: float
    harsh_vr_limit: float
    mild_vr_limit: float
    harsh_deltat_limit: float
    mild_deltat_limit: float
    harsh_maxt_limit: float
    mild_maxt_limit: float
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
