# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import (
    RAMSTKHazardAnalysis as RAMSTKHazardAnalysis
)

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _pkey: Any = ...
    _last_id: Any = ...

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        ...

    last_id: Any = ...

    def _do_delete_hazard(self, node_id: int) -> None:
        ...

    def do_get_all_attributes(self, node_id: int) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    def do_insert_hazard(self, parent_id: int = ...) -> None:
        ...

    _revision_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: int) -> None:
        ...
