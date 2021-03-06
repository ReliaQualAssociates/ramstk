# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.utilities import boolean_to_integer as boolean_to_integer
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton as RAMSTKCheckButton
from .combo import RAMSTKComboBox as RAMSTKComboBox
from .entry import RAMSTKEntry as RAMSTKEntry
from .entry import RAMSTKTextView as RAMSTKTextView
from .frame import RAMSTKFrame as RAMSTKFrame
from .label import RAMSTKLabel as RAMSTKLabel
from .label import do_make_label_group as do_make_label_group
from .plot import RAMSTKPlot as RAMSTKPlot
from .scrolledwindow import RAMSTKScrolledWindow as RAMSTKScrolledWindow
from .treeview import RAMSTKTreeView as RAMSTKTreeView

class RAMSTKPanel(RAMSTKFrame):
    _module: str = ...
    _dic_attribute_keys: Any = ...
    _dic_attribute_updater: Any = ...
    _dic_row_loader: Any = ...
    _lst_col_order: Any = ...
    _lst_labels: Any = ...
    _lst_widgets: Any = ...
    _parent_id: int = ...
    _record_id: int = ...
    _title: str = ...
    _tree_loaded: bool = ...
    fmt: str = ...
    pltPlot: Any = ...
    tvwTreeView: Any = ...

    def __init__(self) -> None:
        ...

    def do_clear_tree(self) -> None:
        ...

    def do_expand_tree(self) -> None:
        ...

    def do_load_panel(self,
                      tree: treelib.Tree = ...,
                      node_id: Any = ...,
                      row: Gtk.TreeIter = ...) -> None:
        ...

    def do_load_row(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_load_tree(self, tree: treelib.Tree) -> None:
        ...

    def do_make_panel_fixed(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def do_make_panel_plot(self) -> None:
        ...

    def do_make_panel_treeview(self) -> None:
        ...

    def do_make_treeview(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def do_set_cell_callbacks(self, message: str, columns: List[int]) -> None:
        ...

    def do_set_headings(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                     position: int, message: str) -> None:
        ...

    def on_cell_toggled(self, cell: Gtk.CellRenderer, path: str, position: int,
                        message: str) -> None:
        ...

    def on_changed_combo(self, combo: RAMSTKComboBox, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        ...

    def on_changed_entry(self, entry: RAMSTKEntry, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        ...

    def on_changed_textview(
            self, buffer: Gtk.TextBuffer, index: int, message: str,
            textview: RAMSTKTextView) -> Dict[Union[str, Any], Any]:
        ...

    def on_delete(self, tree: treelib.Tree) -> None:
        ...

    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        ...

    def on_insert(self, data: Any) -> None:
        ...

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        ...

    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int,
                   message: str) -> Dict[Union[str, Any], Any]:
        ...

    def _do_load_row(self, node: treelib.Node,
                     row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def _do_load_treerow(self, node: treelib.Node,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_read_text(self, entry: RAMSTKEntry,
                       keys: List[str]) -> Dict[str, Any]:
        ...
