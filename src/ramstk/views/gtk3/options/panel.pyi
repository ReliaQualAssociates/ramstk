# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class OptionsPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
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
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
