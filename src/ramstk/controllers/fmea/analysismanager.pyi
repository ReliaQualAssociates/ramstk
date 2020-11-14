# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import criticality as criticality
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        ...

    def _do_calculate_criticality(self, item_hr: float) -> None:
        ...

    def _do_calculate_rpn(self, method: str = ...) -> None:
        ...

    def __do_calculate_rpn(self, mode: treelib.Node, sod: Dict[str, int],
                           method: str) -> None:
        ...
