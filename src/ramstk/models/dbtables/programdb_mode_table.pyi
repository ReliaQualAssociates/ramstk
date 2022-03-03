# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# RAMSTK Package Imports
from ramstk.analyses.criticality import (
    calculate_mode_criticality as calculate_mode_criticality,
)
from ramstk.analyses.criticality import (
    calculate_mode_hazard_rate as calculate_mode_hazard_rate,
)

# RAMSTK Local Imports
from ..dbrecords import RAMSTKModeRecord as RAMSTKModeRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKModeTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKModeRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKModeRecord: ...
    def do_calculate_criticality(self, item_hr: float) -> None: ...
