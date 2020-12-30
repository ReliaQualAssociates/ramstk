# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor as improvementfactor
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        ...

    def do_calculate_stakeholder(self, node_id: int) -> None:
        ...

    def _do_calculate_improvement(self) -> None:
        ...
