# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKPlot as RAMSTKPlot
from ramstk.views.gtk3.widgets import RAMSTKScrolledWindow as RAMSTKScrolledWindow
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView

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
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...

class DesignElectricStressResultPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    chkOverstress: RAMSTKCheckButton
    pltPlot: RAMSTKPlot
    txtCurrentRatio: RAMSTKEntry
    txtPowerRatio: RAMSTKEntry
    txtVoltageRatio: RAMSTKEntry
    txtReason: RAMSTKTextView
    _lst_derate_criteria: Any
    _category_id: int
    _part_number: str
    _ref_des: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_derating_curve(
        self, attributes: Dict[str, Any], stress: str = ...
    ) -> None: ...
    def _do_load_entries(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
