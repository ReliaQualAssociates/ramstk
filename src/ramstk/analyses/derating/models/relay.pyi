# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    *,
    current_ratio: float,
    temperature_active: float,
    temperature_rated_max: float,
    type_id: int,
) -> Tuple[int, str]: ...
