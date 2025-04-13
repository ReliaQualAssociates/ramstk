# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.connection import CONNECTION_INSERT_DICT as CONNECTION_INSERT_DICT
from ramstk.constants.connection import (
    CONNECTION_QUALITY_DICT as CONNECTION_QUALITY_DICT,
)
from ramstk.constants.connection import (
    CONNECTION_SPECIFICATION_DICT as CONNECTION_SPECIFICATION_DICT,
)
from ramstk.constants.connection import CONNECTION_TYPE_DICT as CONNECTION_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ConnectionDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbInsert: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtContactGauge: RAMSTKEntry
    txtActivePins: RAMSTKEntry
    txtAmpsContact: RAMSTKEntry
    txtMating: RAMSTKEntry
    txtNWave: RAMSTKEntry
    txtNHand: RAMSTKEntry
    txtNPlanes: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_insert(self, combo: RAMSTKComboBox) -> None: ...
    def _do_load_specification(self, combo: RAMSTKComboBox) -> None: ...
    def _get_quality_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
