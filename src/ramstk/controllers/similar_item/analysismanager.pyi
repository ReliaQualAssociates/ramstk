# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import similaritem as similaritem
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    _dic_hardware_hrs: Any = ...
    _node_hazard_rate: float = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        ...

    def _do_calculate_similar_item(self, node_id: int) -> None:
        ...

    def _do_calculate_topic_633(self, node: treelib.Node) -> None:
        ...

    def _do_calculate_user_defined(self, node: treelib.Node) -> None:
        ...

    def _do_roll_up_change_descriptions(self, node: treelib.Node) -> None:
        ...

    def _on_get_hardware_attributes(self, tree: Any) -> None:
        ...
