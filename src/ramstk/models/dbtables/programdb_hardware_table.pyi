# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKHardwareRecord as RAMSTKHardwareRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKHardwareTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKHardwareRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    _parent_id: int
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKHardwareRecord: ...
