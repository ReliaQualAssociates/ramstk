# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKFileChooser as RAMSTKFileChooser
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog as RAMSTKMessageDialog
)

class ExportProject(RAMSTKFileChooser):
    RAMSTK_USER_CONFIGURATION: Any = ...
    _parent: Any = ...

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        ...

    def _do_quit(self) -> None:
        ...

    def _do_select_file(self) -> None:
        ...
