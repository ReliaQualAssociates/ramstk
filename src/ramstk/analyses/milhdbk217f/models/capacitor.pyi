# Standard Library Imports
from typing import Any, Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]] | List[float]]
PART_COUNT_PI_Q: List[float]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, float]
PI_CF: Dict[int, float]
PI_E: List[float]
REF_TEMPS: Dict[float, float]
DEFAULT_CAPACITANCE: Dict[int, float | List[float]]
CAPACITANCE_FACTORS: Dict[int, List[float]]
LAMBDA_B_FACTORS: Dict[int, List[float]]

def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def calculate_capacitance_factor(
    subcategory_id: int,
    capacitance: float,
) -> float: ...
def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def calculate_series_resistance_factor(
    resistance: float,
    voltage_dc_operating: float,
    voltage_ac_operating: float,
) -> float: ...
def get_configuration_factor(
    configuration_id: int,
) -> float: ...
def get_construction_factor(
    construction_id: int,
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
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_capacitance(
    subcategory_id: int,
    style_id: int,
) -> float: ...
def _set_default_picv(
    subcategory_id: int,
) -> float: ...
def _set_default_rated_temperature(
    subcategory_id: int,
    style_id: int,
) -> float: ...
