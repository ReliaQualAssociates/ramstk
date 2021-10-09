# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKDialog as RAMSTKDialog
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

# RAMSTK Local Imports
from . import OptionsPanel as OptionsPanel

class OptionsDialog(RAMSTKDialog):
    _pnlPanel: OptionsPanel
    def __init__(self, parent: object = ...) -> None: ...
    def _cancel(self, __button: Gtk.Button): ...
    def __make_ui(self) -> None: ...
