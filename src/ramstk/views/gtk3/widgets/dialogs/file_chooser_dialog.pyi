# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets.dialogs.base_dialog import (
    RAMSTKBaseDialog as RAMSTKBaseDialog,
)

class RAMSTKFileChooserDialog(Gtk.FileChooserDialog, RAMSTKBaseDialog):
    def __init__(
        self, title: str, parent: object, buttons: tuple[Any, Any, Any, Any] = ...
    ) -> None: ...
    def do_run(self) -> tuple[str | None, str | None]: ...
    def do_set_file_filters(self, filters: Incomplete | None = None) -> None: ...
