# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKEnvironment as RAMSTKEnvironment
from ramstk.models.programdb import RAMSTKMission as RAMSTKMission
from ramstk.models.programdb import RAMSTKMissionPhase as RAMSTKMissionPhase

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    last_id: Any = ...

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    _revision_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: str) -> None:
        ...

    def _do_delete(self, node_id: int) -> None:
        ...

    def _do_insert_environment(self, mission_id: int, phase_id: int) -> None:
        ...

    def _do_insert_mission(self) -> None:
        ...

    def _do_insert_mission_phase(self, mission_id: int) -> None:
        ...

    def _do_set_attributes(self, node_id: List, package: Dict) -> None:
        ...

    def _do_set_all_attributes(self, attributes: Dict[str, Any],
                               node_id: str) -> None:
        ...
