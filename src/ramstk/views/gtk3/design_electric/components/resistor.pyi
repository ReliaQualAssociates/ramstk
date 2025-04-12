# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.resistor import (
    RESISTOR_CONSTRUCTION_DICT as RESISTOR_CONSTRUCTION_DICT,
)
from ramstk.constants.resistor import RESISTOR_QUALITY_DICT as RESISTOR_QUALITY_DICT
from ramstk.constants.resistor import (
    RESISTOR_SPECIFICATION_DICT as RESISTOR_SPECIFICATION_DICT,
)
from ramstk.constants.resistor import RESISTOR_STYLE_DICT as RESISTOR_STYLE_DICT
from ramstk.constants.resistor import RESISTOR_TYPE_DICT as RESISTOR_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ResistorDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbConstruction: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    cmbStyle: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtNElements: RAMSTKEntry
    txtResistance: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_change_subcategory(self, subcategory_id: int) -> None: ...
    def _get_quality_list(self) -> list[list[str]]: ...
    def _get_style_list(self) -> list[list[str]]: ...
    def _get_type_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
