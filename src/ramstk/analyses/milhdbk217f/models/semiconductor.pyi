# Standard Library Imports
from typing import Dict, List, Union

PART_COUNT_LAMBDA_B_DICT: Dict[int, Dict[int, List[float]]]
PART_COUNT_LAMBDA_B_LIST: Dict[int, List[float]]
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_COUNT_PI_Q_HF_DIODE: List[List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PART_STRESS_PI_Q_HF_DIODE: Dict[int, List[float]]
PI_T_DICT: Dict[int, List[float]]
PI_T_LIST: Dict[int, List[float]]
PI_T_SCALAR: Dict[int, float]
CASE_TEMPERATURE: List[float]
THETA_JC: List[float]
PI_C: List[float]
PI_E: Dict[int, List[float]]
PI_M: List[float]

def calculate_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_junction_temperature(
    environment_active_id: int,
    package_id: int,
    temperature_case: float,
    theta_jc: float,
    power_operating: float,
) -> float: ...
def calculate_part_count(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    type_id: int,
    application_id: int,
    frequency_operating: float,
    power_operating: float,
    n_elements: int,
) -> float: ...
def calculate_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def calculate_temperature_factor(
    subcategory_id: int, type_id: int, voltage_ratio: float, temperature_junction: float
) -> float: ...
def get_part_count_lambda_b(
    subcategory_id: int, environment_active_id: int, type_id: int
) -> float: ...
def get_part_count_quality_factor(
    subcategory_id: int, quality_id: int, type_id: int
) -> float: ...
def get_part_stress_quality_factor(
    subcategory_id: int, quality_id: int, type_id: int
) -> float: ...
def _get_section_6_1_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_2_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_2_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_3_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_3_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_3_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_4_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_6_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_6_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_7_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_8_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_10_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _get_section_6_13_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]: ...
def _set_default_application_id(
    application_id: int,
    subcategory_id: int,
    type_id: int,
) -> int: ...
def _set_default_rated_power(
    power_rated: float, subcategory_id: int, type_id: int
) -> float: ...
def _set_default_voltage_ratio(
    voltage_ratio: float, subcategory_id: int, type_id: int
) -> float: ...
