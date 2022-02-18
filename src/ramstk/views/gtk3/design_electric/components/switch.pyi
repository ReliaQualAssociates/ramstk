# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class SwitchDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_applications: Dict[int, List[List[str]]]
    _dic_constructions: Dict[int, List[List[str]]]
    _dic_contact_forms: Dict[int, List[List[str]]]
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbConstruction: RAMSTKComboBox
    cmbContactForm: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    txtNCycles: RAMSTKEntry
    txtNElements: RAMSTKEntry
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_construction_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_contact_form_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_cycles_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_elements_sensitive(self, attributes: Dict[str, Any]) -> None: ...
