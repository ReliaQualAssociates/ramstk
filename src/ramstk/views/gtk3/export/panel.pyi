# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFileChooserButton as RAMSTKFileChooserButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ExportPanel(RAMSTKFixedPanel):
    btnFileName: Incomplete
    chkRevisions: RAMSTKCheckButton
    chkFunctions: RAMSTKCheckButton
    chkRequirements: RAMSTKCheckButton
    chkHardware: RAMSTKCheckButton
    chkValidation: RAMSTKCheckButton
    chkHazards: RAMSTKCheckButton
    chkStakeholder: RAMSTKCheckButton
    chkAllocation: RAMSTKCheckButton
    chkSimilarItem: RAMSTKCheckButton
    chkFMEA: RAMSTKCheckButton
    chkPoF: RAMSTKCheckButton
    chkUsageProfile: RAMSTKCheckButton
    txtFileName: Incomplete
    def __init__(self, analysis_path: str = "", parent: Gtk.Window = None) -> None: ...
    def do_set_file(self, button) -> None: ...
