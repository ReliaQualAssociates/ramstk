# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.assistants import (
    AddStressTestMethod as AddStressTestMethod
)
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

def get_indenture_level(record_id: str) -> str:
    ...


class PoFPanel(RAMSTKPanel):
    dic_damage_models: Any = ...
    dic_icons: Any = ...
    dic_load_history: Any = ...
    dic_measurable_parameters: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_combobox(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...


class PoF(RAMSTKWorkView):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...
