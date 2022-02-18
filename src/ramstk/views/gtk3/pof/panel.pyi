# Standard Library Imports
from typing import Any, Callable, Dict, List

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class PoFTreePanel(RAMSTKTreePanel):
    _dic_column_masks: Dict[str, List[bool]]
    _dic_headings: Dict[str, List[str]]
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    _dic_visible_mask: Dict[str, List[str]]
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    dic_icons: Dict[str, str]
    lst_damage_models: List[str]
    lst_load_history: List[str]
    lst_measurable_parameters: List[str]
    def __init__(self) -> None: ...
    def do_load_comboboxes(self) -> None: ...
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_load_damage_models(self) -> None: ...
    def __do_load_load_history(self) -> None: ...
    def __do_load_measureable_parameters(self) -> None: ...
    def __do_load_mechanism(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_mode(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter: ...
    def __do_load_opload(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_opstress(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_test_method(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
