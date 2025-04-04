# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from .widget import WidgetProperties as WidgetProperties

class RAMSTKLabel(Gtk.Label, RAMSTKBaseWidget):
    def __init__(self, text: str) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_update(
        self, package: dict[str, bool | date | float | int | str]
    ) -> None: ...

def do_make_label_group(text: list[str]) -> tuple[int, list[RAMSTKLabel]]: ...
