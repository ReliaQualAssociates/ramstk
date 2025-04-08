# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class SimilarItemMethodPanel(RAMSTKFixedPanel):
    cmbSimilarItemMethod: RAMSTKComboBox
    method_id: int
    def __init__(self) -> None: ...
