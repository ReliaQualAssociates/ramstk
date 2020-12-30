# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3.allocation import wvwAllocation as wvwAllocation
from ramstk.views.gtk3.fmea import wvwFMEA as wvwFMEA
from ramstk.views.gtk3.function import wvwFunctionGD as wvwFunctionGD
from ramstk.views.gtk3.hardware import wvwHardwareAI as wvwHardwareAI
from ramstk.views.gtk3.hardware import wvwHardwareAR as wvwHardwareAR
from ramstk.views.gtk3.hardware import wvwHardwareGD as wvwHardwareGD
from ramstk.views.gtk3.hazard_analysis import wvwHazOps as wvwHazOps
from ramstk.views.gtk3.pof import wvwPoF as wvwPoF
from ramstk.views.gtk3.requirement import (
    wvwRequirementAnalysis as wvwRequirementAnalysis
)
from ramstk.views.gtk3.requirement import wvwRequirementGD as wvwRequirementGD
from ramstk.views.gtk3.revision import wvwRevisionGD as wvwRevisionGD
from ramstk.views.gtk3.similar_item import wvwSimilarItem as wvwSimilarItem
from ramstk.views.gtk3.validation import wvwBurndownCurve as wvwBurndownCurve
from ramstk.views.gtk3.validation import wvwValidationGD as wvwValidationGD
from ramstk.views.gtk3.widgets import RAMSTKBaseBook as RAMSTKBaseBook
from ramstk.views.gtk3.widgets import RAMSTKBaseView as RAMSTKBaseView

class RAMSTKWorkBook(RAMSTKBaseBook):
    dic_work_views: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _on_module_change(self, module: str = ...) -> None:
        ...
