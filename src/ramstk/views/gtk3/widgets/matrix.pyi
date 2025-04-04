# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .combo import RAMSTKComboBox as RAMSTKComboBox
from .label import RAMSTKLabel as RAMSTKLabel
from .widget import RAMSTKBaseWidget as RAMSTKBaseWidget

class RAMSTKMatrixView(Gtk.Grid, RAMSTKBaseWidget):
    column_id_dic: dict[str, int]
    icons_dic: Incomplete
    row_id_dic: dict[str, int]
    n_columns: int
    n_rows: int
    def __init__(self) -> None: ...
    def do_add_column(self) -> None: ...
    def do_add_row(self) -> None: ...
    def do_build_matrix(
        self,
        column_name_lst: list[tuple[str, str, int]],
        row_name_lst: list[tuple[str, str, int]],
    ) -> None: ...
    def do_get_widget(self, column_idx: int, row_idx: int) -> Gtk.Widget | None: ...
    def do_remove_column(self, position_idx: int) -> None: ...
    def do_remove_row(self, position_idx: int) -> None: ...
    def do_set_column_headings(
        self, column_name_lst: list[tuple[str, str, int]]
    ) -> None: ...
    def do_set_row_headings(self, row_name_lst: list[tuple[str, str, int]]) -> None: ...
