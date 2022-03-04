# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class ConnectionDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_quality: Dict[int, List[List[str]]]
    _dic_type: Dict[int, List[List[str]]]
    _dic_specification: Dict[int, List[List[str]]]
    _lst_insert_A: List[List[str]]
    _lst_insert_B: List[List[str]]
    _lst_insert_C: List[List[str]]
    _lst_insert_D: List[List[str]]
    _dic_insert: Dict[int, Dict[int, List[List[str]]]]
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbInsert: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbSpecification: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtContactGauge: RAMSTKEntry
    txtActivePins: RAMSTKEntry
    txtAmpsContact: RAMSTKEntry
    txtMating: RAMSTKEntry
    txtNWave: RAMSTKEntry
    txtNHand: RAMSTKEntry
    txtNPlanes: RAMSTKEntry
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_load_insert(self, combo: RAMSTKComboBox) -> None: ...
    def _do_load_specification(self, combo: RAMSTKComboBox) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self) -> None: ...
    def __do_set_circular_sensitive(self) -> None: ...
    def __do_set_ic_socket_sensitive(self) -> None: ...
    def __do_set_pwa_edge_sensitive(self) -> None: ...
    def __do_set_pth_sensitive(self) -> None: ...
