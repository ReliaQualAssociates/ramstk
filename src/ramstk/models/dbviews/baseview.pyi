# Standard Library Imports
from typing import Callable, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase

class RAMSTKBaseView:
    _root: int
    _tag: str
    _dic_load_functions: Dict[str, Callable[..., object]]
    _dic_trees: Dict[str, treelib.Tree]
    _lst_modules: List[str]
    _revision_id: int
    dao: BaseDatabase
    tree: treelib.Tree
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_set_tree(self, tree: treelib.Tree) -> None: ...
    def on_select_all(self) -> None: ...
