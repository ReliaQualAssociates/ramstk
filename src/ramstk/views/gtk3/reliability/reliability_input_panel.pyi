# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ReliabilityInputPanel(RAMSTKFixedPanel):
    _record_field: str
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
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def do_load_hr_distributions(self, distributions: list[list[str]]) -> None: ...
    def do_load_hr_methods(self, methods: list[list[str]]) -> None: ...
    def do_load_hr_types(self, hr_types: list[list[str]]) -> None: ...
    def _set_sensitive(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive_assessed(self, type_id: int) -> None: ...
    def _set_sensitive_specified_ht(self, type_id: int) -> None: ...
    def _set_sensitive_specified_mtbf(self, type_id: int) -> None: ...
    def _set_sensitive_specified_distribution(self, type_id: int) -> None: ...
