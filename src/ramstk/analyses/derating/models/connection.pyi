# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, List[float]],
    *,
    current_ratio: float,
) -> Tuple[int, str]: ...
