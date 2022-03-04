# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class InductorDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_insulation: Dict[int, List[List[str]]]
    _dic_quality: Dict[int, List[List[str]]]
    _dic_specifications: Dict[int, List[List[str]]]
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbConstruction: RAMSTKComboBox
    cmbFamily: RAMSTKComboBox
    cmbInsulation: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    txtArea: RAMSTKEntry
    txtWeight: RAMSTKEntry
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_load_panel(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self) -> None: ...
    def __do_load_family_combobox(self) -> None: ...
    def __do_load_insulation_combobox(self) -> None: ...
    def __do_load_quality_combobox(self) -> None: ...
    def __do_load_specification_combobox(self) -> None: ...
