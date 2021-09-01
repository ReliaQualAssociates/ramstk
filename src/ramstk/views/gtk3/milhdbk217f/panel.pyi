# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class MilHdbk217FInputPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Any
    cmbQuality: Any
    _dic_component_panels: Any
    _lst_labels: Any
    _lst_tooltips: Any
    _hazard_rate_method_id: int
    _subcategory_id: int
    def __init__(self) -> None: ...
    _record_id: Any
    def do_load_common(self, attributes: Dict[str, Any]) -> None: ...
    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None: ...
