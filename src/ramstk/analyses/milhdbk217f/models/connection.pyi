# Standard Library Imports
from typing import Any, Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Any]
PART_COUNT_PI_Q: List[float]
PART_STRESS_LAMBDA_B: Dict[int, List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_E: Dict[int, Any]
PI_K: List[float]
REF_TEMPS: Dict[int, float]

def calculate_active_pins_factor(n_active_pins: int) -> float: ...
def calculate_complexity_factor(n_circuit_planes: int) -> float: ...
def calculate_insert_temperature(
    contact_gauge: int, current_operating: float
) -> float: ...
def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int, type_id: int, contact_temperature: float, factor_key: int
) -> float: ...
def get_factor_key(type_id: int, specification_id: int, insert_id: int) -> int: ...
def get_mate_unmate_factor(n_cycles: float) -> float: ...
def get_part_count_lambda_b(**kwargs: Dict[str, int]) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_active_pins(subcategory_id: int, type_id: int) -> int: ...
def _set_default_temperature_rise(subcategory_id: int, type_id: int) -> float: ...
