# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]]
PART_COUNT_PI_Q: List[float]
PART_STRESS_PI_Q: Dict[int, Dict[int, List[float]] | List[float]]
PI_E: Dict[int, List[float]]
REF_TEMPS: Dict[int, Dict[int, float]]

def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def calculate_hot_spot_temperature(
    temperature_active: float,
    temperature_rise: float,
) -> float: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    insulation_id: int,
    temperature_hot_spot: float,
) -> float: ...
def calculate_temperature_rise_input_power_weight(
    power_input: float,
    weight: float,
) -> float: ...
def calculate_temperature_rise_power_loss_surface(
    power_operating: float,
    area: float,
) -> float: ...
def calculate_temperature_rise_power_loss_weight(
    power_operating: float,
    weight: float,
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
def get_temperature_rise_spec_sheet(
    page_number: int,
) -> float: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_max_rated_temperature(
    subcategory_id: int,
) -> float: ...
def _set_default_temperature_rise(
    subcategory_id: int,
    family_id: int,
) -> float: ...
