# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from ..combo import RAMSTKComboBox as RAMSTKComboBox
from ..matrix import RAMSTKMatrixView as RAMSTKMatrixView
from ..scrolledwindow import RAMSTKScrolledWindow as RAMSTKScrolledWindow
from . import RAMSTKBasePanel as RAMSTKBasePanel
from . import do_log_message as do_log_message

class RAMSTKMatrixPanel(RAMSTKBasePanel):
    grdMatrixView: RAMSTKMatrixView
    def __init__(self) -> None: ...
    def do_clear_panel(self) -> None: ...
    def do_load_panel(
        self, attribute_dic: dict[str, list[int] | tuple[int]]
    ) -> None: ...
    def do_make_panel(self) -> None: ...
    def do_set_callbacks(self) -> None: ...
    def on_changed_combo(self, combo_obj: RAMSTKComboBox) -> int: ...
