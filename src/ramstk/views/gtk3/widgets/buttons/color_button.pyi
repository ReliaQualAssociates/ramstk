# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets.widget import WidgetProperties as WidgetProperties

# RAMSTK Local Imports
from . import RAMSTKButton as RAMSTKButton

class RAMSTKCheckButton(Gtk.ColorButton, RAMSTKButton):
    _default_height: int
    _default_width: int
    _edit_signal: str
    def __init__(self) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_update(
        self, package: dict[str, bool | date | float | int | str]
    ) -> None: ...
