# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    *,
    application_id: int,
    current_ratio: float,
    power_ratio: float,
) -> Tuple[int, str]: ...
def _get_switch_application(application_id: int) -> str: ...
