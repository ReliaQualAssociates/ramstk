# Standard Library Imports
from typing import Any, Callable, Dict, List

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class FailureDefinitionTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_load_failure_definition(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
