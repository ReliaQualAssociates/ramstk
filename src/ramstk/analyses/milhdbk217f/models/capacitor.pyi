# Standard Library Imports
from typing import Any, Dict

PART_COUNT_LAMBDA_B: Any
PART_COUNT_PI_Q: Any
PART_STRESS_PI_Q: Any
PI_C: Any
PI_CF: Any
PI_E: Any
REF_TEMPS: Any


def calculate_capacitance_factor(subcategory_id: int,
                                 capacitance: float) -> float:
    ...


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    ...


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def calculate_part_stress_lambda_b(subcategory_id: int,
                                   temperature_rated_max: float,
                                   temperature_active: float,
                                   voltage_ratio: float) -> float:
    ...


def calculate_series_resistance_factor(resistance: float,
                                       voltage_dc_operating: float,
                                       voltage_ac_operating: float) -> float:
    ...


def get_configuration_factor(configuration_id: int) -> float:
    ...


def get_construction_factor(construction_id: int) -> float:
    ...


def get_part_count_lambda_b(subcategory_id: int,
                            environment_active_id: int,
                            specification_id: int = ...) -> float:
    ...
