# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models import RAMSTKAllocationRecord as RAMSTKAllocationRecord
from ramstk.models import (
    RAMSTKDesignElectricRecord as RAMSTKDesignElectricRecord,
)
from ramstk.models import (
    RAMSTKDesignMechanicRecord as RAMSTKDesignMechanicRecord,
)
from ramstk.models import RAMSTKFunctionRecord as RAMSTKFunctionRecord
from ramstk.models import RAMSTKHardwareRecord as RAMSTKHardwareRecord
from ramstk.models import RAMSTKMilHdbk217FRecord as RAMSTKMilHdbk217FRecord
from ramstk.models import RAMSTKNSWCRecord as RAMSTKNSWCRecord
from ramstk.models import RAMSTKReliabilityRecord as RAMSTKReliabilityRecord
from ramstk.models import RAMSTKRequirementRecord as RAMSTKRequirementRecord
from ramstk.models import RAMSTKSimilarItemRecord as RAMSTKSimilarItemRecord
from ramstk.models import RAMSTKValidationRecord as RAMSTKValidationRecord

def _do_replace_nan(value: Any, default: Any) -> Any: ...
def _get_input_value(
    mapper: Dict[str, Any], df_row: pd.Series, field: str, default: Any
) -> Any: ...

class Import:
    _dic_field_map: Any
    _dao: Any
    _df_input_data: Any
    def __init__(self) -> None: ...
    def _do_connect(self, dao: BaseDatabase) -> None: ...
    def _do_import(self, module: str) -> None: ...
    def _do_insert_allocation(
        self, row: pd.Series
    ) -> RAMSTKAllocationRecord: ...
    def _do_insert_design_electric(
        self, row: pd.Series
    ) -> RAMSTKDesignElectricRecord: ...
    def _do_insert_design_mechanic(
        self, row: pd.Series
    ) -> RAMSTKDesignMechanicRecord: ...
    def _do_insert_function(self, row: pd.Series) -> RAMSTKFunctionRecord: ...
    def _do_insert_hardware(self, row: pd.Series) -> RAMSTKHardwareRecord: ...
    def _do_insert_mil_hdbk_f(
        self, row: pd.Series
    ) -> RAMSTKMilHdbk217FRecord: ...
    def _do_insert_nswc(self, row: pd.Series) -> RAMSTKNSWCRecord: ...
    def _do_insert_reliability(
        self, row: pd.Series
    ) -> RAMSTKReliabilityRecord: ...
    def _do_insert_requirement(
        self, row: pd.Series
    ) -> RAMSTKRequirementRecord: ...
    def _do_insert_similar_item(
        self, row: pd.Series
    ) -> RAMSTKSimilarItemRecord: ...
    def _do_insert_validation(
        self, row: pd.Series
    ) -> RAMSTKValidationRecord: ...
    def _do_map_to_field(
        self, module: str, import_field: str, format_field: str
    ) -> None: ...
    def _do_read_db_fields(self, module: str) -> None: ...
    def _do_read_file(self, file_type: str, file_name: str) -> None: ...
