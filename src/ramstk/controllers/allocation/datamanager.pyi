# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKAllocation as RAMSTKAllocation

class DataManager(RAMSTKDataManager):
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _select_msg: str = ...
    _tag: str = ...
    _pkey: Any = ...
    _lst_id_columns: Any = ...
    _record: Any = ...
    pkey: str = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    _parent_id: Any = ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None: ...
