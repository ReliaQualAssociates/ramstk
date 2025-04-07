# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class AllocationGoalMethodPanel(RAMSTKFixedPanel):
    cmbAllocationGoal: RAMSTKComboBox
    cmbAllocationMethod: RAMSTKComboBox
    txtHazardRateGoal: RAMSTKEntry
    txtMTBFGoal: RAMSTKEntry
    txtReliabilityGoal: RAMSTKEntry
    method_id: int
    def __init__(self) -> None: ...
