# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class SimilarItemTreePanel(RAMSTKTreePanel):
    _lst_environments: list[str]
    _lst_qualities: list[str]
    _select_msg: str
    _tag: str
    _title: Incomplete
    _dic_visible_mask: dict[int, dict[str, bool]]
    _lst_widget_configuration: list[WidgetConfig]
    _filtered_tree: bool
    _method_id: int
    _on_edit_message: str
    def __init__(self) -> None: ...
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool: ...
    def do_refresh_functions(self, row: Gtk.TreeIter, function: list[str]) -> None: ...
    def _do_load_environments(self) -> None: ...
    def _do_load_quality(self) -> None: ...
    def _do_set_columns_visible(self) -> None: ...
    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None: ...
    def _do_set_reliability_attributes(self, tree: treelib.Tree) -> None: ...
    def _do_subscribe_to_messages(self) -> None: ...
    def _on_method_changed(self, method_id: int) -> None: ...
    _record_id: Incomplete
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    _parent_id: Incomplete
    def _on_select_hardware(self, attributes: dict[str, int | float | str]) -> None: ...
    def __do_load_similar_item(
        self, node: Any = "", row: Gtk.TreeIter = None
    ) -> None: ...
