# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.constants.relay import RELAY_APPLICATION_DICT as RELAY_APPLICATION_DICT
from ramstk.constants.relay import RELAY_CONSTRUCTION_DICT as RELAY_CONSTRUCTION_DICT
from ramstk.constants.relay import RELAY_CONTACT_FORM_LIST as RELAY_CONTACT_FORM_LIST
from ramstk.constants.relay import (
    RELAY_CONTACT_RATING_LIST as RELAY_CONTACT_RATING_LIST,
)
from ramstk.constants.relay import RELAY_QUALITY_DICT as RELAY_QUALITY_DICT
from ramstk.constants.relay import RELAY_TECHNOLOGY_LIST as RELAY_TECHNOLOGY_LIST
from ramstk.constants.relay import RELAY_TYPE_DICT as RELAY_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RelayDesignElectricInputPanel(RAMSTKFixedPanel):
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
    _lst_widget_configuration: list[WidgetConfig]
    _hazard_rate_method_id: int
    _quality_id: int
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def on_subcategory_change(self, subcategory_id: int) -> None: ...
    def _do_load_application(self) -> None: ...
    def _do_load_construction(self) -> None: ...
    def _do_load_contact_form(self) -> None: ...
    def _do_load_contact_rating(self) -> None: ...
    def _do_load_technology(self) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _get_application_list(self) -> list[list[str]]: ...
    def _get_construction_list(self) -> list[list[str]]: ...
    def _get_quality_list(self) -> list[list[str]]: ...
    def _set_reliability_attributes(self, attributes: dict[str, Any]) -> None: ...
    def _set_sensitive(self) -> None: ...
