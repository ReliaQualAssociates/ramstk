# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# Third Party Imports
import treelib

# RAMSTK Local Imports
from ..dbrecords import RAMSTKDesignMechanicRecord as RAMSTKDesignMechanicRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKDesignMechanicTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKDesignMechanicRecord]
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKDesignMechanicRecord: ...
    def _on_insert_hardware(self, tree: treelib.Tree) -> None: ...
