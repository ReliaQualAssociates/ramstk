# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable

class RAMSTKSimilarItemTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: Any
    _node_hazard_rate: float
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    _parent_id: Any
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_similar_item(self, node_id: int) -> None: ...
    def do_roll_up_change_descriptions(self, node_id: int) -> None: ...
    def _do_calculate_topic_633(self, node_id: int) -> None: ...
    def _do_calculate_user_defined(self, node_id: int) -> None: ...
