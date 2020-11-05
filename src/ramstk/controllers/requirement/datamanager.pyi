# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKRequirement as RAMSTKRequirement

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _pkey: Any = ...

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        ...

    last_id: Any = ...

    def _do_delete_requirement(self, node_id: int) -> None:
        ...

    def _do_get_attributes(self, node_id: int, table: str) -> None:
        ...

    def do_create_code(self, node_id: int, prefix: str) -> None:
        ...

    def do_get_all_attributes(self, node_id: int) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    def do_insert_requirement(self, parent_id: int = ...) -> None:
        ...

    _revision_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: int) -> None:
        ...
