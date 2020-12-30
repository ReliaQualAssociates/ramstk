# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Reliability Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Any, Dict, List

PART_COUNT_LAMBDA_B = {
    1: [
        0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016, 0.025,
        0.025, 0.00025, 0.0098, 0.035, 0.36
    ],
    2: {
        1: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033,
            0.030, 0.00025, 0.014, 0.044, 0.69
        ],
        2: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033,
            0.030, 0.00025, 0.014, 0.044, 0.69
        ],
        3: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038,
            0.034, 0.00028, 0.016, 0.050, 0.78
        ],
        4: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038,
            0.034, 0.00028, 0.016, 0.050, 0.78
        ]
    },
    3: [
        0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19, 0.24, 0.32, 0.0060,
        0.18, 0.47, 8.2
    ],
    4: [
        0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043, 0.077, 0.15, 0.10,
        0.0011, 0.055, 0.15, 1.7
    ],
    5: [
        0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30, 0.38, 0.26, 0.0068,
        0.13, 0.37, 5.4
    ],
    6: {
        1: [
            0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19, 0.39, 0.42,
            0.0042, 0.21, 0.62, 9.4
        ],
        2: [
            0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18, 0.35, 0.38,
            0.0038, 0.19, 0.56, 8.6
        ]
    },
    7: [
        0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12, 0.24, 0.25, 0.004,
        0.13, 0.37, 5.5
    ],
    8: [
        0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7, 2.4, 0.032, 1.3, 3.4,
        62.0
    ],
    9: [
        0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35, 0.58, 1.1, 0.013,
        0.52, 1.6, 24.0
    ],
    10: [
        0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0, 0.16, 11.0, 33.0,
        510.0
    ],
    11:
    [0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0, 0.075, 0.0, 0.0, 0.0],
    12:
    [0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6, 0.076, 0.0, 0.0, 0.0],
    13: [
        0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8, 2.8, 2.5, 0.21, 1.2,
        3.7, 49.0
    ],
    14: [
        0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5, 3.3, 0.025, 1.5, 4.7,
        67.0
    ],
    15: [
        0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2, 2.3, 0.024, 1.2,
        3.4, 52.0
    ]
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
    15: [2.0, 4.0]
}
PI_C = {10: [2.0, 1.0, 3.0, 1.5], 12: [2.0, 1.0]}
PI_E = {
    1: [
        1.0, 3.0, 8.0, 5.0, 13.0, 4.0, 5.0, 7.0, 11.0, 19.0, 0.5, 11.0, 27.0,
        490.0
    ],
    2: [
        1.0, 2.0, 8.0, 4.0, 14.0, 4.0, 8.0, 10.0, 18.0, 19.0, 0.2, 10.0, 28.0,
        510.0
    ],
    3: [
        1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5, 14.0, 36.0,
        660.0
    ],
    4: [
        1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5, 14.0, 36.0,
        660.0
    ],
    5: [
        1.0, 2.0, 11.0, 5.0, 18.0, 15.0, 18.0, 28.0, 35.0, 27.0, 0.8, 14.0,
        38.0, 610.0
    ],
    6: [
        1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0, 0.3, 13.0, 34.0,
        610.0
    ],
    7: [
        1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0, 0.5, 13.0, 34.0,
        610.0
    ],
    8: [
        1.0, 5.0, 21.0, 11.0, 24.0, 11.0, 30.0, 16.0, 42.0, 37.0, 0.5, 20.0,
        53.0, 950.0
    ],
    9: [
        1.0, 2.0, 12.0, 6.0, 20.0, 5.0, 8.0, 9.0, 15.0, 33.0, 0.5, 18.0, 48.0,
        870.0
    ],
    10: [
        1.0, 2.0, 18.0, 8.0, 30.0, 8.0, 12.0, 13.0, 18.0, 53.0, 0.5, 29.0,
        76.0, 1400.0
    ],
    11:
    [1.0, 2.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0, 0.5, 0.0, 0.0, 0.0],
    12:
    [1.0, 3.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0, 0.5, 0.0, 0.0, 0.0],
    13: [
        1.0, 3.0, 14.0, 6.0, 24.0, 5.0, 7.0, 12.0, 18.0, 39.0, 0.5, 22.0, 57.0,
        1000.0
    ],
    14: [
        1.0, 2.0, 19.0, 8.0, 29.0, 40.0, 65.0, 48.0, 78.0, 46.0, 0.5, 25.0,
        66.0, 1200.0
    ],
    15: [
        1.0, 3.0, 14.0, 7.0, 24.0, 6.0, 12.0, 20.0, 30.0, 39.0, 0.5, 22.0,
        57.0, 1000.0
    ]
}
PI_R = {
    1: [1.0, 1.1, 1.6, 2.5],
    2: [1.0, 1.1, 1.6, 2.5],
    3: [1.0, 1.2, 1.3, 3.5],
    5: [1.0, 1.7, 3.0, 5.0],
    6: [[[1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
         [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
         [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
         [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
         [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0]],
        [[1.0, 1.0, 1.0, 1.0, 1.2, 1.6], [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
         [1.0, 1.0, 1.0, 2.0, 0.0, 0.0], [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
         [1.0, 1.2, 1.4, 0.0, 0.0, 0.0], [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.2, 2.0, 0.0, 0.0], [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
         [1.0, 1.0, 1.0, 1.4, 0.0, 0.0], [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0], [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0], [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.0, 1.4, 0.0, 0.0], [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
         [1.0, 1.0, 1.0, 1.4, 0.0, 0.0], [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
         [1.0, 1.0, 1.0, 1.4, 1.6, 2.0], [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
         [1.0, 1.0, 1.4, 2.4, 0.0, 0.0], [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
         [1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
         [1.0, 1.0, 0.0, 0.0, 0.0, 0.0], [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0], [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
         [1.0, 1.2, 0.0, 0.0, 0.0, 0.0]]],
    7: [[[1.0, 1.2, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
         [1.0, 1.0, 1.2, 1.2, 1.6, 0.0], [1.0, 1.0, 1.0, 1.1, 1.2, 1.6],
         [1.0, 1.0, 1.0, 1.0, 1.2, 1.6], [1.0, 1.0, 1.0, 1.0, 1.2, 1.6]],
        [[1.0, 1.2, 1.6, 0.0, 0.0, 0.0], [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
         [1.0, 1.0, 1.0, 1.2, 1.6, 0.0], [1.0, 1.0, 1.0, 1.1, 1.4, 0.0]]],
    9: [1.0, 1.4, 2.0],
    10: [1.0, 1.1, 1.4, 2.0, 2.5, 3.5],
    11: [1.0, 1.4, 2.0],
    12: [1.0, 1.4, 2.0],
    13: [1.0, 1.1, 1.2, 1.4, 1.8],
    14: [1.0, 1.1, 1.2, 1.4, 1.8],
    15: [1.0, 1.1, 1.2, 1.4, 1.8]
}
PI_V = {
    9: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    10: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    11: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    12: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    13: [1.0, 1.05, 1.2],
    14: [1.0, 1.05, 1.2],
    15: [1.0, 1.05, 1.2]
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
    15: 343.0
}
REF_TEMPS_FILM: Dict[int, float] = {1: 343.0, 2: 343.0, 3: 398.0, 4: 398.0}


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(attributes)


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress hazard rate for a resistor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = calculate_part_stress_lambda_b(attributes)
    attributes = get_resistance_factor(attributes)
    attributes = calculate_temperature_factor(attributes)

    _subcategory_id: Any = attributes['subcategory_id']
    _construction_id: Any = attributes['construction_id']
    _lambda_b: Any = attributes['lambda_b']
    _n_elements: Any = attributes['n_elements']
    _pi_q: Any = attributes['piQ']
    _pi_e: Any = attributes['piE']
    _pi_t: Any = attributes['piT']
    _pi_r: Any = attributes['piR']

    # Calculate the voltage factor and taps factor (piTAPS).
    if _subcategory_id in [9, 10, 11, 12, 13, 14, 15]:
        attributes = get_voltage_factor(attributes)
        _pi_v = attributes['piV']
        _pi_taps: Any = (_n_elements**1.5 / 25.0) + 0.792
        attributes['piTAPS'] = _pi_taps

    # Determine the consruction class factor (piC).
    if _subcategory_id in [10, 12]:
        _pi_c: Any = PI_C[_subcategory_id][_construction_id - 1]
        attributes['piC'] = _pi_c

    _hazard_rate_active: Any = (_lambda_b * _pi_q * _pi_e)
    if _subcategory_id == 4:
        _hazard_rate_active = (_hazard_rate_active * _pi_t * _n_elements)
    elif _subcategory_id in [9, 11, 13, 14, 15]:
        _hazard_rate_active = (_hazard_rate_active * _pi_taps * _pi_r * _pi_v)
    elif _subcategory_id in [10, 12]:
        _hazard_rate_active = (_hazard_rate_active * _pi_taps * _pi_c * _pi_r
                               * _pi_v)
    elif _subcategory_id != 8:
        _hazard_rate_active = (_hazard_rate_active * _pi_r)

    attributes['hazard_rate_active'] = _hazard_rate_active

    return attributes


# pylint: disable=too-many-locals
def calculate_part_stress_lambda_b(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param attributes: the attributes of the switch being calculated.
    :return attributes: the updated attributes of the switch being calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown quality ID or application ID.
    :raise: KeyError is passed an unknown construction ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _specification_id: Any = attributes['specification_id']
    _type_id: Any = attributes['type_id']
    _temperature_active: Any = attributes['temperature_active']
    _power_ratio: Any = attributes['power_ratio']

    _dic_factors: Dict[int, List[float]] = {
        1: [4.5E-9, 12.0, 1.0, 0.6, 1.0, 1.0],
        3: [7.33E-3, 0.202, 2.6, 1.45, 0.89, 1.3],
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
        15: [0.018, 1.0, 7.4, 2.55, 3.6, 1.0]
    }
    _dic_factors_film: Dict[int, List[float]] = {
        1: [3.25E-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        2: [3.25E-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        3: [5.0E-5, 3.5, 1.0, 1.0, 1.0, 1.0],
        4: [5.0E-5, 3.5, 1.0, 1.0, 1.0, 1.0]
    }

    if _subcategory_id == 2:
        _ref_temp = REF_TEMPS_FILM[_specification_id]
        _f0 = _dic_factors_film[_specification_id][0]
        _f1 = _dic_factors_film[_specification_id][1]
        _f2 = _dic_factors_film[_specification_id][2]
        _f3 = _dic_factors_film[_specification_id][3]
        _f4 = _dic_factors_film[_specification_id][4]
        _f5 = _dic_factors_film[_specification_id][5]
    elif _subcategory_id not in [4, 8]:
        _ref_temp = REF_TEMPS[_subcategory_id]
        _f0 = _dic_factors[_subcategory_id][0]
        _f1 = _dic_factors[_subcategory_id][1]
        _f2 = _dic_factors[_subcategory_id][2]
        _f3 = _dic_factors[_subcategory_id][3]
        _f4 = _dic_factors[_subcategory_id][4]
        _f5 = _dic_factors[_subcategory_id][5]

    if _subcategory_id == 4:
        _lambda_b = 0.00006
    elif _subcategory_id == 8:
        _lambda_b = _dic_factors[_subcategory_id][_type_id - 1]
    else:
        _lambda_b = _f0 * exp(
            _f1 * ((_temperature_active + 273.0) / _ref_temp), )**_f2 * exp(
                ((_power_ratio / _f3) *
                 ((_temperature_active + 273.0) / 273.0)**_f4)**_f5)

    attributes['lambda_b'] = _lambda_b

    return attributes


def calculate_temperature_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the temperature factor (piT).

    :param temperature_active: the ambient operating temperature of the
        resistor in C.
    :param power_ratio: the ratio of the power dissipated by the resistor
        and it's rated power; both in W.
    :return: (temperature_case, _pi_c); the calculated surface temperature of
        the rsistor and it's resistance factor.
    :rtype: tuple
    """
    _temperature_active: float = float(attributes['temperature_active'])
    _power_ratio: float = float(attributes['power_ratio'])

    _temperature_case: float = _temperature_active + 55.0 * _power_ratio
    _pi_t: float = exp(-4056.0 * ((1.0 /
                                   (_temperature_case + 273.0)) - 1.0 / 298.0))

    attributes['temperature_case'] = _temperature_case
    attributes['piT'] = _pi_t

    return attributes


def get_part_count_lambda_b(attributes: Dict[str, Any]) -> Dict[str, Any]:
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
    | Subcategory    |            Resistor           | MIL-HDBK-217F   |
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
    _subcategory_id: Any = attributes['subcategory_id']
    _environment_active_id: Any = attributes['environment_active_id']
    _specification_id: Any = attributes['specification_id']

    if _subcategory_id in [2, 6]:
        _base_hr: Any = PART_COUNT_LAMBDA_B[_subcategory_id][
            _specification_id][_environment_active_id - 1]
    else:
        _base_hr: Any = PART_COUNT_LAMBDA_B[_subcategory_id][
            _environment_active_id - 1]

    attributes['lambda_b'] = _base_hr

    return _base_hr


def get_resistance_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
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
    _subcategory_id: Any = attributes['subcategory_id']
    _specification_id: Any = attributes['specification_id']
    _family_id: Any = attributes['family_id']
    _resistance: Any = attributes['resistance']

    _dic_breakpoints = {
        1: [1.0E5, 1.0E6, 1.0E7],
        2: [1.0E5, 1.0E6, 1.0E7],
        3: [100.0, 1.0E5, 1.0E6],
        5: [1.0E4, 1.0E5, 1.0E6],
        6: [[500.0, 1.0E3, 5.0E3, 7.5E3, 1.0E4, 1.5E4, 2.0E4],
            [100.0, 1.0E3, 1.0E4, 1.0E5, 1.5E5, 2.0E5]],
        7: [500.0, 1.0E3, 5.0E3, 1.0E4, 2.0E4],
        9: [2.0E3, 5.0E3],
        10: [1.0E4, 2.0E4, 5.0E4, 1.0E5, 2.0E5],
        11: [2.0E3, 5.0E3],
        12: [2.0E3, 5.0E3],
        13: [5.0E4, 1.0E5, 2.0E5, 5.0E5],
        14: [5.0E4, 1.0E5, 2.0E5, 5.0E5],
        15: [1.0E4, 5.0E4, 2.0E5, 1.0E6]
    }
    _pi_r = 0.0

    if _subcategory_id not in [4, 8]:
        _index = -1
        if _subcategory_id == 6:
            _breaks = _dic_breakpoints[_subcategory_id][_specification_id - 1]
        else:
            _breaks = _dic_breakpoints[_subcategory_id]

        for _index, _value in enumerate(_breaks):
            _diff = _value - _resistance
            if (len(_breaks) == 1 and _diff < 0) or _diff >= 0:
                break

        # Resistance factor (piR) dictionary of values.  The key is the
        # subcategory ID.  The index in the returned list is the resistance
        # range breakpoint (breakpoint values are in _lst_breakpoints below).
        # For subcategory ID 6 and 7, the specification ID selects the correct
        # set of lists, then the style ID selects the proper list of piR values
        # and then the resistance range breakpoint is used to select
        if _subcategory_id in [6, 7]:
            _pi_r = PI_R[_subcategory_id][_specification_id
                                          - 1][_family_id - 1][_index + 1]
        elif _subcategory_id not in [4, 8]:
            _pi_r = PI_R[_subcategory_id][_index + 1]

    attributes['piR'] = _pi_r

    return attributes


def get_voltage_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve the voltage factor (piV).

    :param subcategory_id: the subcategory identifier.
    :param voltage_ratio: the ratio of voltages on each half of the
        potentiometer.
    :return: _pi_v; the selected voltage factor.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _subcategory_id: int = int(attributes['subcategory_id'])
    _voltage_ratio: float = float(attributes['voltage_ratio'])

    _index = -1
    _breaks = [0.0]
    if _subcategory_id in [9, 10, 11, 12]:
        _breaks = [0.1, 0.2, 0.6, 0.7, 0.8, 0.9]
    elif _subcategory_id in [13, 14, 15]:
        _breaks = [0.8, 0.9]

    for _index, _value in enumerate(_breaks):
        _diff = _value - _voltage_ratio
        if (len(_breaks) == 1
                and _diff < 0.0) or (_index == 0
                                     and _diff >= 0.0) or _diff >= 0:
            break

    attributes['piV'] = PI_V[_subcategory_id][_index]

    return attributes
