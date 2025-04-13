# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKPlot as RAMSTKPlot
from ramstk.views.gtk3.widgets import RAMSTKScrolledWindow as RAMSTKScrolledWindow
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class StressResultPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    chkOverstress: RAMSTKCheckButton
    pltPlot: RAMSTKPlot
    txtCurrentRatio: RAMSTKEntry
    txtPowerRatio: RAMSTKEntry
    txtVoltageRatio: RAMSTKEntry
    txtReason: RAMSTKTextView
    _lst_widget_configuration: list[WidgetConfig]
    _lst_derate_criteria: list[list[float]]
    _category_id: int
    _part_number: str
    _ref_des: str
    def __init__(self) -> None: ...
    def _do_load_derating_curve(
        self, attributes: dict[str, Any], stress: str = "voltage"
    ) -> None: ...
    def _do_load_entries(self, attributes: dict[str, Any]) -> None: ...
    def _do_set_hardware_attributes(self, attributes: dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
