# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

class RAMSTKScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self, child: object) -> None:
        ...
