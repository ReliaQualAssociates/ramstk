# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    *,
    current_ratio: float,
    package_id: int,
    technology_id: int,
    temperature_junction: float,
) -> Tuple[int, str]: ...
