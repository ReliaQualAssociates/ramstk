# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKCause as RAMSTKCause

class DataManager(RAMSTKDataManager):
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _select_msg: str = ...
    _tag: str = ...
    _fkey: Any = ...
    _pkey: Any = ...
    _record: Any = ...
    pkey: str = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
