# Standard Library Imports
from typing import Callable, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView as RAMSTKBaseView

class RAMSTKUsageProfileView(RAMSTKBaseView):
    _tag: str
    _dic_load_functions: Dict[str, Callable[..., object]]
    _dic_trees: Dict[str, treelib.Tree]
    _lst_modules: List[str]
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def _do_load_environments(self, mission_phase_id: int, parent_id: str) -> None: ...
    def _do_load_missions(self) -> None: ...
    def _do_load_mission_phases(self, mission_id: int) -> None: ...
