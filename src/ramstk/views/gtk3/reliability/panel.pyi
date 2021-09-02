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
    _title: Any
    cmbFailureDist: Any
    cmbHRMethod: Any
    cmbHRType: Any
    txtAddAdjFactor: Any
    txtFailLocation: Any
    txtFailScale: Any
    txtFailShape: Any
    txtMultAdjFactor: Any
    txtSpecifiedHt: Any
    txtSpecifiedHtVar: Any
    txtSpecifiedMTBF: Any
    txtSpecifiedMTBFVar: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_hr_distributions(self, distributions: List[str]) -> None: ...
    def do_load_hr_methods(self, methods: List[str]) -> None: ...
    def do_load_hr_types(self, hr_types: List[str]) -> None: ...
    def _do_set_sensitive_assessed(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_ht(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_mtbf(self, type_id: int) -> None: ...
    def _do_set_sensitive_specified_distribution(self, type_id: int) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
