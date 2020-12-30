# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.analyses import allocation as allocation
from ramstk.analyses import derating as derating
from ramstk.analyses import dormancy as dormancy
from ramstk.analyses import similaritem as similaritem
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

    def _do_calculate_agree_total_elements(self, node_id: int) -> None:
        ...

    def _do_calculate_all_hardware(self, node_id: int) -> List[float]:
        ...

    _attributes: Any = ...

    def _do_calculate_allocation_goals(self) -> None:
        ...

    def _do_calculate_allocation(self, node_id: int) -> None:
        ...

    def _do_calculate_arinc_weight_factor(self, node_id: int) -> None:
        ...

    def _do_calculate_cost_metrics(self) -> None:
        ...

    def _do_calculate_current_ratio(self) -> None:
        ...

    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int:
        ...

    def _do_calculate_hardware(self, node_id: int, system: bool = ...) -> None:
        ...

    def _do_calculate_hazard_rate_metrics(self) -> None:
        ...

    def _do_calculate_mtbf_metrics(self) -> None:
        ...

    def _do_calculate_power_ratio(self) -> None:
        ...

    def _do_calculate_reliability_metrics(self) -> None:
        ...

    def _do_calculate_similar_item(self, node_id: int) -> None:
        ...

    def _do_calculate_topic_633(self) -> None:
        ...

    def _do_calculate_user_defined(self) -> None:
        ...

    def _do_calculate_voltage_ratio(self) -> None:
        ...

    def _do_derating_analysis(self, node_id: int) -> None:
        ...

    def _do_get_allocation_goal(self) -> Dict[str, Any]:
        ...

    def _do_roll_up_change_descriptions(self, node_id: int) -> None:
        ...

    def _on_allocate_reliability(self, attributes: Dict[str, Any]) -> None:
        ...

    def _on_predict_reliability(self, attributes: Dict[str, Any]) -> None:
        ...

    def _request_do_calculate_all_hardware(self) -> None:
        ...

    def _request_do_predict_active_hazard_rate(self) -> None:
        ...

    def _request_do_stress_analysis(self) -> None:
        ...
