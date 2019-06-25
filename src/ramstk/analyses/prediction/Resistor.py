# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Reliability Calculations Module."""

# Standard Library Imports
from math import exp

PART_COUNT_217F_LAMBDA_B = {
    1: [
        0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016,
        0.025, 0.025, 0.00025, 0.0098, 0.035, 0.36,
    ],
    2: {
        1: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018,
            0.033, 0.030, 0.00025, 0.014, 0.044, 0.69,
        ],
        2: [
            0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018,
            0.033, 0.030, 0.00025, 0.014, 0.044, 0.69,
        ],
        3: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021,
            0.038, 0.034, 0.00028, 0.016, 0.050, 0.78,
        ],
        4: [
            0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021,
            0.038, 0.034, 0.00028, 0.016, 0.050, 0.78,
        ],
    },
    3: [
        0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19, 0.24, 0.32,
        0.0060, 0.18, 0.47, 8.2,
    ],
    4: [
        0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043, 0.077, 0.15,
        0.10, 0.0011, 0.055, 0.15, 1.7,
    ],
    5: [
        0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30, 0.38, 0.26,
        0.0068, 0.13, 0.37, 5.4,
    ],
    6: {
        1: [
            0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19, 0.39, 0.42,
            0.0042, 0.21, 0.62, 9.4,
        ],
        2: [
            0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18, 0.35, 0.38,
            0.0038, 0.19, 0.56, 8.6,
        ],
    },
    7: [
        0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12, 0.24, 0.25,
        0.004, 0.13, 0.37, 5.5,
    ],
    8: [
        0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7, 2.4, 0.032, 1.3,
        3.4, 62.0,
    ],
    9: [
        0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35, 0.58, 1.1, 0.013,
        0.52, 1.6, 24.0,
    ],
    10: [
        0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0, 0.16, 11.0,
        33.0, 510.0,
    ],
    11: [
        0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0, 0.075, 0.0,
        0.0, 0.0,
    ],
    12: [
        0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6, 0.076, 0.0,
        0.0, 0.0,
    ],
    13: [
        0.043, 0.15, 0.75, 0.35, 1.3, 0.39, 0.78, 1.8, 2.8, 2.5, 0.21, 1.2,
        3.7, 49.0,
    ],
    14: [
        0.05, 0.11, 1.1, 0.45, 1.7, 2.8, 4.6, 4.6, 7.5, 3.3, 0.025, 1.5,
        4.7, 67.0,
    ],
    15: [
        0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2, 2.3, 0.024,
        1.2, 3.4, 52.0,
    ],
}
PI_C = {10: [2.0, 1.0, 3.0, 1.5], 12: [2.0, 1.0]}
PI_R = {
    1: [1.0, 1.1, 1.6, 2.5],
    2: [1.0, 1.1, 1.6, 2.5],
    3: [1.0, 1.2, 1.3, 3.5],
    5: [1.0, 1.7, 3.0, 5.0],
    6: [
        [
            [1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0, ],
            [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6, ],
            [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0, ],
        ],
        [
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6, ],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0, ],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0, ],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.6, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.2, 0.0, 0.0, ],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, ],
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 1.5, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 1.6, 0.0, ],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0, ],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0, ],
            [1.0, 1.0, 1.4, 2.4, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 2.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, ],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0, ],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.0, 1.6, 0.0, 0.0, ],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, ],
            [1.0, 1.2, 1.5, 0.0, 0.0, 0.0, ],
            [1.0, 1.2, 0.0, 0.0, 0.0, 0.0, ],
        ],
    ],
    7: [
        [
            [1.0, 1.2, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.2, 1.6, 0.0], [1.0, 1.0, 1.0, 1.1, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6], [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
        ],
        [
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0], [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0], [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0], [1.0, 1.0, 1.0, 1.1, 1.4, 0.0],
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
REF_TEMPS = {
    1: 343.0,
    2: {
        1: 343.0,
        2: 343.0,
        3: 398.0,
        4: 398.0,
    },
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

def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param dict attributes: the attributes for the resistor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    _dic_factors = {
        1: [4.5E-9, 12.0, 1.0, 0.6, 1.0, 1.0],
        2: {
            1: [3.25E-4, 1.0, 3.0, 1.0, 1.0, 1.0],
            2: [3.25E-4, 1.0, 3.0, 1.0, 1.0, 1.0],
            3: [5.0E-5, 3.5, 1.0, 1.0, 1.0, 1.0],
            4: [5.0E-5, 3.5, 1.0, 1.0, 1.0, 1.0],
        },
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
        15: [0.018, 1.0, 7.4, 2.55, 3.6, 1.0],
    }

    if attributes['subcategory_id'] == 2:
        _ref_temp = REF_TEMPS[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ]
        _f0 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][0]
        _f1 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][1]
        _f2 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][2]
        _f3 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][3]
        _f4 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][4]
        _f5 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'specification_id'
            ]
        ][5]
    elif attributes['subcategory_id'] not in [4, 8]:
        _ref_temp = REF_TEMPS[attributes['subcategory_id']]
        _f0 = _dic_factors[attributes['subcategory_id']][0]
        _f1 = _dic_factors[attributes['subcategory_id']][1]
        _f2 = _dic_factors[attributes['subcategory_id']][2]
        _f3 = _dic_factors[attributes['subcategory_id']][3]
        _f4 = _dic_factors[attributes['subcategory_id']][4]
        _f5 = _dic_factors[attributes['subcategory_id']][5]

    if attributes['subcategory_id'] == 4:
        attributes['lambda_b'] = 0.00006
    elif attributes['subcategory_id'] == 8:
        attributes['lambda_b'] = _dic_factors[attributes['subcategory_id']][
            attributes['type_id'] - 1
        ]
    else:
        attributes['lambda_b'] = _f0 * exp(
            _f1 * (
                (attributes['temperature_active'] + 273.0) / _ref_temp
            ),
        )**_f2 * exp(
            (
                (attributes['power_ratio'] / _f3) * (
                    (attributes['temperature_active'] + 273.0) / 273.0
                )**_f4
            )**_f5,
        )

    return attributes


def _calculate_temperature_factor(attributes):
    """Calculate the temperature factor (piT)."""
    if attributes['subcategory_id'] == 4:
        attributes['temperature_case'] = (
            attributes['temperature_active']
            + 55.0 * attributes['power_ratio']
        )
        attributes['piT'] = exp(
            -4056.0 * (
                (1.0 / (attributes['temperature_case'] + 273.0)) - 1.0 / 298.0
            ),
        )

    return attributes


def _calculate_voltage_factor(attributes):
    """Calculate the voltage factor (piV)."""
    if attributes['subcategory_id'] > 8:
        _index = -1
        if attributes['subcategory_id'] in [9, 10, 11, 12]:
            _breaks = [0.1, 0.2, 0.6, 0.7, 0.8, 0.9]
        elif attributes['subcategory_id'] in [13, 14, 15]:
            _breaks = [0.8, 0.9]
        for _index, _value in enumerate(_breaks):
            _diff = _value - attributes['voltage_ratio']
            if len(_breaks) == 1 and _diff < 0.0:
                break
            elif _index == 0 and _diff >= 0.0:
                break
            elif _diff >= 0:
                break
        attributes['piV'] = PI_V[attributes['subcategory_id']][_index]

    return attributes


def _calculate_resistance_factor(attributes):
    """Calculate the resistance factor (piR)."""
    _dic_breakpoints = {
        1: [1.0E5, 1.0E6, 1.0E7],
        2: [1.0E5, 1.0E6, 1.0E7],
        3: [100.0, 1.0E5, 1.0E6],
        5: [1.0E4, 1.0E5, 1.0E6],
        6: [
            [500.0, 1.0E3, 5.0E3, 7.5E3, 1.0E4, 1.5E4, 2.0E4],
            [100.0, 1.0E3, 1.0E4, 1.0E5, 1.5E5, 2.0E5],
        ],
        7: [500.0, 1.0E3, 5.0E3, 1.0E4, 2.0E4],
        9: [2.0E3, 5.0E3],
        10: [1.0E4, 2.0E4, 5.0E4, 1.0E5, 2.0E5],
        11: [2.0E3, 5.0E3],
        12: [2.0E3, 5.0E3],
        13: [5.0E4, 1.0E5, 2.0E5, 5.0E5],
        14: [5.0E4, 1.0E5, 2.0E5, 5.0E5],
        15: [1.0E4, 5.0E4, 2.0E5, 1.0E6],
    }

    if attributes['subcategory_id'] not in [4, 8]:
        _index = -1
        if attributes['subcategory_id'] == 6:
            _breaks = _dic_breakpoints[attributes['subcategory_id']][
                attributes['specification_id'] - 1
            ]
        else:
            _breaks = _dic_breakpoints[attributes['subcategory_id']]

        for _index, _value in enumerate(_breaks):
            _diff = _value - attributes['n_elements']
            if len(_breaks) == 1 and _diff < 0:
                break
            elif _diff >= 0:
                break

        # Resistance factor (piR) dictionary of values.  The key is the
        # subcategory ID.  The index in the returned list is the resistance
        # range breakpoint (breakpoint values are in _lst_breakpoints below).
        # For subcategory ID 6 and 7, the specification ID selects the correct
        # set of lists, then the style ID selects the proper list of piR values
        # and then the resistance range breakpoint is used to select
        if attributes['subcategory_id'] in [6, 7]:
            attributes['piR'] = PI_R[attributes['subcategory_id']][
                attributes['specification_id'] - 1
            ][
                attributes['family_id'] - 1
            ][_index + 1]
        elif attributes['subcategory_id'] not in [4, 8]:
            attributes['piR'] = PI_R[attributes['subcategory_id']][
                _index + 1
            ]

    return attributes


def calculate_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. specification id; if the resistor subcategory is NOT specification
            dependent, then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |            Resistor \         | MIL-HDBK-217F \ |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Fixed, Composition (RC, RCR)  |        9.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Film (RL, RLR, RN, \   |        9.2      |
    |                | RNC, RNN, RNR)                |                 |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Film, Power (RD)       |        9.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Film, Network (RZ)     |        9.4      |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Wirewound (RB, RBR)    |        9.5      |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Wirewound, Power \     |        9.6      |
    |                | (RW, RWR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Wirewound, Power, \    |        9.7      |
    |                | Chassis Mounted (RE, RER)     |                 |
    +----------------+-------------------------------+-----------------+
    |        8       | Thermistor                    |        9.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Variable, Wirewound (RT, RTR) |        9.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Variable, Wirewound, \        |       9.10      |
    |                | Precision (RR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Variable, Wirewound, \        |       9.11      |
    |                | Semiprecision (RA, RK)        |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Variable, Wirewound, Power \  |       9.12      |
    |                | (RP)                          |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Variable, Non-Wirewound \     |       9.13      |
    |                | (RJ, RJR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Variable, Composition (RV)    |       9.14      |
    +----------------+-------------------------------+-----------------+
    |       15       | Variable,Non-Wirewound, \     |       9.15      |
    |                | Film and Precision (RQ, RVC)  |                 |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the resistor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] in [2, 6]:
            _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
                attributes['subcategory_id']
            ][
                attributes['specification_id']
            ]
        else:
            _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
                attributes['subcategory_id']
            ]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1
        ]
    except IndexError:
        attributes['lambda_b'] = 0.0

    _msg = _do_check_variables(attributes)

    return attributes, _msg


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the resistor type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the resistor being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating resistor, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, specification ID: {2:d}, ' \
            'active environment ID: {3:d}, and quality ID: ' \
            '{4:d}.\n'.format(
                attributes['hardware_id'],
                attributes['subcategory_id'],
                attributes['specification_id'],
                attributes['environment_active_id'],
                attributes['quality_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'resistor, hardware ID: {0:d}, quality ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['quality_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piC'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piC is 0.0 when calculating ' \
                'resistor, hardware ID: {0:d}, ' \
                'construction ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['construction_id'],
                )

        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'resistor, hardware ID: {0:d}, ' \
                'active environment ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['environment_active_id'],
                )

        if attributes['piR'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piR is 0.0 when calculating ' \
                'resistor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'specification ID: {2:d}, ' \
                'family ID: {3:d}, ' \
                '# of elements: {4:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['specification_id'],
                    attributes['family_id'],
                    attributes['n_elements'],
                )

        if attributes['piT'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piT is 0.0 when calculating ' \
                'resistor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'case temperature: {2:f}, ' \
                'ambient temperature: {3:f}, ' \
                'power ratio: {4:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['temperature_case'],
                    attributes['temperature_active'],
                    attributes['power_ratio'],
                )

        if attributes['piV'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piV is 0.0 when calculating ' \
                'resistor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'voltage ratio: {2:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['voltage_ratio'],
                )
    print(_msg)
    return _msg


def calculate_217f_part_stress(**attributes):  # pylint: disable=R0912, R0914
    """
    Calculate the part stress hazard rate for a resistor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _calculate_resistance_factor(attributes)
    attributes = _calculate_voltage_factor(attributes)
    attributes = _calculate_temperature_factor(attributes)

    # Calculate the taps factor (piTAPS).
    if attributes['subcategory_id'] in [9, 10, 11, 12, 13, 14, 15]:
        attributes['piTAPS'] = (attributes['n_elements']**1.5 / 25.0) + 0.792

    # Determine the consruction class factor (piC).
    if attributes['subcategory_id'] in [10, 12]:
        attributes['piC'] = PI_C[attributes['subcategory_id']][
            attributes['construction_id'] - 1
        ]

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 4:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piT'] *
            attributes['n_elements']
        )
    elif attributes['subcategory_id'] in [9, 11, 13, 14, 15]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piTAPS'] *
            attributes['piR'] * attributes['piV']
        )
    elif attributes['subcategory_id'] in [10, 12]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piTAPS'] *
            attributes['piC'] * attributes['piR'] * attributes['piV']
        )
    elif attributes['subcategory_id'] != 8:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piR']
        )

    return attributes, _msg
