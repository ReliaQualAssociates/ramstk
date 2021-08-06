# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKMission as RAMSTKMission

class DataManager(RAMSTKDataManager):
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _select_msg: str = ...
    _tag: str = ...
    _pkey: Any = ...
    _lst_id_columns: Any = ...
    _record: Any = ...
    pkey: str = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
