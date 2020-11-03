# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKRevision as RAMSTKRevision

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _pkey: Any = ...

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        ...

    def do_get_all_attributes(self, node_id: int) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    last_id: Any = ...

    def do_insert(self) -> None:
        ...

    def do_select_all(self) -> None:
        ...

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: int) -> None:
        ...

    def _do_delete(self, node_id: int) -> None:
        ...

    def _do_get_attributes(self, node_id: int) -> None:
        ...
