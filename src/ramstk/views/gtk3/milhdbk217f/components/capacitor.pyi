# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry

class CapacitorMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    _dic_part_stress: Dict[int, str]
    _title: str
    txtPiCV: RAMSTKEntry
    txtPiCF: RAMSTKEntry
    txtPiC: RAMSTKEntry
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: Dict[str, Any]) -> None: ...
