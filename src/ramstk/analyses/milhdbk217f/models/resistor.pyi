# Standard Library Imports
from typing import Any, Dict, Tuple, Union

PART_COUNT_LAMBDA_B: Any
PART_COUNT_PI_Q: Any
PART_STRESS_PI_Q: Any
PI_C: Any
PI_E: Any
PI_R: Any
PI_V: Any
REF_TEMPS: Dict[int, float]
REF_TEMPS_FILM: Dict[int, float]

def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    specification_id: int,
    type_id: int,
    temperature_active: float,
    power_ratio: float,
) -> float: ...
def calculate_temperature_factor(
    temperature_active: float, power_ratio
) -> Tuple[float, float]: ...
def get_part_count_lambda_b(
    subcategory_id: int, environment_active_id: int, specification_id: int
) -> float: ...
def get_resistance_factor(
    subcategory_id: int, specification_id: int, family_id: int, resistance: float
) -> float: ...
def get_voltage_factor(subcategory_id: int, voltage_ratio: float) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_resistance(resistance: float, subcategory_id: int) -> float: ...
def _set_default_elements(n_elements: int, subcategory_id: int) -> float: ...
