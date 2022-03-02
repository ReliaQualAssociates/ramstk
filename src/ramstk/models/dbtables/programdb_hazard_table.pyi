# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# RAMSTK Package Imports
from ramstk.analyses import fha as fha

# RAMSTK Local Imports
from ..dbrecords import RAMSTKHazardRecord as RAMSTKHazardRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKHazardTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKHazardRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKHazardRecord: ...
    def do_calculate_fha(self, node_id: int) -> None: ...
    def _do_calculate_hri(self, node_id: int) -> None: ...
    def _do_calculate_user_defined(self, node_id: int) -> None: ...
