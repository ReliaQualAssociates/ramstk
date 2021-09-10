# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class DesignElectricEnvironmentalInputPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    cmbActiveEnviron: RAMSTKComboBox
    cmbDormantEnviron: RAMSTKComboBox
    txtActiveTemp: RAMSTKEntry
    txtDormantTemp: RAMSTKEntry
    txtDutyCycle: RAMSTKEntry
    txtMissionTime: RAMSTKEntry
    dic_attribute_index_map: Dict[int, List[str]]
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def do_load_environment_active(self, environments: List[str]) -> None: ...
    def do_load_environment_dormant(self, environments: List[str]) -> None: ...

class DesignElectricStressInputPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    txtTemperatureRatedMin: RAMSTKEntry
    txtTemperatureKnee: RAMSTKEntry
    txtTemperatureRatedMax: RAMSTKEntry
    txtCurrentRated: RAMSTKEntry
    txtCurrentOperating: RAMSTKEntry
    txtPowerRated: RAMSTKEntry
    txtPowerOperating: RAMSTKEntry
    txtVoltageRated: RAMSTKEntry
    txtVoltageAC: RAMSTKEntry
    txtVoltageDC: RAMSTKEntry
    dic_attribute_index_map: Dict[int, List[str]]
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
