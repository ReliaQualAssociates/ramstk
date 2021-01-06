# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import allocation as allocation
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    _system_hazard_rate: float = ...
    _node_hazard_rate: float = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        ...

    def _do_calculate_agree_allocation(self, node: treelib.Node) -> None:
        ...

    def _do_calculate_agree_total_elements(
            self, node: treelib.Node) -> Tuple[int, int]:
        ...

    def _do_calculate_allocation(self, node_id: int) -> None:
        ...

    @staticmethod
    def _do_calculate_allocation_goals(node: treelib.Node) -> None:
        ...

    def _do_calculate_arinc_allocation(self, node: treelib.Node) -> None:
        ...

    def _do_calculate_arinc_weight_factor(self, node: treelib.Node) -> float:
        ...

    def _do_calculate_equal_allocation(self, node: treelib.Node) -> None:
        ...

    def _do_calculate_foo_allocation(self, node: treelib.Node) -> None:
        ...

    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int:
        ...

    def _do_get_allocation_goal(self) -> Dict[str, Any]:
        ...

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        ...
