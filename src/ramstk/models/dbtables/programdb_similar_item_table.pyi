# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.analyses import similaritem as similaritem
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from ..dbrecords import RAMSTKSimilarItemRecord as RAMSTKSimilarItemRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKSimilarItemTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _node_hazard_rate: float
    _record: Type[RAMSTKSimilarItemRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    _parent_id: int
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKSimilarItemRecord: ...
    def do_calculate_similar_item(self, node_id: int) -> None: ...
    def do_roll_up_change_descriptions(self, node_id: int) -> None: ...
    def _do_calculate_topic_633(self, node_id: int) -> None: ...
    def _do_calculate_user_defined(self, node_id: int) -> None: ...
    def _on_insert_hardware(self, tree: treelib.Tree) -> None: ...
