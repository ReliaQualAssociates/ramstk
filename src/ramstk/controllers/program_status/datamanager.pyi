# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.models.programdb import RAMSTKProgramStatus as RAMSTKProgramStatus

class DataManager(RAMSTKDataManager):
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _select_msg: str = ...
    _tag: str = ...
    _dic_status: Any = ...
    _lst_id_columns: Any = ...
    _record: Any = ...
    pkey: str = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_get_actual_status(self) -> None: ...
    def _do_set_attributes(self, cost_remaining: Any, time_remaining: Any) -> None: ...
