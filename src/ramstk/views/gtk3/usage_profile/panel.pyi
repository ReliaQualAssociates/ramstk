# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class UsageProfileTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    _dic_visible_mask: Dict[str, Dict[str, bool]]
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    dic_icons: Dict[str, Any]
    dic_units: Dict[str, Tuple[str, str, str]]
    def __init__(self) -> None: ...
    def do_load_combobox(self) -> None: ...
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_load_environment(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_mission(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_phase(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
