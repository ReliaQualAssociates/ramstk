# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.analyses import derating as derating
from ramstk.analyses import stress as stress
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKDesignElectricRecord as RAMSTKDesignElectricRecord

class RAMSTKDesignElectricTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: RAMSTKDesignElectricRecord
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
