# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk

class RAMSTKBaseBook(Gtk.Notebook):
    RAMSTK_SITE_CONFIGURATION: Any = ...
    dic_tab_position: Any = ...
    dic_handler_id: Any = ...
    RAMSTK_USER_CONFIGURATION: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration) -> None:
        ...

    def _set_properties(self, book: str) -> None:
        ...
