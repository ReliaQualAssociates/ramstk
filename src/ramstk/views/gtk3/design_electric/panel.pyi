# Standard Library Imports
from typing import Any, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKScrolledWindow as RAMSTKScrolledWindow

class DesignElectricInputPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Any
    cmbActiveEnviron: Any
    cmbDormantEnviron: Any
    scwDesignRatings: Any
    txtActiveTemp: Any
    txtDormantTemp: Any
    txtDutyCycle: Any
    txtMissionTime: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_environment_active(self, environments: List[str]) -> None: ...
    def do_load_environment_dormant(self, environments: List[str]) -> None: ...
