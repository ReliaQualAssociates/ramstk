# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Type, Union

# Third Party Imports
import pandas as pd

# RAMSTK Local Imports
from ..dbrecords import RAMSTKValidationRecord as RAMSTKValidationRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKValidationTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _dic_status: Dict[Any, float]
    _lst_id_columns: List[str]
    _record: Type[RAMSTKValidationRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKValidationRecord: ...
    def do_calculate_plan(self) -> None: ...
    def _do_calculate_all_tasks(self) -> None: ...
    def _do_calculate_task(self, node_id: int) -> None: ...
    def _do_select_assessment_targets(self) -> pd.DataFrame: ...
