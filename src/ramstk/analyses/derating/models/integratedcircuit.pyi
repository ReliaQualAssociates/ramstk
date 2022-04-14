# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]: ...
def _do_check_current_limit(
    current_ratio: float, current_limit: float
) -> Tuple[int, str]: ...
def _do_check_temperature_limit(
    junction_temperature: float, temperature_limit: float
) -> Tuple[int, str]: ...
