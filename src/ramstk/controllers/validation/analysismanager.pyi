# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    _status_tree: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        ...

    def do_calculate_plan(self) -> None:
        ...

    def _do_calculate_all_tasks(self) -> None:
        ...

    def _do_calculate_task(self, node_id: int) -> None:
        ...

    _tree: Any = ...

    def _do_request_status_tree(self, tree: treelib.Tree) -> None:
        ...

    def _do_select_actual_status(self) -> pd.DataFrame:
        ...

    def _do_select_assessment_targets(self) -> pd.DataFrame:
        ...

    def _on_get_status_tree(self, tree: treelib.Tree) -> None:
        ...
