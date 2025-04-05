# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKBaseWidget as RAMSTKBaseWidget
from ramstk.views.gtk3.widgets import WidgetProperties as WidgetProperties

def do_make_buttonbox(view: Any, **kwargs: Any) -> Gtk.HButtonBox | Gtk.VButtonBox: ...

class RAMSTKButton(Gtk.Button, RAMSTKBaseWidget):
    label_text: Incomplete
    def __init__(self, label: str = "...") -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
