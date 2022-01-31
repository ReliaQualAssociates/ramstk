# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable, RAMSTKSubCategoryRecord

class RAMSTKSubCategoryTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _deprecated: bool
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: RAMSTKSubCategoryRecord
    pkey: str
    def __init__(self, **kwargs) -> None: ...
