# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.analyses import fha as fha
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKHazardRecord as RAMSTKHazardRecord

class RAMSTKHazardTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: RAMSTKHazardRecord
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_fha(self, node_id: int) -> None: ...
    def _do_calculate_hri(self, node_id: int) -> None: ...
    def _do_calculate_user_defined(self, node_id: int) -> None: ...
