# Standard Library Imports
from typing import Any, Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]]
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, List[float]]
PI_E: Dict[int, Any]
PI_F: Dict[int, Dict[int, Dict[int, List[float]]]]

def calculate_cycling_factor(quality_id: int, n_cycles: float) -> float: ...
def calculate_load_stress_factor(technology_id: int, current_ratio: float) -> float: ...
def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int, type_id: int, temperature_active: float
) -> float: ...
def get_application_construction_factor(
    quality_id: int, contact_rating_id: int, construction_id: int, application_id: int
) -> float: ...
def get_environment_factor(
    subcategory_id: int, quality_id: int, environment_active_id: int
) -> float: ...
def get_part_count_lambda_b(
    subcategory_id: int, type_id: int, environment_active_id: int
) -> float: ...