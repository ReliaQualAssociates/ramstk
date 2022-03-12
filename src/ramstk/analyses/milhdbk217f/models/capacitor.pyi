# Standard Library Imports
from typing import Any, Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Any]
PART_COUNT_PI_Q: List[float]
PART_STRESS_PI_Q: Dict[int, List[float]]
PI_C: Dict[int, float]
PI_CF: Dict[int, float]
PI_E: List[float]
REF_TEMPS: Dict[float, float]

def calculate_capacitance_factor(subcategory_id: int, capacitance: float) -> float: ...
def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    temperature_rated_max: float,
    temperature_active: float,
    voltage_ratio: float,
) -> float: ...
def calculate_series_resistance_factor(
    resistance: float, voltage_dc_operating: float, voltage_ac_operating: float
) -> float: ...
def get_configuration_factor(configuration_id: int) -> float: ...
def get_construction_factor(construction_id: int) -> float: ...
def get_part_count_lambda_b(
    subcategory_id: int, environment_active_id: int, specification_id: int = ...
) -> float: ...
