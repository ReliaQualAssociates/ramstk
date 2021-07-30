# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKAction as RAMSTKAction

class DataManager(RAMSTKDataManager):
    _id_col: str = ...
    _table: str = ...
    _tag: str = ...
    _pkey: Any = ...
    _hardware_id: int = ...
    _mode_id: int = ...
    _mechanism_id: int = ...
    _cause_id: int = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    _revision_id: Any = ...
    _parent_id: Any = ...
    last_id: Any = ...
    def do_select_all(self, attributes: Dict[str, Any]) -> None: ...
    def _do_insert_action(self) -> None: ...
