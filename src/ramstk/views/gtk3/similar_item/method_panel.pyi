# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class SimilarItemMethodPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
    cmbSimilarItemMethod: RAMSTKComboBox
    _lst_widget_configuration: list[WidgetConfig]
    _method_id: int
    _on_edit_message: Incomplete
    method_id: int
    def __init__(self) -> None: ...
    def _do_load_methods(self) -> None: ...
    def _do_set_sensitive(self, attributes: dict[str, int | float | str]) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _on_method_changed(self, combo: RAMSTKComboBox) -> None: ...
