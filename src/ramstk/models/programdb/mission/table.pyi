# Standard Library Imports
from typing import Any, Dict, List, Type

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKMissionRecord as RAMSTKMissionRecord

class RAMSTKMissionTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKMissionRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Any]
    ) -> Type[RAMSTKMissionRecord]: ...
