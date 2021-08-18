# Standard Library Imports
from typing import Any, Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses import derating as derating
from ramstk.analyses import stress as stress
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKDesignElectricRecord as RAMSTKDesignElectricRecord

def do_check_overstress(
    overstress: Dict[str, List[float]], stress_type: str
) -> Tuple[bool, str]: ...

class RAMSTKDesignElectricTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _dic_stress_limits: Any
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_current_ratio(self, node_id: int) -> None: ...
    def do_calculate_power_ratio(self, node_id: int) -> None: ...
    def do_calculate_voltage_ratio(self, node_id: int) -> None: ...
    def do_derating_analysis(self, node_id: int, category_id: int) -> None: ...
    def do_stress_analysis(self, node_id: int, category_id: int) -> None: ...
