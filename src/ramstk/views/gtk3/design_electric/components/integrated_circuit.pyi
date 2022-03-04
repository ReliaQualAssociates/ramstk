# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class ICDesignElectricInputPanel(RAMSTKFixedPanel):
    _dic_technology: Dict[int, List[List[str]]]
    _dic_types: Dict[int, List[List[str]]]
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbConstruction: RAMSTKComboBox
    cmbECC: RAMSTKComboBox
    cmbManufacturing: RAMSTKComboBox
    cmbPackage: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbTechnology: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtArea: RAMSTKEntry
    txtFeatureSize: RAMSTKEntry
    txtNActivePins: RAMSTKEntry
    txtNCycles: RAMSTKEntry
    txtNElements: RAMSTKEntry
    txtOperatingLife: RAMSTKEntry
    txtThetaJC: RAMSTKEntry
    txtVoltageESD: RAMSTKEntry
    txtYearsInProduction: RAMSTKEntry
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self) -> None: ...
    def _do_load_application_combo(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_dram_sensitive(self) -> None: ...
    def __do_set_eeprom_sensitive(self) -> None: ...
    def __do_set_gaas_sensitive(self) -> None: ...
    def __do_set_linear_sensitive(self) -> None: ...
    def __do_set_logic_sensitive(self) -> None: ...
    def __do_set_microprocessor_microcontroller_sensitive(self) -> None: ...
    def __do_set_pal_pla_sensitive(self) -> None: ...
    def __do_set_rom_sensitive(self) -> None: ...
    def __do_set_sram_sensitive(self) -> None: ...
    def __do_set_vhsic_vlsi_sensitive(self) -> None: ...
