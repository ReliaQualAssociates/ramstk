# Standard Library Imports
from typing import Dict, List, Optional, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    *,
    specification_id: int,
    temperature_case: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]: ...
def _get_subcategory_name(
    subcategory_id: int,
    specification_id: Optional[int],
) -> str: ...
