# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.utilities import string_to_boolean as string_to_boolean
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango

# RAMSTK Local Imports
from .label import RAMSTKLabel as RAMSTKLabel
from .widget import RAMSTKWidget as RAMSTKWidget

def do_make_cell(
    cell_type: str
) -> Union[Gtk.CellRendererText, Gtk.CellRendererToggle, Gtk.CellRendererSpin,
           Gtk.CellRendererCombo]:
    ...


def do_make_column(cells: List[Gtk.CellRenderer],
                   **kwargs: Dict[str, Any]) -> Gtk.TreeViewColumn:
    ...


def do_make_combo_cell() -> Gtk.CellRendererCombo:
    ...


def do_make_spin_cell() -> Gtk.CellRendererSpin:
    ...


def do_make_text_cell(blob: bool = ...) -> Gtk.CellRendererText:
    ...


def do_make_toggle_cell() -> Gtk.CellRendererToggle:
    ...


def do_set_cell_properties(cell: Gtk.CellRenderer, **kwargs: Any) -> None:
    ...


class RAMSTKTreeView(Gtk.TreeView, RAMSTKWidget):
    _has_pixbuf: bool = ...
    datatypes: Any = ...
    editable: Any = ...
    headings: Any = ...
    korder: Any = ...
    position: Any = ...
    visible: Any = ...
    widgets: Any = ...
    selection: Any = ...

    def __init__(self) -> None:
        ...

    def do_build_treeview(self, format_file: str, colors: Dict[str,
                                                               str]) -> None:
        ...

    def do_edit_cell(self, cell: Gtk.CellRenderer, path: str, new_text: Any,
                     position: int) -> Any:
        ...

    def do_expand_tree(self) -> None:
        ...

    def do_get_row_by_value(self, search_col: int, value: Any) -> Gtk.TreeIter:
        ...

    def do_insert_row(self,
                      data: Dict[str, Any],
                      prow: Gtk.TreeIter = ...) -> None:
        ...

    def do_load_tree(self,
                     tree: treelib.Tree,
                     tag: str,
                     row: Gtk.TreeIter = ...) -> None:
        ...

    def do_make_columns(self, colors: Dict[str, str] = ...) -> None:
        ...

    def do_make_model(self) -> None:
        ...

    def do_parse_format(self, fmt_file: str) -> None:
        ...

    def do_set_columns_editable(self) -> None:
        ...

    def do_set_editable_columns(self, method: object) -> None:
        ...

    def do_set_visible_columns(self) -> None:
        ...

    def get_aggregate_attributes(self, entity: object) -> List[Any]:
        ...

    def get_cell_model(self, column: int, clear: bool = ...) -> Gtk.TreeModel:
        ...

    def get_simple_attributes(self, entity: object) -> List[Any]:
        ...

    @staticmethod
    def _do_format_cell(__column: Gtk.TreeViewColumn, cell: Gtk.CellRenderer,
                        model: Gtk.TreeModel, row: Gtk.TreeIter,
                        data: Tuple[Any]) -> None:
        ...

    def _do_set_column_properties(self, key: str,
                                  column: Gtk.TreeViewColumn) -> None:
        ...

    @staticmethod
    def _resize_wrap(column: Gtk.TreeViewColumn, __param: Any,
                     cell: Gtk.CellRenderer) -> None:
        ...


class CellRendererML(Gtk.CellRendererText):
    textedit_window: Any = ...
    selection: Any = ...
    treestore: Any = ...
    treeiter: Any = ...
    textedit: Any = ...
    textbuffer: Any = ...

    def __init__(self) -> None:
        ...

    def do_get_size(self, widget: Any, cell_area: Any):
        ...

    def do_start_editing(self, __event: Any, treeview: Any, path: Any,
                         __background_area: Any, cell_area: Any,
                         __flags: Any) -> None:
        ...

    def _keyhandler(self, __widget: Any, event: Any) -> None:
        ...
