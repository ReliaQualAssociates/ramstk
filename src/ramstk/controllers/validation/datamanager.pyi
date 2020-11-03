# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus as RAMSTKProgramStatus
from ramstk.models.programdb import RAMSTKValidation as RAMSTKValidation

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _dic_status: Any = ...
    _pkey: Any = ...
    last_id: Any = ...
    status_tree: Any = ...

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        ...

    def _do_delete_validation(self, node_id: int) -> None:
        ...

    def _do_insert_status(self) -> RAMSTKProgramStatus:
        ...

    def _do_select_all_status_tree(self) -> None:
        ...

    def _do_update_program_status(self, cost_remaining: Any,
                                  time_remaining: Any) -> None:
        ...

    def do_get_all_attributes(self, node_id: Any) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    def do_get_status_tree(self) -> None:
        ...

    def do_insert_validation(self) -> None:
        ...

    _revision_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_set_all_attributes(self, attributes: Any) -> None:
        ...

    def do_update(self, node_id: Any) -> None:
        ...
