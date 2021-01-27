# Standard Library Imports
from typing import Any, Dict, List

PART_COUNT_LAMBDA_B_DICT: Any
PART_COUNT_LAMBDA_B_LIST: Any
PART_COUNT_PI_Q: Dict[int, List[float]]
PART_COUNT_PI_Q_HF_DIODE: List[List[float]]
PART_STRESS_PI_Q: Dict[int, List[float]]
PART_STRESS_PI_Q_HF_DIODE: Dict[int, List[float]]
PI_A: Any
PI_T_DICT: Dict[int, List[float]]
PI_T_LIST: Dict[int, List[float]]
PI_T_SCALAR: Dict[int, float]
CASE_TEMPERATURE: Any
THETA_JC: Any
PI_C: Any
PI_E: Any
PI_M: Any


def calculate_application_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_electrical_stress_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_junction_temperature(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_part_count(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_part_stress_lambda_b(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_power_rating_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_temperature_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def get_part_count_lambda_b(attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def get_part_count_quality_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def get_part_stress_quality_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...
