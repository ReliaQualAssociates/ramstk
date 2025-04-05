# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets import WidgetProperties as WidgetProperties

# RAMSTK Local Imports
from . import RAMSTKButton as RAMSTKButton

class RAMSTKCheckButton(Gtk.CheckButton, RAMSTKButton):
    def __init__(self, label: str = "") -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_update(
        self, package: dict[str, bool | date | float | int | str]
    ) -> None: ...
