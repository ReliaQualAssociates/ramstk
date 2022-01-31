# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKCategoryRecord as RAMSTKCategoryRecord

class RAMSTKCategoryTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _tag: str
    _lst_id_columns: List[str]
    _record: RAMSTKCategoryRecord
    pkey: str
    def __init__(self, **kwargs) -> None: ...
