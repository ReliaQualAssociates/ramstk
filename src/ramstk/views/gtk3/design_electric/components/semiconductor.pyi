# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_APPLICATION_DICT as SEMICONDUCTOR_APPLICATION_DICT,
)
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_MATCHING_DICT as SEMICONDUCTOR_MATCHING_DICT,
)
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_PACKAGES_LIST as SEMICONDUCTOR_PACKAGES_LIST,
)
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_QUALITY_DICT as SEMICONDUCTOR_QUALITY_DICT,
)
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_TYPE_DICT as SEMICONDUCTOR_TYPE_DICT,
)
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class SemiconductorDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbConstruction: RAMSTKComboBox
    cmbMatching: RAMSTKComboBox
    cmbPackage: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtFrequencyOperating: RAMSTKEntry
    txtNElements: RAMSTKEntry
    txtThetaJC: RAMSTKEntry
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_change_subcategory(self, subcategory_id: int) -> None: ...
    def _do_load_construction(self) -> None: ...
    def _do_load_package(self) -> None: ...
    def _get_quality_list(self) -> list[list[str]]: ...
    def _get_part_count_quality_list(self) -> list[list[str]]: ...
    def _get_type_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
