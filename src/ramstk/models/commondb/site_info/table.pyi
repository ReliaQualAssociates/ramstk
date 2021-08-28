# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKSiteInfoRecord as RAMSTKSiteInfoRecord

class RAMSTKSiteInfoTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _tag: str
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs) -> None: ...
