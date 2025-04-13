# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.milhdbk217f import (
    MilHdbk217FResultPanel as MilHdbk217FResultPanel,
)
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class ICMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    _lambda_p: str
    _function_1: str
    _function_2: str
    _function_3: Incomplete
    _dic_part_stress: dict[int, str]
    _record_field: str
    _tag: str
    _title: str
    txtC1: RAMSTKEntry
    txtC2: RAMSTKEntry
    txtLambdaBD: RAMSTKEntry
    txtLambdaBP: RAMSTKEntry
    txtLambdaCYC: RAMSTKEntry
    txtLambdaEOS: RAMSTKEntry
    txtPiA: RAMSTKEntry
    txtPiCD: RAMSTKEntry
    txtPiL: RAMSTKEntry
    txtPiMFG: RAMSTKEntry
    txtPiPT: RAMSTKEntry
    txtPiT: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def _do_load_entries(self, attributes: dict[str, Any]) -> None: ...
