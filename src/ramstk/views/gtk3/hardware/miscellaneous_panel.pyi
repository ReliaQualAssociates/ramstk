# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
    chkTagged: RAMSTKCheckButton
    txtAttachments: RAMSTKTextView
    txtRemarks: RAMSTKTextView
    _lst_widget_configuration: list[WidgetConfig]
    def __init__(self) -> None: ...
