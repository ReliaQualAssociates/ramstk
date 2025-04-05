# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets.dialogs.base_dialog import (
    RAMSTKBaseDialog as RAMSTKBaseDialog,
)

class RAMSTKMessageDialog(Gtk.MessageDialog, RAMSTKBaseDialog):
    def __init__(
        self, title: str, parent: object, buttons: tuple[Any, Any, Any, Any] = ...
    ) -> None: ...
    def do_set_message(self, message: str) -> None: ...
    def do_set_message_type(self, message_type: str = "error") -> None: ...
