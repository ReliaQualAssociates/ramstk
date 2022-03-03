# Standard Library Imports
from typing import Dict, List, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKProgramInfoRecord as RAMSTKProgramInfoRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKProgramInfoTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKProgramInfoRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
