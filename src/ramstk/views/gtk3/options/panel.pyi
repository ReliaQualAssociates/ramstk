# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class OptionsPanel(RAMSTKFixedPanel):
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
    txtSiteID: RAMSTKEntry
    txtSiteName: RAMSTKEntry
    txtProductKey: RAMSTKEntry
    txtExpireDate: RAMSTKEntry
    def __init__(self) -> None: ...
