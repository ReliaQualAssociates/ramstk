# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKValidationRecord as RAMSTKValidationRecord

class RAMSTKValidationTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _dic_status: Any
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_plan(self) -> None: ...
    def _do_calculate_all_tasks(self) -> None: ...
    def _do_calculate_task(self, node_id: int) -> None: ...
    def _do_select_assessment_targets(self) -> pd.DataFrame: ...
