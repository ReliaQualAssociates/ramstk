# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HardwareGeneralDataPanel(RAMSTKFixedPanel):
    chkRepairable: RAMSTKCheckButton
    cmbCategory: RAMSTKComboBox
    cmbSubcategory: RAMSTKComboBox
    txtAltPartNum: RAMSTKEntry
    txtCompRefDes: RAMSTKEntry
    txtDescription: RAMSTKTextView
    txtFigureNumber: RAMSTKEntry
    txtLCN: RAMSTKEntry
    txtName: RAMSTKEntry
    txtPageNumber: RAMSTKEntry
    txtPartNumber: RAMSTKEntry
    txtRefDes: RAMSTKEntry
    txtSpecification: RAMSTKEntry
    dicSubcategories: dict[int, dict[int, str]]
    def __init__(self) -> None: ...
    def do_load_categories(self, category: dict[int, tuple[str]]) -> None: ...
