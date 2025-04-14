# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.milhdbk217f import (
    MilHdbk217FResultPanel as MilHdbk217FResultPanel,
)
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class SwitchMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    _dic_part_stress: dict[int, str]
    _record_field: str
    _tag: str
    _title: str
    txtPiC: RAMSTKEntry
    txtPiCYC: RAMSTKEntry
    txtPiL: RAMSTKEntry
    txtPiN: RAMSTKEntry
    txtPiU: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: dict[str, Any]) -> None: ...
