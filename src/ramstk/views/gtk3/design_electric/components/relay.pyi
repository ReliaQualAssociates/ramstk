# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class RelayDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_quality: Dict[int, List[List[str]]]
    _dic_pc_types: Dict[int, List[List[str]]]
    _dic_types: Dict[int, List[List[str]]]
    _dic_application: Dict[int, List[List[str]]]
    _dic_construction: Dict[int, Dict[int, List[List[str]]]]
    _lst_technology: List[List[str]]
    _lst_contact_form: List[List[str]]
    _lst_contact_rating: List[List[str]]
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbConstruction: RAMSTKComboBox
    cmbContactForm: RAMSTKComboBox
    cmbContactRating: RAMSTKComboBox
    cmbLoadType: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtCycles: RAMSTKEntry
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self) -> None: ...
    def _on_combo_changed(self, __combo: RAMSTKComboBox, index: int) -> None: ...
    def __do_load_application_combo(self) -> None: ...
    def __do_load_construction_combo(self) -> None: ...
    def __do_load_quality_combo(self) -> None: ...
    def __do_load_type_combo(self) -> None: ...
