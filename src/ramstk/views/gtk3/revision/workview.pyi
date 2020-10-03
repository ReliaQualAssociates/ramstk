# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

class GeneralDataPanel(RAMSTKPanel):
    txtCode: Any = ...
    txtName: Any = ...
    txtRemarks: Any = ...
    def __init__(self) -> None: ...

class GeneralData(RAMSTKWorkView):
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None: ...
