# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties as WidgetProperties
from . import RAMSTKButton as RAMSTKButton

class RAMSTKOptionButton(Gtk.RadioButton, RAMSTKButton):
    def __init__(self, group: Gtk.RadioButton = None, label: str = "") -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_update(
        self, package: dict[str, bool | date | float | int | str]
    ) -> None: ...
    def on_changed(self) -> None: ...
