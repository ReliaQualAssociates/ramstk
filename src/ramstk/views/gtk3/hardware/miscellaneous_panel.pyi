# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    chkTagged: RAMSTKCheckButton
    txtAttachments: RAMSTKTextView
    txtRemarks: RAMSTKTextView
    def __init__(self) -> None: ...
