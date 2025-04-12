# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _

PART_COUNT_LAMBDA_B: dict[int, dict[int, list[float]] | list[float]]
PART_COUNT_PI_Q: list[float]
PART_STRESS_PI_Q: dict[int, list[float]]
PI_C: dict[int, float]
PI_CF: dict[int, float]
PI_E: list[float]
REF_TEMPS: dict[float, float]
DEFAULT_CAPACITANCE: dict[int, float | list[float]]
CAPACITANCE_FACTORS: dict[int, list[float]]
LAMBDA_B_FACTORS: dict[int, list[float]]
CAPACITOR_QUALITY_DICT: dict[int, list[str | list[str]]]
CAPACITOR_SPECIFICATION_DICT: dict[int, list[list[str]]]
CAPACITOR_STYLE_DICT: dict[int, list[list[list[str]]]]
CAPACITOR_STYLE_DICT2: dict[int, list[list[str]]]
