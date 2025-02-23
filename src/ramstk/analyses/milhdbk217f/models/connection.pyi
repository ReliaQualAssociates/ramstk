# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]] | List[float]]
PART_COUNT_PI_Q: List[float]
PART_STRESS_LAMBDA_B: Dict[int, List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_E: Dict[int, Dict[int, List[float]] | List[float]]
PI_K: List[float]
REF_TEMPS: Dict[int, float]
INSERT_TEMP_FACTORS: Dict[int, float]
LAMBDA_B_FACTORS: Dict[int, List[float]]
FACTOR_KEYS: Dict[int, Dict[int, List[float]]]

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
def _calculate_active_pins_factor(
    n_active_pins: int,
) -> float: ...
def _calculate_complexity_factor(
    n_circuit_planes: int,
) -> float: ...
def _calculate_insert_temperature(
    contact_gauge: int,
    current_operating: float,
) -> float: ...
def _get_factor_key(
    type_id: int,
    specification_id: int,
    insert_id: int,
) -> int: ...
def _get_mate_unmate_factor(
    n_cycles: float,
) -> float: ...
def _set_default_active_pins(
    subcategory_id: int,
    type_id: int,
) -> int: ...
def _set_default_temperature_rise(
    subcategory_id: int,
    type_id: int,
) -> float: ...
