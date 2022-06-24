# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column

# RAMSTK Local Imports
from .. import RAMSTK_BASE as RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKMatrixRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[int, str]]
    __tablename__: str
    __table_args__: Column
    revision_id: Column
    matrix_id: Column
    description: Column
    column_id: Column
    row_id: Column
    correlation: Column
    def get_attributes(self) -> Dict[str, Union[int, str]]: ...
