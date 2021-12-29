# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.analyses import dormancy as dormancy
from ramstk.analyses.statistics import exponential as exponential
from ramstk.analyses.statistics import lognormal as lognormal
from ramstk.analyses.statistics import normal as normal
from ramstk.analyses.statistics import weibull as weibull
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKReliabilityRecord as RAMSTKReliabilityRecord

class RAMSTKReliabilityTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: RAMSTKReliabilityRecord
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Any]
    ) -> RAMSTKReliabilityRecord: ...
