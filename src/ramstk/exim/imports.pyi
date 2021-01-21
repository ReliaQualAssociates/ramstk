# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKNSWC as RAMSTKNSWC
from ramstk.models.programdb import RAMSTKAllocation as RAMSTKAllocation
from ramstk.models.programdb import (
    RAMSTKDesignElectric as RAMSTKDesignElectric
)
from ramstk.models.programdb import (
    RAMSTKDesignMechanic as RAMSTKDesignMechanic
)
from ramstk.models.programdb import RAMSTKFunction as RAMSTKFunction
from ramstk.models.programdb import RAMSTKHardware as RAMSTKHardware
from ramstk.models.programdb import RAMSTKMilHdbkF as RAMSTKMilHdbkF
from ramstk.models.programdb import RAMSTKReliability as RAMSTKReliability
from ramstk.models.programdb import RAMSTKRequirement as RAMSTKRequirement
from ramstk.models.programdb import RAMSTKSimilarItem as RAMSTKSimilarItem
from ramstk.models.programdb import RAMSTKValidation as RAMSTKValidation

def _do_replace_nan(value: Any, default: Any) -> Any:
    ...


def _get_input_value(mapper: Dict[str, Any], df_row: pd.Series, field: str,
                     default: Any) -> Any:
    ...


class Import:
    _dic_field_map: Any = ...
    _dao: Any = ...
    _df_input_data: Any = ...

    def __init__(self) -> None:
        ...

    def _do_connect(self, dao: BaseDatabase) -> None:
        ...

    def _do_import(self, module: str) -> None:
        ...

    def _do_insert_allocation(self, row: pd.Series) -> RAMSTKAllocation:
        ...

    def _do_insert_design_electric(self,
                                   row: pd.Series) -> RAMSTKDesignElectric:
        ...

    def _do_insert_design_mechanic(self,
                                   row: pd.Series) -> RAMSTKDesignMechanic:
        ...

    def _do_insert_function(self, row: pd.Series) -> RAMSTKFunction:
        ...

    def _do_insert_hardware(self, row: pd.Series) -> RAMSTKHardware:
        ...

    def _do_insert_mil_hdbk_f(self, row: pd.Series) -> RAMSTKMilHdbkF:
        ...

    def _do_insert_nswc(self, row: pd.Series) -> RAMSTKNSWC:
        ...

    def _do_insert_reliability(self, row: pd.Series) -> RAMSTKReliability:
        ...

    def _do_insert_requirement(self, row: pd.Series) -> RAMSTKRequirement:
        ...

    def _do_insert_similar_item(self, row: pd.Series) -> RAMSTKSimilarItem:
        ...

    def _do_insert_validation(self, row: pd.Series) -> RAMSTKValidation:
        ...

    def _do_map_to_field(self, module: str, import_field: str,
                         format_field: str) -> None:
        ...

    def _do_read_db_fields(self, module: str) -> None:
        ...

    def _do_read_file(self, file_type: str, file_name: str) -> None:
        ...
