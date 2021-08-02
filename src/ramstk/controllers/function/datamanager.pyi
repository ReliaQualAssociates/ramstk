# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKFunction as RAMSTKFunction

class DataManager(RAMSTKDataManager):
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _tag: str = ...
    _fkey: Any = ...
    _pkey: Any = ...
    _record: Any = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    last_id: Any = ...
    def do_select_all(self, attributes: Dict[str, Any]) -> None: ...
