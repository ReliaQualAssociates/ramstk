# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor as improvementfactor

# RAMSTK Local Imports
from ..dbrecords import RAMSTKStakeholderRecord as RAMSTKStakeholderRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKStakeholderTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKStakeholderRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKStakeholderRecord: ...
    def do_calculate_stakeholder(self, node_id: int) -> None: ...
    def _do_calculate_improvement(self, node_id: int) -> None: ...
