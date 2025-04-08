# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKBaseDialog as RAMSTKBaseDialog
from ramstk.views.gtk3.widgets import RAMSTKBasePanel as RAMSTKBasePanel

# RAMSTK Local Imports
from . import ExportPanel as ExportPanel

class ExportDialog(RAMSTKBaseDialog):
    def __init__(
        self, configuration: RAMSTKUserConfiguration, parent: object = None
    ) -> None: ...
    def do_get_export_information(self) -> tuple[dict[str, bool], str]: ...
