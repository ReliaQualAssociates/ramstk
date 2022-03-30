# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, List[float]]
PART_STRESS_LAMBDA_B: Dict[int, float]
PI_E: List[float]
PI_Q: List[float]

def calculate_part_count(**attributes: Dict[str, int]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def get_part_count_lambda_b(type_id: int, environment_active_id: int) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
