# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Reliability Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, List, Tuple, Union

PART_COUNT_LAMBDA_B = {
    1: [
        0.0005,
        0.0022,
        0.0071,
        0.0037,
        0.012,
        0.0052,
        0.0065,
        0.016,
        0.025,
        0.025,
        0.00025,
        0.0098,
        0.035,
        0.36,
    ],
    2: {
        1: [
            0.0012,
            0.0027,
            0.011,
            0.0054,
            0.020,
            0.0063,
            0.013,
            0.018,
            0.033,
            0.030,
            0.00025,
            0.014,
            0.044,
            0.69,
        ],
        2: [
            0.0012,
            0.0027,
            0.011,
            0.0054,
            0.020,
            0.0063,
            0.013,
            0.018,
            0.033,
            0.030,
            0.00025,
            0.014,
            0.044,
            0.69,
        ],
        3: [
            0.0014,
            0.0031,
            0.013,
            0.0061,
            0.023,
            0.0072,
            0.014,
            0.021,
            0.038,
            0.034,
            0.00028,
            0.016,
            0.050,
            0.78,
        ],
        4: [
            0.0014,
            0.0031,
            0.013,
            0.0061,
            0.023,
            0.0072,
            0.014,
            0.021,
            0.038,
            0.034,
            0.00028,
            0.016,
            0.050,
            0.78,
        ],
    },
    3: [
        0.012,
        0.025,
        0.13,
        0.062,
        0.21,
        0.078,
        0.10,
        0.19,
        0.24,
        0.32,
        0.0060,
        0.18,
        0.47,
        8.2,
    ],
    4: [
        0.0023,
        0.0066,
        0.031,
        0.013,
        0.055,
        0.022,
        0.043,
        0.077,
        0.15,
        0.10,
        0.0011,
        0.055,
        0.15,
        1.7,
    ],
    5: [
        0.0085,
        0.018,
        0.10,
        0.045,
        0.16,
        0.15,
        0.17,
        0.30,
        0.38,
        0.26,
        0.0068,
        0.13,
        0.37,
        5.4,
    ],
    6: {
        1: [
            0.014,
            0.031,
            0.16,
            0.077,
            0.26,
            0.073,
            0.15,
            0.19,
            0.39,
            0.42,
            0.0042,
            0.21,
            0.62,
            9.4,
        ],
        2: [
            0.013,
            0.028,
            0.15,
            0.070,
            0.24,
            0.065,
            0.13,
            0.18,
            0.35,
            0.38,
            0.0038,
            0.19,
            0.56,
            8.6,
        ],
    },
    7: [
        0.008,
        0.18,
        0.096,
        0.045,
        0.15,
        0.044,
        0.088,
        0.12,
        0.24,
        0.25,
        0.004,
        0.13,
        0.37,
        5.5,
    ],
    8: [
        0.065,
        0.32,
        1.4,
        0.71,
        1.6,
        0.71,
        1.9,
        1.0,
        2.7,
        2.4,
        0.032,
        1.3,
        3.4,
        62.0,
    ],
    9: [
        0.025,
        0.055,
        0.35,
        0.15,
        0.58,
        0.16,
        0.26,
        0.35,
        0.58,
        1.1,
        0.013,
        0.52,
        1.6,
        24.0,
    ],
    10: [
        0.33,
        0.73,
        7.0,
        2.9,
        12.0,
        3.5,
        5.3,
        7.1,
        9.8,
        23.0,
        0.16,
        11.0,
        33.0,
        510.0,
    ],
    11: [
        0.15,
        0.35,
        3.1,
        1.2,
        5.4,
        1.9,
        2.8,
        0.0,
        0.0,
        9.0,
        0.075,
        0.0,
        0.0,
        0.0,
    ],
    12: [
        0.15,
        0.34,
        2.9,
        1.2,
        5.0,
        1.6,
        2.4,
        0.0,
        0.0,
        7.6,
        0.076,
        0.0,
        0.0,
        0.0,
    ],
    13: [
        0.043,
        0.15,
        0.75,
        0.35,
        1.3,
        0.39,
        0.78,
        1.8,
        2.8,
        2.5,
        0.21,
        1.2,
        3.7,
        49.0,
    ],
    14: [
        0.05,
        0.11,
        1.1,
        0.45,
        1.7,
        2.8,
        4.6,
        4.6,
        7.5,
        3.3,
        0.025,
        1.5,
        4.7,
        67.0,
    ],
    15: [
        0.048,
        0.16,
        0.76,
        0.36,
        1.3,
        0.36,
        0.72,
        1.4,
        2.2,
        2.3,
        0.024,
        1.2,
        3.4,
        52.0,
    ],
}
PART_COUNT_PI_Q = [0.030, 0.10, 0.30, 1.0, 3.0, 10.0]
PART_STRESS_PI_Q = {
    1: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    2: [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0],
    3: [1.0, 3.0],
    4: [1.0, 3.0],
    5: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    6: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    7: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    8: [1.0, 15.0],
    9: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
    10: [2.5, 5.0],
    11: [2.0, 4.0],
    12: [2.0, 4.0],
    13: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
    14: [2.5, 5.0],
    15: [2.0, 4.0],
}
PI_C = {10: [2.0, 1.0, 3.0, 1.5], 12: [2.0, 1.0]}
PI_E = {
    1: [
        1.0,
        3.0,
        8.0,
        5.0,
        13.0,
        4.0,
        5.0,
        7.0,
        11.0,
        19.0,
        0.5,
        11.0,
        27.0,
        490.0,
    ],
    2: [
        1.0,
        2.0,
        8.0,
        4.0,
        14.0,
        4.0,
        8.0,
        10.0,
        18.0,
        19.0,
        0.2,
        10.0,
        28.0,
        510.0,
    ],
    3: [
        1.0,
        2.0,
        10.0,
        5.0,
        17.0,
        6.0,
        8.0,
        14.0,
        18.0,
        25.0,
        0.5,
        14.0,
        36.0,
        660.0,
    ],
    4: [
        1.0,
        2.0,
        10.0,
        5.0,
        17.0,
        6.0,
        8.0,
        14.0,
        18.0,
        25.0,
        0.5,
        14.0,
        36.0,
        660.0,
    ],
    5: [
        1.0,
        2.0,
        11.0,
        5.0,
        18.0,
        15.0,
        18.0,
        28.0,
        35.0,
        27.0,
        0.8,
        14.0,
        38.0,
        610.0,
    ],
    6: [
        1.0,
        2.0,
        10.0,
        5.0,
        16.0,
        4.0,
        8.0,
        9.0,
        18.0,
        23.0,
        0.3,
        13.0,
        34.0,
        610.0,
    ],
    7: [
        1.0,
        2.0,
        10.0,
        5.0,
        16.0,
        4.0,
        8.0,
        9.0,
        18.0,
        23.0,
        0.5,
        13.0,
        34.0,
        610.0,
    ],
    8: [
        1.0,
        5.0,
        21.0,
        11.0,
        24.0,
        11.0,
        30.0,
        16.0,
        42.0,
        37.0,
        0.5,
        20.0,
        53.0,
        950.0,
    ],
    9: [
        1.0,
        2.0,
        12.0,
        6.0,
        20.0,
        5.0,
        8.0,
        9.0,
        15.0,
        33.0,
        0.5,
        18.0,
        48.0,
        870.0,
    ],
    10: [
        1.0,
        2.0,
        18.0,
        8.0,
        30.0,
        8.0,
        12.0,
        13.0,
        18.0,
        53.0,
        0.5,
        29.0,
        76.0,
        1400.0,
    ],
    11: [
        1.0,
        2.0,
        16.0,
        7.0,
        28.0,
        8.0,
        12.0,
        0.0,
        0.0,
        38.0,
        0.5,
        0.0,
        0.0,
        0.0,
    ],
    12: [
        1.0,
        3.0,
        16.0,
        7.0,
        28.0,
        8.0,
        12.0,
        0.0,
        0.0,
        38.0,
        0.5,
        0.0,
        0.0,
        0.0,
    ],
    13: [
        1.0,
        3.0,
        14.0,
        6.0,
        24.0,
        5.0,
        7.0,
        12.0,
        18.0,
        39.0,
        0.5,
        22.0,
        57.0,
        1000.0,
    ],
    14: [
        1.0,
        2.0,
        19.0,
        8.0,
        29.0,
        40.0,
        65.0,
        48.0,
        78.0,
        46.0,
        0.5,
        25.0,
        66.0,
        1200.0,
    ],
    15: [
        1.0,
        3.0,
        14.0,
        7.0,
        24.0,
        6.0,
        12.0,
        20.0,
        30.0,
        39.0,
        0.5,
        22.0,
        57.0,
        1000.0,
    ],
}
PI_R = {
    1: [1.0, 1.1, 1.6, 2.5],
    2: [1.0, 1.1, 1.6, 2.5],
    3: [1.0, 1.2, 1.3, 3.5],
    5: [1.0, 1.7, 3.0, 5.0],
    6: [
        [
            [1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
            [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
        [
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
            [1.0, 1.0, 1.4, 2.4, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
            [1.0, 1.2, 0.0, 0.0, 0.0, 0.0],
        ],
    ],
    7: [
        [
            [1.0, 1.2, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.1, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
        ],
        [
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.1, 1.4, 0.0],
        ],
    ],
    9: [1.0, 1.4, 2.0],
    10: [1.0, 1.1, 1.4, 2.0, 2.5, 3.5],
    11: [1.0, 1.4, 2.0],
    12: [1.0, 1.4, 2.0],
    13: [1.0, 1.1, 1.2, 1.4, 1.8],
    14: [1.0, 1.1, 1.2, 1.4, 1.8],
    15: [1.0, 1.1, 1.2, 1.4, 1.8],
}
PI_V = {
    9: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    10: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    11: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    12: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    13: [1.0, 1.05, 1.2],
    14: [1.0, 1.05, 1.2],
    15: [1.0, 1.05, 1.2],
}
REF_TEMPS: Dict[int, float] = {
    1: 343.0,
    3: 298.0,
    5: 398.0,
    6: 298.0,
    7: 298.0,
    9: 358.0,
    10: 358.0,
    11: 313.0,
    12: 298.0,
    13: 358.0,
    14: 343.0,
    15: 343.0,
}
REF_TEMPS_FILM: Dict[int, float] = {1: 343.0, 2: 343.0, 3: 398.0, 4: 398.0}


def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attribute dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes["subcategory_id"],
        attributes["environment_active_id"],
        attributes["specification_id"],
    )


def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a resistor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes["lambda_b"] = calculate_part_stress_lambda_b(
        attributes["subcategory_id"],
        attributes["specification_id"],
        attributes["type_id"],
        attributes["temperature_active"],
        attributes["power_ratio"],
    )
    attributes["piR"] = get_resistance_factor(
        attributes["subcategory_id"],
        attributes["specification_id"],
        attributes["family_id"],
        attributes["resistance"],
    )
    attributes["temperature_case"], attributes["piT"] = calculate_temperature_factor(
        attributes["temperature_active"],
        attributes["power_ratio"],
    )

    # Calculate the voltage factor and taps factor (piTAPS).
    if attributes["subcategory_id"] in [9, 10, 11, 12, 13, 14, 15]:
        attributes["piV"] = get_voltage_factor(
            attributes["subcategory_id"],
            attributes["voltage_ratio"],
        )
        attributes["piTAPS"] = (attributes["n_elements"] ** 1.5 / 25.0) + 0.792

    # Determine the consruction class factor (piC).
    if attributes["subcategory_id"] in [10, 12]:
        attributes["piC"] = PI_C[attributes["subcategory_id"]][
            attributes["construction_id"] - 1
        ]

    attributes["hazard_rate_active"] = (
        attributes["lambda_b"] * attributes["piQ"] * attributes["piE"]
    )
    if attributes["subcategory_id"] == 4:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piT"]
            * attributes["n_elements"]
        )
    elif attributes["subcategory_id"] in [9, 11, 13, 14, 15]:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piTAPS"]
            * attributes["piR"]
            * attributes["piV"]
        )
    elif attributes["subcategory_id"] in [10, 12]:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piTAPS"]
            * attributes["piC"]
            * attributes["piR"]
            * attributes["piV"]
        )
    elif attributes["subcategory_id"] != 8:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] * attributes["piR"]
        )

    return attributes


# pylint: disable=too-many-locals
def calculate_part_stress_lambda_b(
    subcategory_id: int,
    specification_id: int,
    type_id: int,
    temperature_active: float,
    power_ratio: float,
) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param subcategory_id: the subcategory ID for the resistor being calculated.
    :param specification_id: the specification ID for the resistor being calculated.
    :param type_id: the type ID for the resistor being calculated.
    :param temperature_active: the active (surface) temperature for the resistor being
        calculated.
    :param power_ratio: the opearting to rated power ratio for the resistor being
        calculated.
    :return _lambda_b: the calculated base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown quality ID or application ID.
    :raise: KeyError is passed an unknown construction ID.
    """
    _dic_factors: Dict[int, List[float]] = {
        1: [4.5e-9, 12.0, 1.0, 0.6, 1.0, 1.0],
        3: [7.33e-3, 0.202, 2.6, 1.45, 0.89, 1.3],
        5: [0.0031, 1.0, 10.0, 1.0, 1.0, 1.5],
        6: [0.00148, 1.0, 2.0, 0.5, 1.0, 1.0],
        7: [0.00015, 2.64, 1.0, 0.466, 1.0, 1.0],
        8: [0.021, 0.065, 0.105, 0.0, 0.0, 0.0],
        9: [0.0062, 1.0, 5.0, 1.0, 1.0, 1.0],
        10: [0.0735, 1.03, 4.45, 2.74, 3.51, 1.0],
        11: [0.0398, 0.514, 5.28, 1.44, 4.46, 1.0],
        12: [0.0481, 0.334, 4.66, 1.47, 2.83, 1.0],
        13: [0.019, 0.445, 7.3, 2.69, 2.46, 1.0],
        14: [0.0246, 0.459, 9.3, 2.32, 5.3, 1.0],
        15: [0.018, 1.0, 7.4, 2.55, 3.6, 1.0],
    }
    _dic_factors_film: Dict[int, List[float]] = {
        1: [3.25e-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        2: [3.25e-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        3: [5.0e-5, 3.5, 1.0, 1.0, 1.0, 1.0],
        4: [5.0e-5, 3.5, 1.0, 1.0, 1.0, 1.0],
    }

    if subcategory_id == 2:
        _ref_temp = REF_TEMPS_FILM[specification_id]
        _f0 = _dic_factors_film[specification_id][0]
        _f1 = _dic_factors_film[specification_id][1]
        _f2 = _dic_factors_film[specification_id][2]
        _f3 = _dic_factors_film[specification_id][3]
        _f4 = _dic_factors_film[specification_id][4]
        _f5 = _dic_factors_film[specification_id][5]
    elif subcategory_id not in [4, 8]:
        _ref_temp = REF_TEMPS[subcategory_id]
        _f0 = _dic_factors[subcategory_id][0]
        _f1 = _dic_factors[subcategory_id][1]
        _f2 = _dic_factors[subcategory_id][2]
        _f3 = _dic_factors[subcategory_id][3]
        _f4 = _dic_factors[subcategory_id][4]
        _f5 = _dic_factors[subcategory_id][5]

    if subcategory_id == 4:
        return 0.00006
    elif subcategory_id == 8:
        return _dic_factors[subcategory_id][type_id - 1]
    return (
        _f0
        * exp(
            _f1 * ((temperature_active + 273.0) / _ref_temp),
        )
        ** _f2
        * exp(
            ((power_ratio / _f3) * ((temperature_active + 273.0) / 273.0) ** _f4) ** _f5
        )
    )


def calculate_temperature_factor(
    temperature_active: float,
    power_ratio: float,
) -> Tuple[float, float]:
    """Calculate the temperature factor (piT).

    :param temperature_active: the ambient operating temperature of the
        resistor in C.
    :param power_ratio: the ratio of operating to rated power of the resistor being
        calculated.
    :return: (temperature_case, _pi_c); the calculated surface temperature of
        the resistor and it's resistance factor.
    :rtype: tuple
    """
    _temperature_case: float = temperature_active + 55.0 * power_ratio
    _pi_t: float = exp(-4056.0 * ((1.0 / (_temperature_case + 273.0)) - 1.0 / 298.0))

    return _temperature_case, _pi_t


def get_part_count_lambda_b(
    subcategory_id: int,
    environment_active_id: int,
    specification_id: int,
) -> Dict[str, Union[float, int, str]]:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. specification id; if the resistor subcategory is NOT specification
            dependent, then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    |  Subcategory   |            Resistor           | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Fixed, Composition (RC, RCR)  |        9.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Film (RL, RLR, RN,     |        9.2      |
    |                | RNC, RNN, RNR)                |                 |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Film, Power (RD)       |        9.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Film, Network (RZ)     |        9.4      |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Wirewound (RB, RBR)    |        9.5      |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Wirewound, Power       |        9.6      |
    |                | (RW, RWR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Wirewound, Power,      |        9.7      |
    |                | Chassis Mounted (RE, RER)     |                 |
    +----------------+-------------------------------+-----------------+
    |        8       | Thermistor                    |        9.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Variable, Wirewound (RT, RTR) |        9.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Variable, Wirewound,          |       9.10      |
    |                | Precision (RR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Variable, Wirewound,          |       9.11      |
    |                | Semiprecision (RA, RK)        |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Variable, Wirewound, Power    |       9.12      |
    |                | (RP)                          |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Variable, Non-Wirewound       |       9.13      |
    |                | (RJ, RJR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Variable, Composition (RV)    |       9.14      |
    +----------------+-------------------------------+-----------------+
    |       15       | Variable,Non-Wirewound,       |       9.15      |
    |                | Film and Precision (RQ, RVC)  |                 |
    +----------------+-------------------------------+-----------------+

    :param subcategory_id: the subcategory identifier.
    :param environment_active_id: the active environment identifier.
    :param specification_id: the resistor spectification identifier.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or specification ID:
    """
    if subcategory_id in {2, 6}:
        return PART_COUNT_LAMBDA_B[subcategory_id][specification_id][
            environment_active_id - 1
        ]
    return PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id - 1]


def get_resistance_factor(
    subcategory_id: int,
    specification_id: int,
    family_id: int,
    resistance: float,
) -> float:
    """Retrieve the resistance factor (piR).

    :param subcategory_id: the subcategory identifier.
    :param specification_id: the resistor's governing specification
        identifier.
    :param family_id: the resistor family identifier.
    :param resistance: the resistance in ohms of the resistor.
    :return: _pi_r; the calculated resistance factor value.
    :rtype: float
    :raise: IndexError if passed an unknown specification ID or family ID.
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _pi_r = 0.0

    if subcategory_id not in [4, 8]:
        _index = -1
        _dic_breakpoints = {
            1: [1.0e5, 1.0e6, 1.0e7],
            2: [1.0e5, 1.0e6, 1.0e7],
            3: [100.0, 1.0e5, 1.0e6],
            5: [1.0e4, 1.0e5, 1.0e6],
            6: [
                [500.0, 1.0e3, 5.0e3, 7.5e3, 1.0e4, 1.5e4, 2.0e4],
                [100.0, 1.0e3, 1.0e4, 1.0e5, 1.5e5, 2.0e5],
            ],
            7: [500.0, 1.0e3, 5.0e3, 1.0e4, 2.0e4],
            9: [2.0e3, 5.0e3],
            10: [1.0e4, 2.0e4, 5.0e4, 1.0e5, 2.0e5],
            11: [2.0e3, 5.0e3],
            12: [2.0e3, 5.0e3],
            13: [5.0e4, 1.0e5, 2.0e5, 5.0e5],
            14: [5.0e4, 1.0e5, 2.0e5, 5.0e5],
            15: [1.0e4, 5.0e4, 2.0e5, 1.0e6],
        }
        if subcategory_id == 6:
            _breaks = _dic_breakpoints[subcategory_id][specification_id - 1]
        else:
            _breaks = _dic_breakpoints[subcategory_id]

        for _index, _value in enumerate(_breaks):
            _diff = _value - resistance
            if (len(_breaks) == 1 and _diff < 0) or _diff >= 0:
                break

        # Resistance factor (piR) dictionary of values.  The key is the
        # subcategory ID.  The index in the returned list is the resistance
        # range breakpoint (breakpoint values are in _lst_breakpoints below).
        # For subcategory ID 6 and 7, the specification ID selects the correct
        # set of lists, then the style ID selects the proper list of piR values
        # and then the resistance range breakpoint is used to select
        if subcategory_id in {6, 7}:
            _pi_r = PI_R[subcategory_id][specification_id - 1][family_id - 1][
                _index + 1
            ]
        else:
            _pi_r = PI_R[subcategory_id][_index + 1]

    return _pi_r


def get_voltage_factor(
    subcategory_id: int,
    voltage_ratio: float,
) -> float:
    """Retrieve the voltage factor (piV).

    :param subcategory_id: the subcategory identifier.
    :param voltage_ratio: the ratio of voltages on each half of the
        potentiometer.
    :return: _pi_v; the selected voltage factor.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _index = -1
    _breaks = [0.0]
    if subcategory_id in {9, 10, 11, 12}:
        _breaks = [0.1, 0.2, 0.6, 0.7, 0.8, 0.9]
    elif subcategory_id in {13, 14, 15}:
        _breaks = [0.8, 0.9]

    for _index, _value in enumerate(_breaks):
        _diff = _value - voltage_ratio
        if (
            (len(_breaks) == 1 and _diff < 0.0)
            or (_index == 0 and _diff >= 0.0)
            or _diff >= 0
        ):
            break

    return PI_V[subcategory_id][_index]


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the resustor being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["power_ratio"] <= 0.0:
        attributes["power_ratio"] = 0.5

    attributes["resistance"] = _set_default_resistance(
        attributes["resistance"],
        attributes["subcategory_id"],
    )

    attributes["n_elements"] = _set_default_elements(
        attributes["n_elements"], attributes["subcategory_id"]
    )

    if attributes["subcategory_id"] == 4 and attributes["temperature_case"] <= 0.0:
        attributes["temperature_case"] = attributes["temperature_active"] + 28.0

    return attributes


def _set_default_resistance(resistance: float, subcategory_id: int) -> float:
    """Set the default resistance for resistors.

    :param resistance: the current resistance.
    :param subcategory_id: the subcategory ID of the resistor with missing defaults.
    :return: _resistance
    :rtype: float
    """
    if resistance > 0.0:
        return resistance
    return {
        1: 1000000.0,
        2: 1000000.0,
        3: 100.0,
        4: 1000.0,
        5: 100000.0,
        6: 5000.0,
        7: 5000.0,
        8: 1000.0,
        9: 5000.0,
        10: 50000.0,
        11: 5000.0,
        12: 5000.0,
        13: 200000.0,
        14: 200000.0,
        15: 200000.0,
    }[subcategory_id]


def _set_default_elements(n_elements: int, subcategory_id: int) -> float:
    """Set the default number of elements for resistors.

    :param resistance: the current number of elements.
    :param subcategory_id: the subcategory ID of the resistor with missing defaults.
    :return: _n_elements
    :rtype: int
    """
    if n_elements > 0:
        return n_elements
    return {
        1: 0,
        2: 0,
        3: 0,
        4: 10,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 3,
        10: 3,
        11: 3,
        12: 3,
        13: 3,
        14: 3,
        15: 3,
    }[subcategory_id]
