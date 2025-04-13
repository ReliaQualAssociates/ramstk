# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ReliabilityResultsPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    txtActiveHt: RAMSTKEntry
    txtActiveHtVar: RAMSTKEntry
    txtDormantHt: RAMSTKEntry
    txtDormantHtVar: RAMSTKEntry
    txtLogisticsHt: RAMSTKEntry
    txtLogisticsHtVar: RAMSTKEntry
    txtLogisticsMTBF: RAMSTKEntry
    txtLogisticsMTBFVar: RAMSTKEntry
    txtLogisticsRt: RAMSTKEntry
    txtLogisticsRtVar: RAMSTKEntry
    txtMissionHt: RAMSTKEntry
    txtMissionHtVar: RAMSTKEntry
    txtMissionMTBF: RAMSTKEntry
    txtMissionMTBFVar: RAMSTKEntry
    txtMissionRt: RAMSTKEntry
    txtMissionRtVar: RAMSTKEntry
    txtPercentHt: RAMSTKEntry
    txtSoftwareHt: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: dict[str, Any]) -> None: ...
    def _do_load_entries_hazard_rate(self, attributes: dict[str, Any]) -> None: ...
    def _do_load_entries_mtbf(self, attributes: dict[str, Any]) -> None: ...
    def _do_load_entries_reliability(self, attributes: dict[str, Any]) -> None: ...
    def __do_nudge_widgets(self) -> None: ...
