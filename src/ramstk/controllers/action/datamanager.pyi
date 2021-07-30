# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKAction as RAMSTKAction

class DataManager(RAMSTKDataManager):
    _db_tablename: str = ...
    _id_col: str = ...
    _select_msg: str = ...
    _tag: str = ...
    _fkey: Any = ...
    _pkey: Any = ...
    _record: Any = ...
    last_id: int = ...
    pkey: str = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def new_record(self, attributes: Dict[str, Any]) -> Any: ...
