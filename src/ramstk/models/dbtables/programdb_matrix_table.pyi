# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# Third Party Imports
import pandas as pd

# RAMSTK Local Imports
from ..dbrecords import RAMSTKMatrixRecord as RAMSTKMatrixRecord
from .basetable import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKMatrixTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: List[str]
    _record: Type[RAMSTKMatrixRecord]
    matrix_df: pd.DataFrame
    pkey: str
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None: ...
    def do_build_matrix(self, column_lst: List[str], row_lst: List[str]) -> None: ...
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKMatrixRecord: ...
    def do_insert_column(self, column_header_str: str) -> None: ...
    def do_insert_row(self, row_header_str: str) -> None: ...
