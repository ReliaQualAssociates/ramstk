# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class AllocationGoalMethodPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
    cmbAllocationGoal: RAMSTKComboBox
    cmbAllocationMethod: RAMSTKComboBox
    txtHazardRateGoal: RAMSTKEntry
    txtMTBFGoal: RAMSTKEntry
    txtReliabilityGoal: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _goal_id: int
    method_id: int
    def __init__(self) -> None: ...
    def _do_load_allocation_goal(self) -> None: ...
    def _do_load_allocation_methods(self) -> None: ...
    def _do_set_sensitive(self, attributes: dict[str, float | int | str]) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _on_goal_changed(self, combo: RAMSTKComboBox) -> None: ...
    def _on_method_changed(self, combo: RAMSTKComboBox) -> None: ...
