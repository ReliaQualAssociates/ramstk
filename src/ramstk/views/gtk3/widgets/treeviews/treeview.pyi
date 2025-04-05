# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import sort_dict as sort_dict
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from ..label import RAMSTKLabel as RAMSTKLabel
from ..widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from ..widget import WidgetProperties as WidgetProperties
from . import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from . import RAMSTKCellRendererSpin as RAMSTKCellRendererSpin
from . import RAMSTKCellRendererText as RAMSTKCellRendererText
from . import RAMSTKCellRendererToggle as RAMSTKCellRendererToggle

def do_make_column(
    cells: list[object], heading: str, visible: bool
) -> Gtk.TreeViewColumn: ...

class RAMSTKTreeView(Gtk.TreeView, RAMSTKBaseWidget):
    dic_field_position_map: dict[str, int]
    filtered_model: Gtk.TreeModelFilter
    selection: Incomplete
    unfiltered_model: Incomplete
    def __init__(self) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_delete_row(self, filtered: bool) -> None: ...
    def do_insert_row(
        self, data: dict[str, Any], prow: Gtk.TreeIter = None
    ) -> None: ...
    def do_load_cellrenderercombo(
        self, column: str, entries: list[str], clear: bool = True
    ) -> None: ...
    def do_load_tree(
        self,
        tree: treelib.Tree,
        row: Gtk.TreeIter | None = None,
        nid: int | None = None,
    ) -> None: ...
    def do_make_column(self, cellrenderer: Gtk.CellRenderer, n_fields: int) -> None: ...
    def do_make_model(
        self, column_types: list[str], store_type: str = "tree"
    ) -> None: ...
    def do_set_visible_columns(self) -> None: ...
    def do_get_row_by_value(self, search_col: int, value: Any) -> Gtk.TreeIter: ...
    def do_set_editable_columns(self, method: object) -> None: ...
