# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class ResistorDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_quality: Dict[int, List[List[str]]]
    _dic_specifications: Dict[int, List[List[str]]]
    _dic_types: Dict[int, List[List[str]]]
    _dic_styles: Dict[int, Dict[int, List[List[str]]]]
    _dic_construction: Dict[int, List[List[str]]]
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
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_construction_combo(self) -> None: ...
    def __do_load_quality_combo(self) -> None: ...
    def __do_load_specification_combo(self) -> None: ...
    def __do_load_style_combo(self) -> None: ...
    def __do_load_type_combo(self) -> None: ...
    def __do_set_construction_combo_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_elements_entry_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_specification_combo_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_style_combo_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_type_combo_sensitive(self, attributes: Dict[str, Any]) -> None: ...
