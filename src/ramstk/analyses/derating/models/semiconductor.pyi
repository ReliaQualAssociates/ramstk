# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    *,
    current_ratio: float,
    power_ratio: float,
    quality_id: int,
    temperature_junction: float,
    type_id: int,
    voltage_ratio: float,
) -> Tuple[int, str]: ...
def _get_semiconductor_subcategory(subcategory_id: int) -> str: ...
def _get_semiconductor_type(subcategory_id: int, type_id: int) -> str: ...
def _get_semiconductor_quality(quality_id: int) -> str: ...
