# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, List[float]]
PART_COUNT_LAMBDA_B_BREAKER: Dict[int, List[float]]
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_STRESS_LAMBDA_B_TOGGLE: Dict[int, List[float]]
PART_STRESS_LAMBDA_B_BREAKER: List[float]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, List[float]]
PI_E: Dict[int, List[float]]

def calculate_load_stress_factor(
    application_id: int, current_ratio: float
) -> float: ...
def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    quality_id: int,
    construction_id: int,
    application_id: int,
    n_elements: int,
) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def get_part_count_lambda_b(
    subcategory_id: int, environment_active_id: int, construction_id: int
) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_construction_id(construction_id: int, subcategory_id: int) -> int: ...
def _set_default_contact_form_id(contact_form_id: int, subcategory_id: int) -> int: ...
def _set_default_cycle_rate(cycle_rate: float, subcategory_id: int) -> float: ...
def _set_default_active_contacts(active_contacts: int, subcategory_id: int) -> int: ...
