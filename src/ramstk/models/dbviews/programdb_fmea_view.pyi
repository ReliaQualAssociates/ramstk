# Standard Library Imports
from typing import Callable, Dict, List, Union

# Third Party Imports
import treelib

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView as RAMSTKBaseView

class RAMSTKFMEAView(RAMSTKBaseView):
    _root: int
    _tag: str
    _dic_load_functions: Dict[str, Callable[..., object]]
    _dic_trees: Dict[str, treelib.Tree]
    _lst_modules: List[str]
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def _do_load_modes(self) -> None: ...
    def _do_load_mechanisms(self, mode_id: int) -> None: ...
    def _do_load_causes(self, mechanism_id: int, parent_id: str) -> None: ...
    def _do_load_controls(self, cause_id: int, parent_id: str) -> None: ...
    def _do_load_actions(self, cause_id: int, parent_id: str) -> None: ...
