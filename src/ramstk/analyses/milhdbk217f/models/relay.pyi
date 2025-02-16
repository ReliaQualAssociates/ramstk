# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]]
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, List[float]]
PI_E: Dict[int, Dict[int, List[float]] | List[float]]
PI_F: Dict[int, Dict[int, Dict[int, List[float]]]]

def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def get_environment_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def get_part_count_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _calculate_cycling_factor(
    quality_id: int,
    n_cycles: float,
) -> float: ...
def _calculate_load_stress_factor(
    technology_id: int,
    current_ratio: float,
) -> float: ...
def _get_application_construction_factor(
    quality_id: int,
    contact_rating_id: int,
    construction_id: int,
    application_id: int,
) -> float: ...
def _set_default_quality(
    subcategory_id: int,
) -> int: ...
def _set_default_load_type(
    technology_id: int,
    type_id: int,
) -> int: ...
def _set_default_contact_form(
    contact_form_id: int,
    type_id: int,
) -> int: ...
def _set_default_contact_rating(
    contact_rating_id: int,
    type_id: int,
) -> int: ...
def _set_default_application(
    application_id: int,
    type_id: int,
) -> int: ...
def _set_default_construction(
    construction_id: int,
    type_id: int,
) -> int: ...
def _set_default_duty_cycle(
    duty_cycle: float,
    type_id: int,
) -> float: ...
def _set_default_rated_temperature(
    rated_temperature_max: float,
    type_id: int,
) -> float: ...
