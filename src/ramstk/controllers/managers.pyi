# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.exceptions import DataAccessError as DataAccessError

class RAMSTKAnalysisManager:
    RAMSTK_USER_CONFIGURATION: Any = ...
    _attributes: Any = ...
    _tree: Any = ...
    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None: ...
    def on_get_all_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def on_get_tree(self, tree: treelib.Tree) -> None: ...

class RAMSTKDataManager:
    _db_id_colname: str = ...
    _db_tablename: str = ...
    _root: int = ...
    _tag: str = ...
    _pkey: Any = ...
    _dic_insert_function: Any = ...
    _parent_id: int = ...
    _revision_id: int = ...
    dao: Any = ...
    last_id: int = ...
    tree: Any = ...
    do_get_new_record: Any
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_connect(self, dao: BaseDatabase) -> None: ...
    def do_create_all_codes(self, prefix: str) -> None: ...
    def do_delete(self, node_id: int) -> None: ...
    def do_get_attributes(self, node_id: int, table: str) -> None: ...
    def do_get_tree(self) -> None: ...
    def do_insert(self, attributes: Dict[str, Any]) -> None: ...
    def do_select(self, node_id: Any, table: str = ...) -> Any: ...
    def do_set_attributes(self, node_id: List, package: Dict[str, Any]) -> None: ...
    def do_set_tree(self, tree: treelib.Tree) -> None: ...
    def do_update(self, node_id: int, table: str) -> None: ...
    def do_update_all(self) -> None: ...
    def on_insert(self, tree: treelib.Tree, node_id: int) -> None: ...
