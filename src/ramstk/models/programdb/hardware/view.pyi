# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import milhdbk217f as milhdbk217f
from ramstk.models import RAMSTKBaseView as RAMSTKBaseView

class RAMSTKHardwareBoMView(RAMSTKBaseView):
    _tag: str = ...
    _dic_load_functions: Any = ...
    _dic_trees: Any = ...
    _lst_modules: Any = ...
    _hr_multiplier: Any = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_calculate_hardware(self, node_id: int) -> None: ...
    def do_calculate_power_dissipation(self, node_id: int) -> float: ...
    def do_predict_active_hazard_rate(self, node_id: int) -> float: ...
    def _do_load_hardware(self) -> None: ...
    def _do_load_design_electric(self) -> None: ...
    def _do_load_design_mechanic(self) -> None: ...
    def _do_load_milhdbk217f(self) -> None: ...
    def _do_load_nswc(self) -> None: ...
    def _do_load_reliability(self) -> None: ...