# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses import criticality as criticality
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKCauseRecord as RAMSTKCauseRecord

class RAMSTKCauseTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_rpn(self, severity: int) -> None: ...
