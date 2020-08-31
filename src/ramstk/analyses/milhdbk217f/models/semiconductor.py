# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.Semiconductor.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from math import exp, log, sqrt
from typing import Any, Dict, List

PART_COUNT_LAMBDA_B_DICT = {
    1: {
        1: [
            0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210, 0.200, 0.44,
            0.170, 0.00180, 0.076, 0.23, 1.50
        ],
        2: [
            0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054, 0.054, 0.12,
            0.045, 0.00047, 0.020, 0.06, 0.40
        ],
        3: [
            0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700, 3.700, 8.00,
            3.100, 0.03200, 1.400, 4.10, 28.0
        ],
        4: [
            0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160, 0.160, 0.35,
            0.130, 0.00140, 0.060, 0.18, 1.20
        ],
        5: [
            0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170, 0.170, 0.36,
            0.140, 0.00150, 0.062, 0.18, 1.20
        ],
        6: [
            0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150, 0.130, 0.27,
            0.120, 0.00160, 0.060, 0.16, 1.30
        ],
        7: [
            0.00580, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250, 0.220, 0.460,
            0.21, 0.00280, 0.100, 0.28, 2.10
        ]
    },
    2: {
        1: [
            0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0, 62.0, 44.0, 0.43,
            16.0, 67.0, 350.0
        ],
        2: [
            0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50, 7.60, 7.90, 0.16,
            3.70, 12.0, 94.00
        ],
        3: [
            0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032, 0.057, 0.097,
            0.10, 0.002, 0.048, 0.15, 1.2
        ],
        4: [
            0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69, 0.71,
            0.014, 0.34, 1.1, 8.5
        ],
        5: [
            0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2, 0.023,
            0.56, 1.8, 14.0
        ],
        6: [
            0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062, 0.11,
            0.11, 0.0022, 0.052, 0.17, 1.3
        ]
    },
    3: {
        1: [
            0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067, 0.0060,
            0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056
        ],
        2: [
            0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23, 0.50, 0.22,
            0.0029, 0.11, 0.29, 1.1
        ]
    },
    8: {
        1: [
            0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2, 0.083, 2.8,
            11.0, 63.0
        ],
        2: [
            0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0, 0.21, 6.9,
            27.0, 160.0
        ]
    },
    11: {
        1: [
            0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100, 0.2100,
            0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70
        ],
        2: [
            0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500, 0.4900,
            0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70
        ],
        3: [
            0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044, 0.0086,
            0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15
        ]
    },
    13: {
        1: [
            5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0, 230.0, 2.6,
            87.0, 350.0, 2000.0
        ],
        2: [
            8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0, 300.0, 400.0,
            4.5, 150.0, 600.0, 3500.0
        ]
    }
}
PART_COUNT_LAMBDA_B_LIST = {
    4: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51, 0.0069,
        0.25, 0.68, 5.3
    ],
    5: [
        0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6, 0.66, 0.0079,
        0.31, 0.88, 6.4
    ],
    6: [
        0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3, 2.4, 0.047, 1.1,
        3.6, 28.0
    ],
    7: [
        0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52, 0.88, 0.037, 0.33,
        0.66, 1.8, 18.0
    ],
    9: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51, 0.0069,
        0.25, 0.68, 5.3
    ],
    10: [
        0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14, 0.14, 0.31, 0.12,
        0.0012, 0.053, 0.16, 1.1
    ],
    12: [
        0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11, 0.19, 0.18,
        0.0031, 0.082, 0.28, 2.0
    ]
}
PART_COUNT_PI_Q: Dict[int, List[float]] = {
    1: [0.7, 1.0, 2.4, 5.5, 8.0],
    3: [0.7, 1.0, 2.4, 5.5, 8.0],
    4: [0.7, 1.0, 2.4, 5.5, 8.0],
    5: [0.7, 1.0, 2.4, 5.5, 8.0],
    6: [0.7, 1.0, 2.4, 5.5, 8.0],
    7: [0.7, 1.0, 2.4, 5.5, 8.0],
    8: [0.7, 1.0, 2.4, 5.5, 8.0],
    9: [0.7, 1.0, 2.4, 5.5, 8.0],
    10: [0.7, 1.0, 2.4, 5.5, 8.0],
    11: [0.7, 1.0, 2.4, 5.5, 8.0],
    12: [0.7, 1.0, 2.4, 5.5, 8.0],
    13: [1.0, 1.0, 3.3]
}
PART_COUNT_PI_Q_HF_DIODE: List[List[float]] = [[0.5, 1.0, 5.0, 25, 50],
                                               [0.5, 1.0, 1.8, 2.5]]

PART_STRESS_PI_Q: Dict[int, List[float]] = {
    1: [0.7, 1.0, 2.4, 5.5, 8.0],
    3: [0.7, 1.0, 2.4, 5.5, 8.0],
    4: [0.7, 1.0, 2.4, 5.5, 8.0],
    5: [0.7, 1.0, 2.4, 5.5, 8.0],
    6: [0.5, 1.0, 2.0, 5.0],
    7: [0.5, 1.0, 2.0, 5.0],
    8: [0.5, 1.0, 2.0, 5.0],
    9: [0.5, 1.0, 2.0, 5.0],
    10: [0.7, 1.0, 2.4, 5.5, 8.0],
    11: [0.7, 1.0, 2.4, 5.5, 8.0],
    12: [0.7, 1.0, 2.4, 5.5, 8.0],
    13: [1.0, 1.0, 3.3]
}
PART_STRESS_PI_Q_HF_DIODE: Dict[int, List[float]] = {
    1: [0.5, 1.0, 5.0, 25.0, 50.0],
    2: [0.5, 1.0, 5.0, 25.0, 50.0],
    3: [0.5, 1.0, 5.0, 25.0, 50.0],
    4: [0.5, 1.0, 5.0, 25.0, 50.0],
    5: [0.5, 1.0, 1.8, 2.5],
    6: [0.5, 1.0, 5.0, 25.0, 50.0]
}
PI_A = {
    2: [0.5, 2.5, 1.0],
    3: [1.5, 0.7],
    4: [1.5, 0.7, 2.0, 4.0, 8.0, 10.0],
    8: [1.0, 4.0]
}

# Constants used to calculate the temperature factor (piT)
PI_T_DICT: Dict[int, List[float]] = {
    1: [2903.0, 0.1, 2.0],
    2: [5794.0, 0.38, 7.55]
}
PI_T_LIST: Dict[int, List[float]] = {
    1: [3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 1925.0, 1925.0],
    2: [5260.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0]
}
PI_T_SCALAR: Dict[int, float] = {
    3: 2114.0,
    4: 1925.0,
    5: 2483.0,
    6: 2114.0,
    8: 4485.0,
    9: 1925.0,
    10: 3082.0,
    11: 2790.0,
    12: 2790.0,
    13: 4635.0
}

# Constants used to calculate the junction temperature.
CASE_TEMPERATURE = [
    35.0, 45.0, 50.0, 45.0, 50.0, 60.0, 60.0, 75.0, 75.0, 60.0, 35.0, 50.0,
    60.0, 45.0
]
THETA_JC = [
    70.0, 10.0, 70.0, 70.0, 70.0, 70.0, 70.0, 5.0, 70.0, 70.0, 10.0, 70.0,
    70.0, 70.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 70.0, 70.0, 5.0, 22.0,
    70.0, 5.0, 70.0, 5.0, 5.0, 1.0, 10.0, 70.0, 70.0, 5.0, 5.0, 5.0, 10.0, 5.0,
    5.0, 10.0, 5.0, 10.0, 10.0, 10.0, 5.0, 70.0, 5.0, 70.0, 70.0, 70.0, 70.0,
    70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0,
    70.0
]

# Constants used to calculate the construction factor (piC).
PI_C = [1.0, 2.0]

PI_E = {
    1: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    2: [
        1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0, 24.0,
        250.0
    ],
    3: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    4: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    5: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    6: [
        1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0, 24.0,
        250.0
    ],
    7: [
        1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0, 24.0,
        250.0
    ],
    8: [
        1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 7.5, 24.0,
        250.0
    ],
    9: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    10: [
        1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
        32.0, 320.0
    ],
    11: [
        1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0, 24.0,
        450.0
    ],
    12: [
        1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0, 24.0,
        450.0
    ],
    13: [
        1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0, 24.0,
        450.0
    ]
}

# Constants used to calculate the matching factor (piM).
PI_M = [1.0, 2.0, 4.0]


def calculate_application_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the application factor (piA) for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown application ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _application_id: Any = attributes['application_id']
    _duty_cycle: Any = attributes['duty_cycle']

    _pi_a: Any = 1.0
    if _subcategory_id in [2, 3, 4, 8]:
        _pi_a = PI_A[_subcategory_id][_application_id - 1]
    elif _subcategory_id == 7:
        if _application_id == 1:
            _pi_a = 7.6
        else:
            _pi_a = 0.06 * (_duty_cycle / 100.0) + 0.4
    elif _subcategory_id == 13:
        if _application_id == 1:
            _pi_a = 4.4
        else:
            _pi_a = sqrt(_duty_cycle / 100.0)
    else:
        _pi_a = 0.0

    attributes['piA'] = _pi_a

    return attributes


def calculate_electrical_stress_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the electrical stress factor for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    """
    _subcategory_id: Any = int(attributes['subcategory_id'])
    _type_id: Any = int(attributes['type_id'])
    _voltage_ratio: Any = float(attributes['voltage_ratio'])

    _pi_s: Any = 1.0
    if _subcategory_id == 1:
        if _type_id > 5:
            _pi_s = 1.0
        elif _voltage_ratio <= 0.3:
            _pi_s = 0.054
        else:
            _pi_s = _voltage_ratio**2.43
    elif _subcategory_id in [3, 6]:
        _pi_s = 0.045 * exp(3.1 * _voltage_ratio)
    elif _subcategory_id == 10:
        if _voltage_ratio <= 0.3:
            _pi_s = 0.1
        else:
            _pi_s = _voltage_ratio**1.9
    else:
        _pi_s = 0.0

    attributes['piS'] = _pi_s

    return attributes


def calculate_junction_temperature(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the junction temperature of the semiconductor device.

    .. note:: This function will also estimate the case temperature if it is
        passed in at less than or equal to zero.

    .. note:: This function will also estimate the junction-case thermal
        resistance (thetaJC) if it is passed in at less than or equal to zero.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown active environment ID when the case
        temperature is passed at <=0.0 or an unknown package ID when the
        junction-case thermal resistance is passed at <=0.0.
    """
    _environment_active_id: Any = int(attributes['environment_active_id'])
    _package_id: Any = int(attributes['package_id'])
    _temperature_case: Any = float(attributes['temperature_case'])
    _theta_jc: Any = float(attributes['theta_jc'])
    _power_operating: Any = float(attributes['power_operating'])

    _temperature_junction: Any = 0.0
    if _temperature_case <= 0.0:
        _temperature_case = CASE_TEMPERATURE[_environment_active_id - 1]
    if _theta_jc <= 0.0:
        _theta_jc = THETA_JC[_package_id - 1]
    _temperature_junction = (_temperature_case + _theta_jc * _power_operating)

    attributes['temperature_case'] = _temperature_case
    attributes['temperature_junction'] = _temperature_junction
    attributes['theta_jc'] = _theta_jc

    return attributes


def calculate_part_count(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the parts count hazard rate for a semiconductor.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values.
    :rtype: dict
    """
    _lambda_b: Any = get_part_count_lambda_b(attributes)
    attributes['lambda_b'] = _lambda_b

    return attributes


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the part stress active hazard rate for a semiconductor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    :raise: IndexError if passed an unknown construction ID or matching ID.
    """
    attributes = get_part_stress_quality_factor(attributes)
    attributes = calculate_part_stress_lambda_b(attributes)
    attributes = calculate_junction_temperature(attributes)
    attributes = calculate_temperature_factor(attributes)
    attributes = calculate_application_factor(attributes)
    attributes = calculate_power_rating_factor(attributes)
    attributes = calculate_electrical_stress_factor(attributes)

    _lambda_b: Any = attributes['lambda_b']
    _pi_a: Any = attributes['piA']
    _pi_e: Any = attributes['piE']
    _pi_q: Any = attributes['piQ']
    _pi_r: Any = attributes['piR']
    _pi_s: Any = attributes['piS']
    _pi_t: Any = attributes['piT']

    # Retrieve the construction factor (piC).
    _construction_id: Any = attributes['construction_id']
    _pi_c: Any = PI_C[_construction_id - 1]
    attributes['piC'] = _pi_c

    # Retrieve the matching network factor (piM).
    _matching_id: Any = attributes['matching_id']
    _pi_m: Any = PI_M[_matching_id - 1]
    attributes['piM'] = _pi_m

    # Calculate forward current factor (piI) and power degradation factor (piP)
    _current_operating: Any = attributes['current_operating']
    _pi_i: Any = _current_operating**0.68
    attributes['piI'] = _pi_i
    _power_ratio: Any = attributes['power_ratio']
    _pi_p: Any = 1.0 / (2.0 * (1.0 - _power_ratio))
    attributes['piP'] = _pi_p

    _hazard_rate_active: Any = (_lambda_b * _pi_t * _pi_q * _pi_e)

    if attributes['subcategory_id'] == 1:
        _hazard_rate_active = (_hazard_rate_active * _pi_s * _pi_c)
    elif attributes['subcategory_id'] == 2:
        _hazard_rate_active = (_hazard_rate_active * _pi_a * _pi_r)
    elif attributes['subcategory_id'] == 3:
        _hazard_rate_active = (_hazard_rate_active * _pi_a * _pi_r * _pi_s)
    elif attributes['subcategory_id'] == 4:
        _hazard_rate_active = (_hazard_rate_active * _pi_a)
    elif attributes['subcategory_id'] in [6, 10]:
        _hazard_rate_active = (_hazard_rate_active * _pi_r * _pi_s)
    elif attributes['subcategory_id'] in [7, 8]:
        _hazard_rate_active = (_hazard_rate_active * _pi_a * _pi_m)
    elif attributes['subcategory_id'] == 13:
        _hazard_rate_active = (_hazard_rate_active * _pi_i * _pi_a * _pi_p)

    attributes['hazard_rate_active'] = _hazard_rate_active

    return attributes


def calculate_part_stress_lambda_b(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve the MIL-HDBK-217F base hazard rate for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown type ID.
    :raise: KeyError if passed an unkown subcategory ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _application_id: Any = attributes['application_id']
    _type_id: Any = attributes['type_id']
    _frequency_operating: Any = attributes['frequency_operating']
    _power_operating: Any = attributes['power_operating']
    _n_elements: Any = attributes['n_elements']

    _dic_lambdab_scalar: Dict[int, float] = {
        3: 0.00074,
        5: 0.0083,
        6: 0.18,
        10: 0.0022
    }
    _dic_lambdab_list: Dict[int, List[float]] = {
        1: [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034, 0.002],
        2: [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025, 0.0025],
        4: [0.012, 0.0045],
        9: [0.06, 0.023],
        11: [
            0.0055, 0.004, 0.0025, 0.013, 0.013, 0.0064, 0.0033, 0.017, 0.017,
            0.0086, 0.0013, 0.00023
        ],
        13: [3.23, 5.65]
    }

    _lambda_b: Any = 0.0
    if _subcategory_id in [3, 5, 6, 10]:
        _lambda_b = _dic_lambdab_scalar[_subcategory_id]
    elif _subcategory_id == 7:
        _lambda_b = 0.032 * exp(0.354 * _frequency_operating
                                + 0.00558 * _power_operating)
    elif _subcategory_id == 8:
        if 1.0 < _frequency_operating <= 10.0 and _power_operating < 0.1:
            _lambda_b = 0.052
        else:
            _lambda_b = 0.0093 * exp(0.429 * _frequency_operating
                                     + 0.486 * _power_operating)
    elif _subcategory_id == 12:
        if _application_id in [1, 3]:
            _lambda_b = 0.00043 * _n_elements + 0.000043
        else:
            _lambda_b = 0.00043 * _n_elements
    else:
        _lambda_b = _dic_lambdab_list[_subcategory_id][_type_id - 1]

    attributes['lambda_b'] = _lambda_b

    return attributes


def calculate_power_rating_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the power rating factor for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: TypeError if passed a string for the rated power or rated current.
    :raise: ValueError if passed a rated power <=0.0.
    """
    _subcategory_id: Any = int(attributes['subcategory_id'])
    _type_id: Any = int(attributes['type_id'])
    _power_rated: Any = float(attributes['power_rated'])
    _current_rated: Any = float(attributes['current_rated'])

    _pi_r: Any = 1.0
    if _subcategory_id == 2:
        if _type_id == 4:
            _pi_r = 0.326 * log(_power_rated) - 0.25
        else:
            _pi_r = 1.0
    elif _subcategory_id in [3, 6]:
        if _power_rated < 0.1:
            _pi_r = 0.43
        else:
            _pi_r = _power_rated**0.37
    elif _subcategory_id == 10:
        _pi_r = _current_rated**0.4
    else:
        _pi_r = 0.0

    attributes['piR'] = _pi_r

    return attributes


def calculate_temperature_factor(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the temperature factor for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown type ID.
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _type_id: Any = attributes['type_id']
    _voltage_ratio: Any = attributes['voltage_ratio']
    _temperature_junction: Any = attributes['temperature_junction']

    if _subcategory_id in [1, 2]:
        _factors = PI_T_LIST[_subcategory_id][_type_id - 1]
    elif _subcategory_id == 7:
        _factors = PI_T_DICT[_type_id]
    else:
        _factors = PI_T_SCALAR[_subcategory_id]

    _pi_t: Any = 1.0
    if _subcategory_id == 7:
        _f0 = _factors[0]
        _f1 = _factors[1]
        _f2 = _factors[2]
        if _voltage_ratio <= 0.4:
            _pi_t = _f1 * exp(-_f0 *
                              (1.0 /
                               (_temperature_junction + 273.0) - 1.0 / 298.0))
        else:
            _pi_t = _f2 * (_voltage_ratio - 0.35) * exp(
                -_f0 * (1.0 / (_temperature_junction + 273.0) - 1.0 / 298.0))
    else:
        _pi_t = exp(-_factors *
                    (1.0 / (_temperature_junction + 273.0) - 1.0 / 298.0))

    attributes['piT'] = _pi_t

    return attributes


def get_part_count_lambda_b(attributes: Dict[str, Any]) -> float:
    r"""
    Retrieve the MIL-HDBK-217F base hazard rate for the semiconductor device.

    This function retrieves the MIL-HDBK-217F hazard rate from the dictionary
    PART_COUNT_LAMBDA_B.  Keys are for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id; if the semiconductor subcategory is NOT type dependent,
            then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |          Semiconductor \      | MIL-HDBK-217F \ |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Diode, Low Frequency          |        6.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Diode, High Frequency         |        6.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Transistor, Low Frequency, \  |        6.3      |
    |                | Bipolar                       |                 |
    +----------------+-------------------------------+-----------------+
    |        4       | Transistor, Low Frequency, \  |        6.4      |
    |                | Si FET                        |                 |
    +----------------+-------------------------------+-----------------+
    |        5       | Transistor, Unijunction       |        6.5      |
    +----------------+-------------------------------+-----------------+
    |        6       | Transistor, High Frequency, \ |        6.6      |
    |                | Low Noise,Bipolar             |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Transistor, High Frequency, \ |        6.7      |
    |                | High Power, Bipolar           |                 |
    +----------------+-------------------------------+-----------------+
    |        8       | Transistor, High Frequency, \ |        6.8      |
    |                | GaAs FET                      |                 |
    +----------------+-------------------------------+-----------------+
    |        9       | Transistor, High Frequency, \ |        6.9      |
    |                | Si FET                        |                 |
    +----------------+-------------------------------+-----------------+
    |       10       | Thyristor/SCR                 |       6.10      |
    +----------------+-------------------------------+-----------------+
    |       11       | Optoelectronic, Detector, \   |       6.11      |
    |                | Isolator, Emitter             |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Optoelectronic, Alphanumeric \|       6.12      |
    |                | Display                       |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Optoelectronic, Laser Diode   |       6.13      |
    +----------------+-------------------------------+-----------------+

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _environment_active_id: Any = attributes['environment_active_id']
    _type_id: Any = attributes['type_id']

    _base_hr: float = 1.0
    if _subcategory_id in [1, 2, 3, 8, 11, 13]:
        _base_hr = PART_COUNT_LAMBDA_B_DICT[_subcategory_id][_type_id][
            _environment_active_id - 1]
    else:
        _base_hr = PART_COUNT_LAMBDA_B_LIST[_subcategory_id][
            _environment_active_id - 1]

    return _base_hr


def get_part_count_quality_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve the parts count quality factor for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown quality ID.
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _quality_id: Any = attributes['quality_id']
    _type_id: Any = attributes['type_id']

    _pi_q: Any = 1.0
    if _subcategory_id == 2:
        if _type_id == 5:
            _pi_q = PART_COUNT_PI_Q_HF_DIODE[1][_quality_id - 1]
        else:
            _pi_q = PART_COUNT_PI_Q_HF_DIODE[0][_quality_id - 1]
    else:
        _pi_q = PART_COUNT_PI_Q[_subcategory_id][_quality_id - 1]

    attributes['piQ'] = _pi_q

    return attributes


def get_part_stress_quality_factor(
        attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Select the part stress quality factor for the semiconductor device.

    :param dict attributes: the attributes of the semiconductor being
        calculated.
    :return attributes: the updated attributes of the semiconductor being
        calculated.
    :rtype: dict
    :raise: IndexError if passed an unknown quality ID.
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _subcategory_id: Any = attributes['subcategory_id']
    _quality_id: Any = attributes['quality_id']
    _type_id: Any = attributes['type_id']

    _pi_q: Any = 1.0
    if _subcategory_id == 2:
        _pi_q = PART_STRESS_PI_Q_HF_DIODE[_type_id][_quality_id - 1]
    else:
        _pi_q = PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]

    attributes['piQ'] = _pi_q

    return attributes
