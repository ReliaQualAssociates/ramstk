# Standard Library Imports
from datetime import date
from typing import Any

# RAMSTK Package Imports
from ramstk.utilities import none_to_default as none_to_default
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from .widget import WidgetProperties as WidgetProperties

class RAMSTKComboBox(Gtk.ComboBox, RAMSTKBaseWidget):
    _default_height: int
    _default_width: int
    _edit_signal: str
    _index: int
    _n_items: int
    _simple: bool
    def __init__(
        self, index: int = 0, simple: bool = True, n_items: int = 2
    ) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_update(
        self, package: dict[str, bool | date | float | int | str | None]
    ) -> None: ...
    def on_changed(self) -> None: ...
    def do_get_options(self) -> dict[int, Any]: ...
    def do_load_combo(
        self, entries: list[list[str | int]], simple: bool = True
    ) -> None: ...
    def get_value(self, index: int = 0) -> str: ...
