# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class HazardsTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    _filtered_tree: bool
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool: ...
    def do_load_severity(
        self, criticalities: Dict[int, Tuple[str, str, int]]
    ) -> None: ...
    def do_load_hazards(self, hazards: Dict[Any, Any]) -> None: ...
    def do_load_probability(self, probabilities: List[str]) -> None: ...
    _parent_id: int
    _record_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def _on_select_function(self, attributes: Dict[str, Any]) -> None: ...
