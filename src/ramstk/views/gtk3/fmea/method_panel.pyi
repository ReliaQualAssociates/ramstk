# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class FMEAMethodPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
    chkCriticality: RAMSTKCheckButton
    chkRPN: RAMSTKCheckButton
    txtItemCriticality: RAMSTKTextView
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
    def _do_load_item_criticality(self, item_criticality: dict[str, float]) -> None: ...
