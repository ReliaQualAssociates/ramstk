# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import derating as derating
from ramstk.analyses import stress as stress
from ramstk.analyses.milhdbk217f import milhdbk217f as milhdbk217f
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        ...

    def _do_calculate_cost_metrics(self, node: treelib.Node) -> float:
        ...

    @staticmethod
    def _do_calculate_current_ratio(node: treelib.Node) -> None:
        ...

    def _do_calculate_hardware(self, node_id: int) -> None:
        ...

    def _do_calculate_hazard_rates(self, node: treelib.Node) -> float:
        ...

    def _do_calculate_mtbfs(self, node: treelib.Node) -> float:
        ...

    def _do_calculate_part_count(self, node: treelib.Node) -> int:
        ...

    def _do_calculate_power_dissipation(self, node: treelib.Node) -> float:
        ...

    @staticmethod
    def _do_calculate_power_ratio(node: treelib.Node) -> None:
        ...

    def _do_calculate_reliabilities(self, node: treelib.Node) -> None:
        ...

    @staticmethod
    def _do_calculate_voltage_ratio(node: treelib.Node) -> None:
        ...

    def _do_derating_analysis(self, node_id: int) -> None:
        ...

    @staticmethod
    def _do_predict_active_hazard_rate(node: treelib.Node) -> float:
        ...

    def _request_do_stress_analysis(self, node: treelib.Node) -> None:
        ...
