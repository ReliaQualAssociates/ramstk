# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ValidationTreePanel(RAMSTKTreePanel):
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit: dict[int, tuple[str, str]]
    ) -> None: ...
    def do_load_verification_types(
        self, verification_type: dict[int, tuple[str, str]]
    ) -> None: ...
