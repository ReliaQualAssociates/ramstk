# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.capacitor import CAPACITOR_QUALITY_DICT as CAPACITOR_QUALITY_DICT
from ramstk.constants.capacitor import (
    CAPACITOR_SPECIFICATION_DICT as CAPACITOR_SPECIFICATION_DICT,
)
from ramstk.constants.capacitor import CAPACITOR_STYLE_DICT as CAPACITOR_STYLE_DICT
from ramstk.constants.capacitor import CAPACITOR_STYLE_DICT2 as CAPACITOR_STYLE_DICT2
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class CapacitorDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbConfiguration: RAMSTKComboBox
    cmbConstruction: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    cmbStyle: RAMSTKComboBox
    txtCapacitance: RAMSTKEntry
    txtESR: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_configuration(self) -> None: ...
    def _do_load_construction(self) -> None: ...
    def _do_load_styles(self, combo: RAMSTKComboBox) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _get_quality_list(self) -> list[str | list[str]]: ...
    def _get_style_list(self, combo: RAMSTKComboBox) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
