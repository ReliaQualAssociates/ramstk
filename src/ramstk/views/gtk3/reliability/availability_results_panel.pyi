# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class AvailabilityResultsPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    txtCostFailure: RAMSTKEntry
    txtCostHour: RAMSTKEntry
    txtLogisticsAt: RAMSTKEntry
    txtLogisticsAtVar: RAMSTKEntry
    txtMissionAt: RAMSTKEntry
    txtMissionAtVar: RAMSTKEntry
    txtPartCount: RAMSTKEntry
    txtTotalCost: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: dict[str, Any]) -> None: ...
    def _do_load_entries_hardware(self, attributes: dict[str, Any]) -> None: ...
    def __do_nudge_widgets(self) -> None: ...
