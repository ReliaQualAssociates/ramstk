# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses.criticality import (
    calculate_mode_criticality as calculate_mode_criticality,
)
from ramstk.analyses.criticality import (
    calculate_mode_hazard_rate as calculate_mode_hazard_rate,
)
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKModeRecord as RAMSTKModeRecord

class RAMSTKModeTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_criticality(self, item_hr: float) -> None: ...
