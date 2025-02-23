# Standard Library Imports
from typing import Dict, List, Tuple, Union

ACTIVATION_ENERGY: Dict[int, float | List[float]]
C1: Dict[int, List[List[float]]]
C2: Dict[int, List[float]]
PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]] | Dict[int, List[float]]]
PI_A: Dict[int, List[float]]
PI_E: List[float]
PI_PT: Dict[int, float]
PI_Q: List[float]

def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def calculate_die_complexity_factor(
    area: float,
    feature_size: float,
) -> float: ...
def calculate_eos_hazard_rate(
    voltage_esd: float,
) -> float: ...
def calculate_junction_temperature(
    temperature_case: float,
    power_operating: float,
    theta_jc: float,
) -> float: ...
def calculate_lambda_cyclic_factors(
    n_cycles: int,
    construction_id: int,
    n_elements: int,
    temperature_junction: float,
) -> Tuple[float, float, float, float]: ...
def calculate_package_base_hazard_rate(
    n_active_pins: int,
) -> float: ...
def calculate_package_factor(
    package_id: int,
    n_active_pins: int,
) -> float: ...
def calculate_temperature_factor(
    subcategory_id: int,
    family_id: int,
    type_id: int,
    temperature_junction: float,
) -> float: ...
def get_application_factor(
    type_id: int,
    application_id: int,
) -> float: ...
def get_die_base_hazard_rate(
    type_id: int,
) -> float: ...
def get_die_complexity_factor(
    subcategory_id: int,
    technology_id: int,
    application_id: int,
    n_elements: int,
) -> float: ...
def get_environment_factor(
    attributes: Dict[str, Union[float, int, str]],
): ...
def get_error_correction_factor(
    type_id: int,
) -> float: ...
def get_manufacturing_process_factor(
    manufacturing_id: int,
) -> float: ...
def get_package_type_correction_factor(
    package_id: int,
) -> float: ...
def get_part_count_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def get_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float: ...
def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_junction_temperature(
    temperature_junction: float,
    temperature_case: float,
    environment_active_id: int,
) -> float: ...
