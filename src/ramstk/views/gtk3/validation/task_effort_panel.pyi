# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKDateSelectDialog as RAMSTKDateSelectDialog
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ValidationTaskEffortPanel(RAMSTKFixedPanel):
    txtMinTime: RAMSTKEntry
    txtExpTime: RAMSTKEntry
    txtMaxTime: RAMSTKEntry
    txtMinCost: RAMSTKEntry
    txtExpCost: RAMSTKEntry
    txtMaxCost: RAMSTKEntry
    txtMeanTimeLL: RAMSTKEntry
    txtMeanTime: RAMSTKEntry
    txtMeanTimeUL: RAMSTKEntry
    txtMeanCostLL: RAMSTKEntry
    txtMeanCost: RAMSTKEntry
    txtMeanCostUL: RAMSTKEntry
    def __init__(self) -> None: ...
    def do_load_validation_types(
        self, validation_type: dict[int, tuple[str, str]]
    ) -> None: ...
