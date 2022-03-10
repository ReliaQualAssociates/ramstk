# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple, Type, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import allocation as allocation

# RAMSTK Local Imports
from ..dbrecords import RAMSTKAllocationRecord as RAMSTKAllocationRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKAllocationTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _system_hazard_rate: float
    _lst_id_columns: List[str]
    _node_hazard_rate: float
    _record: Type[RAMSTKAllocationRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    _parent_id: int
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKAllocationRecord: ...
    def do_calculate_allocation_goals(self, node_id: int) -> None: ...
    def do_calculate_agree_allocation(
        self, node_id: int, duty_cycle: float
    ) -> None: ...
    def do_calculate_arinc_allocation(self, node_id: int) -> None: ...
    def do_calculate_equal_allocation(self, node_id: int) -> None: ...
    def do_calculate_foo_allocation(self, node_id: int) -> None: ...
    def _do_calculate_agree_total_elements(self, node_id: int) -> Tuple[int, int]: ...
    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int: ...
    def _on_insert_hardware(self, tree: treelib.Tree) -> None: ...
