# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RequirementVerifiabilityPanel(RAMSTKFixedPanel):
    chkVerifiableQ0: RAMSTKCheckButton
    chkVerifiableQ1: RAMSTKCheckButton
    chkVerifiableQ2: RAMSTKCheckButton
    chkVerifiableQ3: RAMSTKCheckButton
    chkVerifiableQ4: RAMSTKCheckButton
    chkVerifiableQ5: RAMSTKCheckButton
    def __init__(self) -> None: ...
