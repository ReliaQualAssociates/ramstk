# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RequirementClarityPanel(RAMSTKFixedPanel):
    chkClarityQ0: RAMSTKCheckButton
    chkClarityQ1: RAMSTKCheckButton
    chkClarityQ2: RAMSTKCheckButton
    chkClarityQ3: RAMSTKCheckButton
    chkClarityQ4: RAMSTKCheckButton
    chkClarityQ5: RAMSTKCheckButton
    chkClarityQ6: RAMSTKCheckButton
    chkClarityQ7: RAMSTKCheckButton
    chkClarityQ8: RAMSTKCheckButton
    def __init__(self) -> None: ...
