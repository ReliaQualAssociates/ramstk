# Standard Library Imports
from typing import Any, Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]]
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_STRESS_LAMBDA_B: Dict[int, Any]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_E: Dict[int, List[float]]
PI_F: List[float]

def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def get_part_count_lambda_b(
    subcategory_id: int, type_id: int, environment_active_id: int
) -> float: ...
def get_part_stress_lambda_b(subcategory_id: int, type_id: int) -> float: ...
def get_temperature_stress_factor(
    temperature_active: float, temperature_rated_max: float
) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
