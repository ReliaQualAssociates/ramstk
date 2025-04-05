# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties as WidgetProperties
from . import RAMSTKButton as RAMSTKButton

class RAMSTKFileChooserButton(Gtk.FileChooserButton, RAMSTKButton):
    def __init__(self, label: str = "...") -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
