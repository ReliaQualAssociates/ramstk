# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.constants.integrated_circuit import IC_TECHNOLOGY_DICT as IC_TECHNOLOGY_DICT
from ramstk.constants.integrated_circuit import IC_TYPE_DICT as IC_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ICDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
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
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_application(self, attributes: dict[str, Any]) -> None: ...
    def _do_load_construction(self) -> None: ...
    def _do_load_ecc(self) -> None: ...
    def _do_load_manufacturing(self) -> None: ...
    def _do_load_package(self) -> None: ...
    def _do_load_quality(self) -> None: ...
    @staticmethod
    def _get_application_list(construction_id: int) -> list[list[str]]: ...
    def _get_part_count_technology_list(self) -> list[list[str]]: ...
    def _get_technology_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
