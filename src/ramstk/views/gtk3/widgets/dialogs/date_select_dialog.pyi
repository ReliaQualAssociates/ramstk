# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from . import RAMSTKBaseDialog as RAMSTKBaseDialog

class RAMSTKDateSelectDialog(RAMSTKBaseDialog):
    def __init__(
        self, title: str, parent: object, buttons: tuple[Any, Any, Any, Any] = ...
    ) -> None: ...
    def do_run(self) -> str: ...
