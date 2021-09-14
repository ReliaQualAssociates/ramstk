# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel

class MilHdbk217FResultPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    lblModel: RAMSTKLabel
    txtLambdaB: RAMSTKEntry
    txtPiQ: RAMSTKEntry
    txtPiE: RAMSTKEntry
    _hazard_rate_method_id: int
    _lambda_b: float
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_entries(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_model_label(self) -> None: ...
