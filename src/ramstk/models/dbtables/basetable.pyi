# Standard Library Imports
from datetime import date
from typing import Any, Callable, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.views.gtk3 import _ as _

def do_clear_tree(tree: treelib.Tree) -> treelib.Tree: ...

class RAMSTKBaseTable:
    _db_id_colname: str
    _db_tablename: str
    _deprecated: bool
    _root: int
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _parent_id: int
    _record: object
    _revision_id: int
    dao: BaseDatabase
    last_id: int
    pkey: str
    tree: treelib.Tree
    do_get_new_record: Callable[[Dict[str, Union[date, float, int, str]]], object]
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_connect(self, dao: BaseDatabase) -> None: ...
    def do_create_all_codes(self, prefix: str) -> None: ...
    def do_delete(self, node_id: int) -> None: ...
    def do_get_attributes(self, node_id: int) -> None: ...
    def do_get_tree(self) -> None: ...
    def do_insert(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> None: ...
    def do_select(self, node_id: Any) -> Any: ...
    def do_select_all(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> None: ...
    def do_set_attributes(
        self, node_id: int, package: Dict[str, Union[date, float, int, str]]
    ) -> None: ...
    def do_set_attributes_all(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> None: ...
    def do_set_tree(self, tree: treelib.Tree) -> None: ...
    def do_update(self, node_id: int) -> None: ...
    def do_update_all(self) -> None: ...
    def _do_initialize_tree(self):
        pass
    def _do_initialize_attributes(self):
        pass
    def do_create_code_for_node(self, _node, prefix):
        pass
    def _do_delete_database_record(self, node_id):
        pass
    def _do_update_last_id(self):
        pass
    def _do_remove_tree_node(self, node_id):
        pass
    def _do_create_new_record(self, attributes):
        pass
    def _do_insert_record_in_database(self, _record):
        pass
    def _do_insert_record_in_tree(self, _identifier, _record):
        pass
    def _do_extract_keys_and_values(self, attributes):
        pass
    def _do_get_parent_id(self, _record):
        pass
    def _do_add_record_to_tree(self, _record, _parent_id):
        pass
    def _do_get_record_attributes(self, node_id):
        pass
    def _do_update_record_attributes(self, node_id, _attributes):
        pass
    def _do_subscribe_to_messages(self):
        pass
    def _do_extract_key_and_value(self, package):
        pass
    def do_create_code(self, identifier, prefix):
        pass
