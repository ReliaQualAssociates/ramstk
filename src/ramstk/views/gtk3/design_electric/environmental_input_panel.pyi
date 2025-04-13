# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class EnvironmentalInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbActiveEnviron: RAMSTKComboBox
    cmbDormantEnviron: RAMSTKComboBox
    txtActiveTemp: RAMSTKEntry
    txtDormantTemp: RAMSTKEntry
    txtDutyCycle: RAMSTKEntry
    txtMissionTime: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def do_load_environment_active(self, environments: list[list[str]]) -> None: ...
    def do_load_environment_dormant(self, environments: list[list[str]]) -> None: ...
