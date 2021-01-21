# Standard Library Imports
from typing import Any, Optional

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKDialog as RAMSTKDialog
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel

class AddStressTestMethod(RAMSTKDialog):
    rdoOpStress: Any = ...
    rdoTestMethod: Any = ...

    def __init__(self, parent: Optional[Any] = ...) -> None:
        ...

    def _cancel(self, __button: Gtk.Button) -> None:
        ...

    def __make_ui(self) -> None:
        ...
