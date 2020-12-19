# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3.failure_definition import (
    lvwFailureDefinition as lvwFailureDefinition
)
from ramstk.views.gtk3.function import (
    mtxFunctionHardware as mtxFunctionHardware
)
from ramstk.views.gtk3.hardware import (
    mtxHardwareRequirement as mtxHardwareRequirement
)
from ramstk.views.gtk3.hardware import (
    mtxHardwareValidation as mtxHardwareValidation
)
from ramstk.views.gtk3.requirement import (
    mtxRequirementHardware as mtxRequirementHardware
)
from ramstk.views.gtk3.stakeholder import lvwStakeholders as lvwStakeholders
from ramstk.views.gtk3.usage_profile import lvwUsageProfile as lvwUsageProfile
from ramstk.views.gtk3.validation import (
    mtxValidationRequirement as mtxValidationRequirement
)
from ramstk.views.gtk3.widgets import RAMSTKBaseBook as RAMSTKBaseBook

class RAMSTKListBook(RAMSTKBaseBook):
    _dic_list_views: Any = ...
    _module: str = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _on_close(self) -> None:
        ...

    def _on_module_change(self, module: str = ...) -> None:
        ...
