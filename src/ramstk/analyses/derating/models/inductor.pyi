# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    *,
    current_ratio: float,
    family_id: int,
    temperature_hot_spot: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]: ...
