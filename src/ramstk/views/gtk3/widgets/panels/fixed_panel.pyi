# Standard Library Imports
from datetime import date

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets.buttons import RAMSTKCheckButton as RAMSTKCheckButton

# RAMSTK Local Imports
from ..entry import RAMSTKTextView as RAMSTKTextView
from ..label import RAMSTKLabel as RAMSTKLabel
from ..label import do_make_label_group as do_make_label_group
from ..scrolledwindow import RAMSTKScrolledWindow as RAMSTKScrolledWindow
from ..widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from . import RAMSTKBasePanel as RAMSTKBasePanel

COLUMN_WIDTH: int
MARGIN: int
LABEL_SPACING: int

class RAMSTKFixedPanel(RAMSTKBasePanel):
    _dic_widget_field_map: dict[str, RAMSTKBaseWidget]
    fixed: Incomplete
    def __init__(self) -> None: ...
    def do_clear_fixed_panel(self) -> None: ...
    _record_id: Incomplete
    def do_load_fixed_panel(
        self, attributes: dict[str, bool | date | float | int | str]
    ) -> None: ...
    def do_make_fixed_panel(
        self, justify: Gtk.Justification = ..., n_columns: int = 1
    ) -> None: ...
    def _do_create_widgets_for_column(
        self, /, column: int, __justify: Gtk.Justification
    ): ...
    def _do_place_widgets(
        self,
        x_pos: list[int],
        labels: list[RAMSTKLabel],
        widgets: list[RAMSTKBaseWidget],
    ) -> None: ...
