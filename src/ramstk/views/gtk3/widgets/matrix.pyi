# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .combo import RAMSTKComboBox as RAMSTKComboBox
from .label import RAMSTKLabel as RAMSTKLabel

class RAMSTKMatrixView(Gtk.Grid):
    column_id_dic: Dict[str, int]
    icons_dic: Dict[str, str]
    row_id_dic: Dict[str, int]
    n_columns: int
    n_rows: int
    def __init__(self) -> None: ...
    def do_add_column(self, heading_str: str, tooltip_str: str) -> None: ...
    def do_add_row(self, heading_str: str, tooltip_str: str) -> None: ...
    def do_remove_column(self, position_idx: int) -> None: ...
    def do_remove_row(self, position_idx: int) -> None: ...
    def do_set_column_headings(
        self, column_name_lst: List[Tuple[str, str, int]]
    ) -> None: ...
    def do_set_row_headings(self, row_name_lst: List[Tuple[str, str, int]]) -> None: ...
    def _do_add_widgets(
        self,
        position_tpl: Tuple[int, int],
        n_positions_int: int,
        heading_str: str,
        tooltip_str: str,
        row_flag: bool = ...,
    ) -> None: ...
    def _do_make_combobox(self) -> RAMSTKComboBox: ...
