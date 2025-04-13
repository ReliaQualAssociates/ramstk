# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class StressInputPanel(RAMSTKFixedPanel):
    _record_field: str
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
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
