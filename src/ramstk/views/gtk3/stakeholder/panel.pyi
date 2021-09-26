# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class StakeholderTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def do_load_affinity_groups(
        self, affinities: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def do_load_stakeholders(self, stakeholders: Dict[int, str]) -> None: ...
    def _do_load_requirements(self, tree: treelib.Tree) -> None: ...
    def _on_insert(self, tree: treelib.Tree) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: int
    _parent_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
