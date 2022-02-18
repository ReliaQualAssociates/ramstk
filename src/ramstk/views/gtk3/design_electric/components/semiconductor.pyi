# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class SemiconductorDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_quality: Dict[int, List[List[str]]]
    _dic_types: Dict[int, List[List[str]]]
    _dic_applications: Dict[int, List[List[str]]]
    _dic_matchings: Dict[int, List[List[str]]]
    _lst_packages: List[List[str]]
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
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_application(self) -> None: ...
    def __do_load_construction(self) -> None: ...
    def __do_load_matching(self) -> None: ...
    def __do_load_quality(self) -> None: ...
    def __do_load_type(self) -> None: ...
    def __do_set_application_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_construction_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_elements_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_matching_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_op_freq_sensitive(
        self, attributes: Dict[str, Any]
    ) -> None: ...
    def __do_set_type_sensitive(self, attributes: Dict[str, Any]) -> None: ...
