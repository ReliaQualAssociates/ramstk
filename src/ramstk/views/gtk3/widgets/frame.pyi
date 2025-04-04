# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .label import RAMSTKLabel as RAMSTKLabel
from .widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from .widget import WidgetProperties as WidgetProperties

class RAMSTKFrame(Gtk.Frame, RAMSTKBaseWidget):
    def __init__(self) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
