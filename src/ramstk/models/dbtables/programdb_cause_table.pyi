# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# RAMSTK Package Imports
from ramstk.analyses import criticality as criticality

# RAMSTK Local Imports
from ..dbrecords import RAMSTKCauseRecord as RAMSTKCauseRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKCauseTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKCauseRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKCauseRecord: ...
    def do_calculate_rpn(self, severity: int) -> None: ...
