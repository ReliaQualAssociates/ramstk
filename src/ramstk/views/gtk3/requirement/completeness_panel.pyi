# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RequirementCompletenessPanel(RAMSTKFixedPanel):
    chkCompleteQ0: RAMSTKCheckButton
    chkCompleteQ1: RAMSTKCheckButton
    chkCompleteQ2: RAMSTKCheckButton
    chkCompleteQ3: RAMSTKCheckButton
    chkCompleteQ4: RAMSTKCheckButton
    chkCompleteQ5: RAMSTKCheckButton
    chkCompleteQ6: RAMSTKCheckButton
    chkCompleteQ7: RAMSTKCheckButton
    chkCompleteQ8: RAMSTKCheckButton
    chkCompleteQ9: RAMSTKCheckButton
    def __init__(self) -> None: ...
