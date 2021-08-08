# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseView

class RAMSTKUsageProfileView(RAMSTKBaseView):
    _root: int = ...
    _tag: str = ...
    _dic_load_functions: Any = ...
    _dic_trees: Any = ...
    _lst_modules: Any = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def _do_load_environments(self, phase_id: int, parent_id: str) -> None: ...
    def _do_load_missions(self) -> None: ...
    def _do_load_mission_phases(self, mission_id: int) -> None: ...
