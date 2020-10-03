# Standard Library Imports
from typing import Any, List

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.assistants import EditFunction as EditFunction
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

class MethodPanel(RAMSTKPanel):
    cmbSimilarItemMethod: Any = ...
    def __init__(self) -> None: ...

class SimilarItemPanel(RAMSTKPanel):
    def __init__(self) -> None: ...
    def do_load_combobox(self) -> None: ...
    def do_refresh_functions(self, row: Gtk.TreeIter, function: List[str]) -> None: ...
    def do_set_callbacks(self) -> None: ...

class SimilarItem(RAMSTKWorkView):
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None: ...
