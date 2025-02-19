# Standard Library Imports
from typing import Tuple

def do_update_overstress_status(
    overstress: int, reason: str, result: Tuple[int, str]
) -> Tuple[int, str]: ...
def do_check_current_limit(
    current_ratio: float,
    current_limit: float,
) -> Tuple[int, str]: ...
def do_check_power_limit(
    power_ratio: float,
    power_limit: float,
) -> Tuple[int, str]: ...
def do_check_temperature_limit(
    actual_temperature: float, max_rated_temperature: float, limit: float
) -> Tuple[int, str]: ...
def do_check_voltage_limit(
    voltage_ratio: float,
    voltage_limit: float,
) -> Tuple[int, str]: ...
