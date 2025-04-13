# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class MiscDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtFrequency: RAMSTKEntry
    txtUtilization: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _duty_cycle: float
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_application(self) -> None: ...
    def _do_load_quality(self) -> None: ...
    def _do_load_type(self) -> None: ...
    def _get_type_list(self) -> list[list[str]]: ...
    def _set_hardware_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
