# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RequirementConsistencyPanel(RAMSTKFixedPanel):
    chkConsistentQ0: RAMSTKCheckButton
    chkConsistentQ1: RAMSTKCheckButton
    chkConsistentQ2: RAMSTKCheckButton
    chkConsistentQ3: RAMSTKCheckButton
    chkConsistentQ4: RAMSTKCheckButton
    chkConsistentQ5: RAMSTKCheckButton
    chkConsistentQ6: RAMSTKCheckButton
    chkConsistentQ7: RAMSTKCheckButton
    chkConsistentQ8: RAMSTKCheckButton
    def __init__(self) -> None: ...
