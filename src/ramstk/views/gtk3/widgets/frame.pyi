# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .label import RAMSTKLabel as RAMSTKLabel

class RAMSTKFrame(Gtk.Frame):
    def __init__(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...
