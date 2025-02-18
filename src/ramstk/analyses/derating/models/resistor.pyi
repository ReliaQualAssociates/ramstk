# Standard Library Imports
from typing import Dict, List, Tuple, Union

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Union[Dict[str, List[float]], List[float]]]],
    *,
    power_rated: float,
    power_ratio: float,
    temperature_case: float,
    temperature_knee: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]: ...
def _get_stress_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Union[Dict[str, List[float]], List[float]]]],
    limit_type: str,
) -> float: ...
