# Standard Library Imports
from typing import Any, Callable, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class SimilarItemMethodPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbSimilarItemMethod: RAMSTKComboBox
    _method_id: int
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def do_load_comboboxes(self) -> None: ...
    def _do_set_sensitive(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None: ...
    def _on_method_changed(self, combo: RAMSTKComboBox) -> None: ...

class SimilarItemTreePanel(RAMSTKTreePanel):
    _dic_quality: Dict[int, str]
    _dic_environment: Dict[int, str]
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Dict[str, Callable]
    _dic_visible_mask: Dict[int, Dict[str, str]]
    _method_id: int
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def do_load_combobox(self) -> None: ...
    def do_refresh_functions(self, row: Gtk.TreeIter, function: List[str]) -> None: ...
    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None: ...
    def _do_set_reliability_attributes(self, tree: treelib.Tree) -> None: ...
    def _on_method_changed(self, method_id: int) -> None: ...
    _record_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None: ...
    def _do_set_columns_visible(self) -> None: ...
    def __do_load_similar_item(
        self, node: Any = ..., row: Gtk.TreeIter = ...
    ) -> Gtk.TreeIter: ...
