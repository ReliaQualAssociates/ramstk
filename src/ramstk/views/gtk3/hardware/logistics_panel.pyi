# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HardwareLogisticsPanel(RAMSTKFixedPanel):
    cmbCostType: RAMSTKComboBox
    cmbManufacturer: RAMSTKComboBox
    txtCAGECode: RAMSTKEntry
    txtCost: RAMSTKEntry
    txtNSN: RAMSTKEntry
    txtQuantity: RAMSTKEntry
    txtYearMade: RAMSTKEntry
    def __init__(self) -> None: ...
    def do_load_cost_types(self) -> None: ...
    def do_load_manufacturers(
        self, manufacturers: dict[int, list[list[str | int]]]
    ) -> None: ...
