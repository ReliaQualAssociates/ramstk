# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class CapacitorDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_quality: Dict[int, List[Any]]
    _dic_specifications: Dict[int, List[Any]]
    _dic_styles: Dict[int, List[Any]]
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
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_load_styles(self, combo: RAMSTKComboBox) -> None: ...
    def _do_set_sensitive(self) -> None: ...
    def __do_set_parts_count_sensitive(self) -> None: ...
    def __do_set_part_stress_sensitive(self) -> None: ...
