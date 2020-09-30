from .label import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3 import GObject as GObject, Gtk as Gtk
from typing import Any, Dict

class RAMSTKFrame(Gtk.Frame):
    def __init__(self) -> None: ...
    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None: ...
