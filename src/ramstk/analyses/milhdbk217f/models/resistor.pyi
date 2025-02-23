# Standard Library Imports
from typing import Dict, List, Tuple, Union

PART_COUNT_LAMBDA_B: Dict[int, List[float]]
PART_COUNT_PI_Q: List[float]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, List[float]]
PI_E: Dict[int, List[float]]
PI_R: Dict[int, List[float] | List[List[float]]]
PI_V: Dict[int, List[float]]
REF_TEMPS: Dict[int, float]
REF_TEMPS_FILM: Dict[int, float]

def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def calculate_temperature_factor(
    temperature_active: float,
    power_ratio: float,
) -> Tuple[float, float]: ...
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
def get_resistance_factor(
    subcategory_id: int,
    specification_id: int,
    family_id: int,
    resistance: float,
) -> float: ...
def get_voltage_factor(
    subcategory_id: int,
    voltage_ratio: float,
) -> float: ...
def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _get_factors_and_temp(
    subcategory_id: int,
) -> Tuple[List[float], float]: ...
def _get_film_factors_and_temp(
    specification_id: int,
) -> Tuple[List[float], float]: ...
def _get_type_factor(
    type_id: int,
) -> float: ...
def _set_default_resistance(
    resistance: float,
    subcategory_id: int,
) -> float: ...
def _set_default_elements(
    n_elements: int,
    subcategory_id: int,
) -> float: ...
