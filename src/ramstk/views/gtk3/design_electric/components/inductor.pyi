# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.inductor import (
    INDUCTOR_INSULATION_DICT as INDUCTOR_INSULATION_DICT,
)
from ramstk.constants.inductor import INDUCTOR_QUALITY_DICT as INDUCTOR_QUALITY_DICT
from ramstk.constants.inductor import (
    INDUCTOR_SPECIFICATION_DICT as INDUCTOR_SPECIFICATION_DICT,
)
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

PART_COUNT: int
PART_STRESS: int

class InductorDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbConstruction: RAMSTKComboBox
    cmbFamily: RAMSTKComboBox
    cmbInsulation: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    txtArea: RAMSTKEntry
    txtWeight: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_construction(self) -> None: ...
    def _do_load_panel(self, attributes: dict[str, Any]) -> None: ...
    def _get_family_list(self) -> list[list[str]]: ...
    def _get_quality_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
