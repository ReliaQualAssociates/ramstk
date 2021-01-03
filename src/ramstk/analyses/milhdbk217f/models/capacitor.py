# -*- coding: utf-8 -*-
#
#       ramstk.analyses.functions.mil_hdbk_217f.Capacitor.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.0036, 0.0072, 0.330, 0.016, 0.055, 0.023, 0.030, 0.07, 0.13,
            0.083, 0.0018, 0.044, 0.12, 2.1
        ],
        2: [
            0.0039, 0.0087, 0.042, 0.022, 0.070, 0.035, 0.047, 0.19, 0.35,
            0.130, 0.0020, 0.056, 0.19, 2.5
        ]
    },
    2: [
        0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030, 0.040, 0.094, 0.15, 0.11,
        0.0024, 0.058, 0.18, 2.7
    ],
    3: [
        0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068, 0.013, 0.026, 0.048,
        0.044, 0.0010, 0.023, 0.063, 1.1
    ],
    4: [
        0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012, 0.018, 0.037, 0.066, 0.060,
        0.0014, 0.032, 0.088, 1.5
    ],
    5: [
        0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026, 0.048, 0.086, 0.14, 0.10,
        0.0020, 0.054, 0.15, 2.5
    ],
    6: [
        0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096, 0.014, 0.034, 0.053,
        0.048, 0.0011, 0.026, 0.07, 1.2
    ],
    7: [
        0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095, 0.054, 0.069,
        0.031, 0.00025, 0.012, 0.046, 0.45
    ],
    8: [
        0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60, 0.48, 0.0091,
        0.25, 0.68, 11.0
    ],
    9: [
        0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062, 0.035, 0.045,
        0.020, 0.00016, 0.0076, 0.030, 0.29
    ],
    10: [
        0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015, 0.015, 0.032, 0.048, 0.077,
        0.0014, 0.049, 0.13, 2.3
    ],
    11: [
        0.00078, 0.0022, 0.013, 0.0056, 0.023, 0.0077, 0.015, 0.053, 0.12,
        0.048, 0.00039, 0.017, 0.065, 0.68
    ],
    12: [
        0.0018, 0.0039, 0.016, 0.0097, 0.028, 0.0091, 0.011, 0.034, 0.057,
        0.055, 0.00072, 0.022, 0.066, 1.0
    ],
    13: [
        0.0061, 0.013, 0.069, 0.039, 0.11, 0.031, 0.061, 0.13, 0.29, 0.18,
        0.0030, 0.069, 0.26, 4.0
    ],
    14: [
        0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6, 1.2, .012, 0.49,
        1.7, 21.0
    ],
    15: [
        0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4, 2.0, 0.015, 0.68,
        2.8, 28.0
    ],
    16: [
        0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9, 5.9,
        85.0
    ],
    17: [
        0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16, 0.93,
        3.2, 37.0
    ],
    18: [
        0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5, 8.9,
        100.0
    ],
    19: [
        0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0, 0.0,
        0.0
    ]
}
PART_COUNT_PI_Q = [0.030, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0]
PART_STRESS_PI_Q = {
    1: [3.0, 7.0],
    2: [1.0, 3.0, 10.0],
    3: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0],
    4: [0.03, 0.1, 0.3, 1.0, 3.0, 7.0, 20.0],
    5: [0.03, 0.1, 0.3, 1.0, 10.0],
    6: [0.02, 0.1, 0.3, 1.0, 10.0],
    7: [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 6.0, 15.0],
    8: [5.0, 15.0],
    9: [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0],
    10: [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0],
    11: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
    12: [0.001, 0.01, 0.03, 0.03, 0.1, 0.3, 1.0, 1.5, 10.0],
    13: [0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0],
    14: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
    15: [3.0, 10.0],
    16: [4.0, 20.0],
    17: [3.0, 10.0],
    18: [5.0, 20.0],
    19: [3.0, 20.0]
}
PI_C = {1: 0.3, 2: 1.0, 3: 2.0, 4: 2.5, 5: 3.0}
PI_CF = {1: 0.1, 2: 1.0}
PI_E = [
    1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0, 32.0,
    320.0
]
REF_TEMPS = {
    65.0: 338.0,
    70.0: 343.0,
    85.0: 358.0,
    105.0: 378.0,
    125.0: 398.0,
    150.0: 423.0,
    170.0: 443.0,
    175.0: 448.0,
    200.0: 473.0
}


def calculate_capacitance_factor(subcategory_id: int,
                                 capacitance: float) -> float:
    """Calculate the capacitance factor (piCV).

    :param subcategory_id: the capacitor subcategory identifier.
    :param capacitance: the capacitance value in Farads.
    :return: _pi_cv; the calculated capacitance factor.
    :rtype: float
    :raise: KeyError if passed an unknown subcategor ID.
    """
    _dic_factors = {
        1: [1.2, 0.095],
        2: [1.4, 0.12],
        3: [1.6, 0.13],
        4: [1.2, 0.092],
        5: [1.1, 0.085],
        6: [1.2, 0.092],
        7: [0.45, 0.14],
        8: [0.31, 0.23],
        9: [0.62, 0.14],
        10: [0.41, 0.11],
        11: [0.59, 0.12],
        12: [1.0, 0.12],
        13: [0.82, 0.066],
        14: [0.34, 0.18],
        15: [0.321, 0.19],
        16: [1.0, 0.0],
        17: [1.0, 0.0],
        18: [1.0, 0.0],
        19: [1.0, 0.0]
    }
    _f0 = _dic_factors[subcategory_id][0]
    _f1 = _dic_factors[subcategory_id][1]
    _pi_cv = _f0 * capacitance**_f1

    return _pi_cv


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b_list function.

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the capacitor being calculated.
    :return: _base_hr; the base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID or specification ID.
    """
    return get_part_count_lambda_b(
        attributes['subcategory_id'],  # type: ignore
        attributes['environment_active_id'],  # type: ignore
        attributes['specification_id'])  # type: ignore


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress active hazard rate for a capacitor.

    :param attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    :raise: KeyError if the attribute dict is missing one or more keys.
    """
    attributes['lambda_b'] = calculate_part_stress_lambda_b(  # type: ignore
        attributes['subcategory_id'],  # type: ignore
        attributes['temperature_rated_max'],  # type: ignore
        attributes['temperature_active'],  # type: ignore
        attributes['voltage_ratio'])  # type: ignore
    attributes['piCV'] = calculate_capacitance_factor(  # type: ignore
        attributes['subcategory_id'],  # type: ignore
        attributes['capacitance'])  # type: ignore

    attributes['hazard_rate_active'] = (
        attributes['lambda_b']  # type: ignore
        * attributes['piQ'] * attributes['piE'] * attributes['piCV'])
    if attributes['subcategory_id'] == 12:
        attributes[
            'piSR'] = calculate_series_resistance_factor(  # type: ignore
                attributes['resistance'],  # type: ignore
                attributes['voltage_dc_operating'],  # type: ignore
                attributes['voltage_ac_operating'])  # type: ignore
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active']  # type: ignore
            * attributes['piSR'])  # type: ignore
    elif attributes['subcategory_id'] == 13:
        attributes['piC'] = get_construction_factor(  # type: ignore
            attributes['construction_id'])  # type: ignore
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active']  # type: ignore
            * attributes['piC'])
    elif attributes['subcategory_id'] == 19:
        attributes['piCF'] = get_configuration_factor(  # type: ignore
            attributes['configuration_id'])  # type: ignore
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active']  # type: ignore
            * attributes['piCF'] / attributes['piCV'])

    return attributes


def calculate_part_stress_lambda_b(subcategory_id: int,
                                   temperature_rated_max: float,
                                   temperature_active: float,
                                   voltage_ratio: float) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    :param subcategory_id: the capacitor subcategory identifier.
    :param temperature_rated_max: the maximum rated temperature of the
        capacitor.
    :param temperature_active: the operating ambient temperature of the
        capacitor.
    :param voltage_ratio: the ratio of operating to rated voltage for the
        capacitor.
    :return: _base_hr; the calculates base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID.
    """
    _dic_factors = {
        1: [0.00086, 0.4, 5.0, 2.5, 1.8],
        2: [0.00115, 0.4, 5.0, 2.5, 1.8],
        3: [0.0005, 0.4, 5.0, 2.5, 1.8],
        4: [0.00069, 0.4, 5.0, 2.5, 1.8],
        5: [0.00099, 0.4, 5.0, 2.5, 1.8],
        6: [0.00055, 0.4, 5.0, 2.5, 1.8],
        7: [8.6E-10, 0.4, 3.0, 16.0, 1.0],
        8: [0.0053, 0.4, 3.0, 1.2, 6.3],
        9: [8.25E-10, 0.5, 4.0, 16.0, 1.0],
        10: [0.0003, 0.3, 3.0, 1.0, 1.0],
        11: [2.6E-9, 0.3, 3.0, 14.3, 1.0],
        12: [0.00375, 0.4, 3.0, 2.6, 9.0],
        13: [0.00165, 0.4, 3.0, 2.6, 9.0],
        14: [0.00254, 0.5, 3.0, 5.09, 5.0],
        15: [0.0028, 0.55, 3.0, 4.09, 5.9],
        16: [0.00224, 0.17, 3.0, 1.59, 10.1],
        17: [7.3E-7, 0.33, 3.0, 12.1, 1.0],
        18: [1.92E-6, 0.33, 3.0, 10.8, 1.0],
        19: [0.0112, 0.17, 3.0, 1.59, 10.1]
    }

    # This will retrieve the reference temperature for the maximum rated
    # temperature closest (round up) to one of the keys in the REF_TEMPS dict.
    _ref_temp = REF_TEMPS.get(
        temperature_rated_max,
        REF_TEMPS[min(REF_TEMPS.keys(),
                      key=lambda k: abs(k - temperature_rated_max))])
    _f0 = _dic_factors[subcategory_id][0]
    _f1 = _dic_factors[subcategory_id][1]
    _f2 = _dic_factors[subcategory_id][2]
    _f3 = _dic_factors[subcategory_id][3]
    _f4 = _dic_factors[subcategory_id][4]
    _lambda_b = _f0 * ((voltage_ratio / _f1)**_f2 + 1.0) * exp(_f3 * (
        (temperature_active + 273.0) / _ref_temp)**_f4)

    return _lambda_b


def calculate_series_resistance_factor(resistance: float,
                                       voltage_dc_operating: float,
                                       voltage_ac_operating: float) -> float:
    """Calculate the series resistance factor (piSR).

    :param resistance: the equivalent series resistance of the capacitor.
    :param voltage_dc_operating: the operating DC voltage.
    :param voltage_ac_operating: the operating ac voltage (ripple
        voltage).
    :return: _pi_sr, _error_msg; the series resistance factor and any error
        message raised by this function.
    :rtype: tuple
    :raise: TypeError if passed a non-numerical input.
    :raise: ZeroDivisionError if passed both ac and DC voltages = 0.0.
    """
    _ckt_resistance = resistance / (voltage_dc_operating
                                    + voltage_ac_operating)

    if 0 < _ckt_resistance <= 0.1:
        _pi_sr = 0.33
    elif 0.1 < _ckt_resistance <= 0.2:
        _pi_sr = 0.27
    elif 0.2 < _ckt_resistance <= 0.4:
        _pi_sr = 0.2
    elif 0.4 < _ckt_resistance <= 0.6:
        _pi_sr = 0.13
    elif 0.6 < _ckt_resistance <= 0.8:
        _pi_sr = 0.1
    else:
        _pi_sr = 0.066

    return _pi_sr


def get_configuration_factor(configuration_id: int) -> float:
    """Retrieve the configuration factor (piCF) for the capacitor.

    :param configuration_id: the capacitor configuration identifier.
    :return: _pi_cf; the configuration factor value.
    :rtype: float
    :raise: KeyError if passed an unknown configuration ID.
    """
    return PI_CF[configuration_id]


def get_construction_factor(construction_id: int) -> float:
    """Retrieve the configuration factor (piC) for the capacitor.

    :param construction_id: the capacitor construction identifier.
    :return: _pi_c; the construction factor value.
    :rtype: float
    :raise: KeyError if passed an unknown construction ID.
    """
    return PI_C[construction_id]


def get_part_count_lambda_b(subcategory_id: int,
                            environment_active_id: int,
                            specification_id: int = -1) -> float:
    """Retrieve the MIL-HDBK-217F parts count base hazard rate (lambda b).

    The dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217F parts count
    base hazard rates.  Keys are for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. specification id; if the capacitor subcategory is NOT specification
           dependent, then pass -1 for the specification ID key.

    Subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory ID |         Capacitor Style       | MIL-HDBK-217F   |
    |                |                               | Section         |
    +================+===============================+=================+
    |        1       | Fixed, Paper, Bypass (CA, CP) |       10.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Feed-Through (CZ, CZR) |       10.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Paper and Plastic      |       10.3      |
    |                | Film (CPV, CQ, CQR)           |                 |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Metallized Paper,      |       10.4      |
    |                | Paper-Plastic and Plastic     |                 |
    |                | (CH, CHR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Plastic and            |       10.5      |
    |                | Metallized Plastic (CFR)      |                 |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Super-Metallized       |       10.6      |
    |                | Plastic (CRH)                 |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Mica (CM, CMR)         |       10.7      |
    +----------------+-------------------------------+-----------------+
    |        8       | Fixed, Mica, Button (CB)      |       10.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Fixed, Glass (CY, CYR)        |       10.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Fixed, Ceramic, General       |      10.10      |
    |                | Purpose (CK, CKR)             |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Fixed, Ceramic, Temperature   |      10.11      |
    |                | Compensating and Chip         |                 |
    |                | (CC, CCR, CDR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Fixed, Electrolytic,          |      10.12      |
    |                | Tantalum, Solid (CSR)         |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Fixed, Electrolytic,          |      10.13      |
    |                | Tantalum, Non-Solid (CL, CLR) |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Fixed, Electrolytic,          |      10.14      |
    |                | Aluminum (CU, CUR)            |                 |
    +----------------+-------------------------------+-----------------+
    |       15       | Fixed, Electrolytic (Dry),    |      10.15      |
    |                | Aluminum (CE)                 |                 |
    +----------------+-------------------------------+-----------------+
    |       16       | Variable, Ceramic (CV)        |      10.16      |
    +----------------+-------------------------------+-----------------+
    |       17       | Variable, Piston Type (PC)    |      10.17      |
    +----------------+-------------------------------+-----------------+
    |       18       | Variable, Air Trimmer (CT)    |      10.18      |
    +----------------+-------------------------------+-----------------+
    |       19       | Variable and Fixed, Gas or    |      10.19      |
    |                | Vacuum (CG)                   |                 |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param subcategory_id: the capacitor subcategory identifier.
    :param environment_active_id: the ID of the active (operating)
        environment.
    :param specification_id: the capacitor specification identifier.
        Default is -1.
    :return: _base_hr; the MIL-HDBK-217F part count base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID or specification ID.
    """
    if subcategory_id == 1:
        _base_hr = PART_COUNT_LAMBDA_B[subcategory_id][  # type: ignore
            specification_id][environment_active_id - 1]
    else:
        _base_hr = PART_COUNT_LAMBDA_B[subcategory_id][  # type: ignore
            environment_active_id - 1]

    return _base_hr
