# Standard Library Imports
from typing import Any, Dict, Tuple

ACTIVATION_ENERGY: Any
C1: Any
C2: Any
PART_COUNT_LAMBDA_B: Any
PI_A: Any
PI_E: Any
PI_PT: Any
PI_Q: Any


def calculate_die_complexity_factor(area: float, feature_size: float) -> float:
    ...


def calculate_junction_temperature(temperature_case: float,
                                   power_operating: float,
                                   theta_jc: float) -> float:
    ...


def calculate_lambda_cyclic_factors(
        n_cycles: int, construction_id: int, n_elements: int,
        temperature_junction: float) -> Tuple[float, float, float, float]:
    ...


def calculate_temperature_factor(subcategory_id: int, family_id: int,
                                 type_id: int,
                                 temperature_junction: float) -> float:
    ...


def calculate_eos_hazard_rate(voltage_esd: float) -> float:
    ...


def calculate_package_base_hazard_rate(n_active_pins: int) -> float:
    ...


def calculate_package_factor(package_id: int, n_active_pins: int) -> float:
    ...


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    ...


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def get_application_factor(type_id: int, application_id: int) -> float:
    ...


def get_die_complexity_factor(subcategory_id: int, technology_id: int,
                              application_id: int, n_elements: int) -> float:
    ...


def get_die_base_hazard_rate(type_id: int) -> float:
    ...


def get_error_correction_factor(type_id: int) -> float:
    ...


def get_manufacturing_process_factor(manufacturing_id: int) -> float:
    ...


def get_package_type_correction_factor(package_id: int) -> float:
    ...


def get_part_count_lambda_b(n_elements: int, id_keys: Dict[str, int]) -> float:
    ...
