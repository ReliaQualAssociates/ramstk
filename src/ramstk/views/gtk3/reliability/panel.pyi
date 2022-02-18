# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class ReliabilityInputPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    cmbFailureDist: RAMSTKComboBox
    cmbHRMethod: RAMSTKComboBox
    cmbHRType: RAMSTKComboBox
    txtAddAdjFactor: RAMSTKEntry
    txtFailLocation: RAMSTKEntry
    txtFailScale: RAMSTKEntry
    txtFailShape: RAMSTKEntry
    txtMultAdjFactor: RAMSTKEntry
    txtSpecifiedHt: RAMSTKEntry
    txtSpecifiedHtVar: RAMSTKEntry
    txtSpecifiedMTBF: RAMSTKEntry
    txtSpecifiedMTBFVar: RAMSTKEntry
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def do_load_hr_distributions(self, distributions: List[str]) -> None: ...
    def do_load_hr_methods(self, methods: List[str]) -> None: ...
    def do_load_hr_types(self, hr_types: List[str]) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive_assessed(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_ht(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_mtbf(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_distribution(self, type_id: int) -> None: ...

class ReliabilityResultsPanel(RAMSTKFixedPanel):
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
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: Dict[str, Any]) -> None: ...
    def _do_load_entries_hazard_rate(self, attributes: Dict[str, Any]) -> None: ...
    def _do_load_entries_mtbf(self, attributes: Dict[str, Any]) -> None: ...
    def _do_load_entries_reliability(self, attributes: Dict[str, Any]) -> None: ...
    def __do_nudge_widgets(self) -> None: ...

class AvailabilityResultsPanel(RAMSTKFixedPanel):
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
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: Dict[str, Any]) -> None: ...
    def _do_load_entries_hardware(self, attributes: Dict[str, Any]) -> None: ...
    def __do_nudge_widgets(self) -> None: ...
