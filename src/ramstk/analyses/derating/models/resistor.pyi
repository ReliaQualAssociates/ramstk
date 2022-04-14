# Standard Library Imports
from typing import Dict, List, Tuple

def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
    **kwargs,
) -> Tuple[int, str]: ...
def _do_check_power_limit(
    power_ratio: float, power_limit: float
) -> Tuple[int, str]: ...
def _do_check_temperature_limit(
    case_temperature: float,
    knee_temperature: float,
    max_rated_temperature: float,
    temperature_limit: float,
) -> Tuple[int, str]: ...
def _do_check_voltage_limit(
    voltage_ratio: float, voltage_limit: float
) -> Tuple[int, str]: ...
def _do_get_power_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float: ...
def _do_get_temperature_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float: ...
def _do_get_voltage_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float: ...
