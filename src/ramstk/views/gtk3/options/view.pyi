# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKBasePanel as RAMSTKBasePanel
from ramstk.views.gtk3.widgets.dialogs import RAMSTKBaseDialog as RAMSTKBaseDialog

# RAMSTK Local Imports
from . import OptionsPanel as OptionsPanel

class OptionsDialog(RAMSTKBaseDialog):
    def __init__(self, parent: object = None) -> None: ...
