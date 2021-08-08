# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase

class RAMSTKBaseView:
    _root: int = ...
    _tag: str = ...
    _dic_load_functions: Any = ...
    _dic_trees: Any = ...
    _lst_modules: Any = ...
    _revision_id: int = ...
    dao: Any = ...
    tree: Any = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_set_tree(self, tree: treelib.Tree) -> None: ...
    def on_insert(self, tree: treelib.Tree, node_id: int) -> None: ...
    def on_select_all(self) -> None: ...
