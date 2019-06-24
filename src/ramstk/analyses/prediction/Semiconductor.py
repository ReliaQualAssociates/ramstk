# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Semiconductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Reliability Calculations Module."""

# Standard Library Imports
from math import exp, log, sqrt

PART_COUNT_217F_LAMBDA_B = {
    1: {
        1: [
            0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210, 0.200,
            0.44, 0.170, 0.00180, 0.076, 0.23, 1.50,
        ],
        2: [
            0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054, 0.054,
            0.12, 0.045, 0.00047, 0.020, 0.06, 0.40,
        ],
        3: [
            0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700, 3.700,
            8.00, 3.100, 0.03200, 1.400, 4.10, 28.0,
        ],
        4: [
            0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160, 0.160,
            0.35, 0.130, 0.00140, 0.060, 0.18, 1.20,
        ],
        5: [
            0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170, 0.170,
            0.36, 0.140, 0.00150, 0.062, 0.18, 1.20,
        ],
        6: [
            0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150, 0.130,
            0.27, 0.120, 0.00160, 0.060, 0.16, 1.30,
        ],
        7: [
            0.00580, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250, 0.220,
            0.460, 0.21, 0.00280, 0.100, 0.28, 2.10,
        ],
    },
    2: {
        1: [
            0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0, 62.0, 44.0, 0.43,
            16.0, 67.0, 350.0,
        ],
        2: [
            0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50, 7.60, 7.90, 0.16,
            3.70, 12.0, 94.00,
        ],
        3: [
            0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032, 0.057,
            0.097, 0.10, 0.002, 0.048, 0.15, 1.2,
        ],
        4: [
            0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69, 0.71,
            0.014, 0.34, 1.1, 8.5,
        ],
        5: [
            0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2,
            0.023, 0.56, 1.8, 14.0,
        ],
        6: [
            0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062, 0.11,
            0.11, 0.0022, 0.052, 0.17, 1.3,
        ],
    },
    3: {
        1: [
            0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067,
            0.0060, 0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056,
        ],
        2: [
            0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23, 0.50,
            0.22, 0.0029, 0.11, 0.29, 1.1,
        ],
    },
    4: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51,
        0.0069, 0.25, 0.68, 5.3,
    ],
    5: [
        0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6, 0.66, 0.0079,
        0.31, 0.88, 6.4,
    ],
    6: [
        0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3, 2.4, 0.047,
        1.1, 3.6, 28.0,
    ],
    7: [
        0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52, 0.88, 0.037, 0.33,
        0.66, 1.8, 18.0,
    ],
    8: {
        1: [
            0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2, 0.083, 2.8,
            11.0, 63.0,
        ],
        2: [
            0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0, 0.21,
            6.9, 27.0, 160.0,
        ],
    },
    9: [
        0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51,
        0.0069, 0.25, 0.68, 5.3,
    ],
    10: [
        0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14, 0.14, 0.31, 0.12,
        0.0012, 0.053, 0.16, 1.1,
    ],
    11: {
        1: [
            0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100,
            0.2100, 0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70,
        ],
        2: [
            0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500,
            0.4900, 0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70,
        ],
        3: [
            0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044,
            0.0086, 0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15,
        ],
    },
    12: [
        0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11, 0.19, 0.18,
        0.0031, 0.082, 0.28, 2.0,
    ],
    13: {
        1: [
            5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0, 230.0,
            2.6, 87.0, 350.0, 2000.0,
        ],
        2: [
            8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0, 300.0,
            400.0, 4.5, 150.0, 600.0, 3500.0,
        ],
    },
}
PI_A = {
    2: [0.5, 2.5, 1.0],
    3: [1.5, 0.7],
    4: [1.5, 0.7, 2.0, 4.0, 8.0, 10.0],
    8: [1.0, 4.0],
}

# Constants used to calculate the temperature factor (piT)
PI_T = {
    1: [3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 1925.0, 1925.0],
    2: [5260.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0],
    3: 2114.0,
    4: 1925.0,
    5: 2483.0,
    6: 2114.0,
    7: {
        1: [2903.0, 0.1, 2.0],
        2: [5794.0, 0.38, 7.55],
    },
    8: 4485.0,
    9: 1925.0,
    10: 3082.0,
    11: 2790.0,
    12: 2790.0,
    13: 4635.0,
}

# Constants used to calculate the junction temperature.
CASE_TEMPERATURE = [
    35.0, 45.0, 50.0, 45.0, 50.0, 60.0, 60.0, 75.0, 75.0, 60.0, 35.0, 50.0,
    60.0, 45.0,
]
THETA_JC = [
    70.0, 10.0, 70.0, 70.0, 70.0, 70.0, 70.0, 5.0, 70.0, 70.0, 10.0, 70.0,
    70.0, 70.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 70.0, 70.0, 5.0, 22.0,
    70.0, 5.0, 70.0, 5.0, 5.0, 1.0, 10.0, 70.0, 70.0, 5.0, 5.0, 5.0, 10.0, 5.0,
    5.0, 10.0, 5.0, 10.0, 10.0, 10.0, 5.0, 70.0, 5.0, 70.0, 70.0, 70.0, 70.0,
    70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0,
    70.0,
]

# Constants used to calculate the construction factor (piC).
PI_C = [1.0, 2.0]

# Constants used to calculate the matching factor (piM).
PI_M = [1.0, 2.0, 4.0]



def _calculate_active_hazard_rate(attributes):
    """
    Calculate the active hazard rate for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piT'] * attributes['piQ'] *
        attributes['piE']
    )
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piS'] *
            attributes['piC']
        )
    elif attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piR']
        )
    elif attributes['subcategory_id'] == 3:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piR'] * attributes['piS']
        )
    elif attributes['subcategory_id'] == 4:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA']
        )
    elif attributes['subcategory_id'] in [6, 10]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piR'] *
            attributes['piS']
        )
    elif attributes['subcategory_id'] in [7, 8]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piM']
        )
    elif attributes['subcategory_id'] == 13:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piI'] *
            attributes['piA'] * attributes['piP']
        )

    return attributes


def _calculate_application_factor(attributes):
    """
    Calculate the temperature factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    if attributes['subcategory_id'] in [2, 3, 4, 8]:
        try:
            attributes['piA'] = PI_A[attributes['subcategory_id']][
                attributes['application_id'] - 1
            ]
        except KeyError:
            attributes['piA'] = 0.0
    elif attributes['subcategory_id'] == 7:
        if attributes['application_id'] == 1:
            attributes['piA'] = 7.6
        else:
            attributes['piA'] = 0.06 * (attributes['duty_cycle'] / 100.0) + 0.4
    elif attributes['subcategory_id'] == 13:
        if attributes['application_id'] == 1:
            attributes['piA'] = 4.4
        else:
            attributes['piA'] = sqrt(attributes['duty_cycle'] / 100.0)

    return attributes


def _calculate_electrical_stress_factor(attributes):
    """
    Calculate the electrical stress factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    if attributes['subcategory_id'] == 1:
        if attributes['type_id'] > 5:
            attributes['piS'] = 1.0
        elif attributes['voltage_ratio'] <= 0.3:
            attributes['piS'] = 0.054
        else:
            attributes['piS'] = attributes['voltage_ratio']**2.43
    elif attributes['subcategory_id'] in [3, 6]:
        attributes['piS'] = 0.045 * exp(3.1 * attributes['voltage_ratio'])
    elif attributes['subcategory_id'] == 10:
        if attributes['voltage_ratio'] <= 0.3:
            attributes['piS'] = 0.1
        else:
            attributes['piS'] = attributes['voltage_ratio']**1.9

    return attributes


def _calculate_junction_temperature(attributes):
    """
    Calculate the junction temperature of the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    if attributes['temperature_case'] <= 0.0:
        attributes['temperature_case'] = CASE_TEMPERATURE[
            attributes['environment_active_id'] - 1
        ]
    if attributes['theta_jc'] <= 0.0:
        attributes['theta_jc'] = THETA_JC[attributes['package_id'] - 1]
    attributes['temperature_junction'] = (
        attributes['temperature_case']
        + attributes['theta_jc'] * attributes['power_operating']
    )

    return attributes


def _calculate_mil_hdbk_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the MIL-HDBK-217F base hazard rate for the semiconductor device.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
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

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the semiconductor being
        calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] in [1, 2, 3, 8, 11, 13]:
            _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
                attributes['subcategory_id']
            ][
                attributes['type_id']
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

    return attributes


def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Retrieve the MIL-HDBK-217F base hazard rate for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _dic_lambdab = {
        1: [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034, 0.002],
        2: [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025, 0.0025],
        3:
        0.00074,
        4: [0.012, 0.0045],
        5:
        0.0083,
        6:
        0.18,
        9: [0.06, 0.023],
        10:
        0.0022,
        11: [
            0.0055, 0.004, 0.0025, 0.013, 0.013, 0.0064, 0.0033, 0.017, 0.017,
            0.0086, 0.0013, 0.00023,
        ],
        13: [3.23, 5.65],
    }

    try:
        if attributes['subcategory_id'] in [3, 5, 6, 10]:
            attributes['lambda_b'] = _dic_lambdab[attributes['subcategory_id']]
        elif attributes['subcategory_id'] == 7:
            attributes['lambda_b'] = 0.032 * exp(
                0.354 * attributes['frequency_operating'] +
                0.00558 * attributes['power_operating'],
            )
        elif attributes['subcategory_id'] == 8:
            if (
                    attributes['frequency_operating'] >= 1.0
                    and attributes['frequency_operating'] <= 10.0
                    and attributes['power_operating'] < 0.1
            ):
                attributes['lambda_b'] = 0.052
            else:
                attributes['lambda_b'] = 0.0093 * exp(
                    0.429 * attributes['frequency_operating'] +
                    0.486 * attributes['power_operating'],
                )
        elif attributes['subcategory_id'] == 12:
            if attributes['application_id'] in [1, 3]:
                attributes[
                    'lambda_b'
                ] = 0.00043 * attributes['n_elements'] + 0.000043
            else:
                attributes['lambda_b'] = 0.00043 * attributes['n_elements']
        else:
            attributes['lambda_b'] = _dic_lambdab[
                attributes[
                    'subcategory_id'
                ]
            ][attributes['type_id'] - 1]
    except KeyError:
        attributes['lambda_b'] = 0.0

    return attributes


def _calculate_power_rating_factor(attributes):
    """
    Calculate the power rating factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    if attributes['subcategory_id'] == 2:
        if attributes['type_id'] == 4:
            try:
                attributes[
                    'piR'
                ] = 0.326 * log(attributes['power_rated']) - 0.25
            except ValueError:
                attributes['piR'] = 0.0
        else:
            attributes['piR'] = 1.0
    elif attributes['subcategory_id'] in [3, 6]:
        if attributes['power_rated'] < 0.1:
            attributes['piR'] = 0.43
        else:
            try:
                attributes['piR'] = attributes['power_rated']**0.37
            except ValueError:
                attributes['piR'] = 0.0
    elif attributes['subcategory_id'] == 10:
        attributes['piR'] = attributes['current_rated']**0.4

    return attributes


def _calculate_temperature_factor(attributes):
    """
    Calculate the temperature factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] in [1, 2]:
            _factors = PI_T[attributes['subcategory_id']][
                attributes['type_id'] - 1
            ]
        elif attributes['subcategory_id'] == 7:
            _factors = PI_T[attributes['subcategory_id']][
                attributes[
                    'type_id'
                ]
            ]
        else:
            _factors = PI_T[attributes['subcategory_id']]

        if attributes['subcategory_id'] == 7:
            _f0 = _factors[0]
            _f1 = _factors[1]
            _f2 = _factors[2]
            if attributes['voltage_ratio'] <= 0.4:
                attributes['piT'] = _f1 * exp(
                    -_f0 * (
                        1.0 / (attributes['temperature_junction'] + 273.0)
                        - 1.0 / 298.0
                    ),
                )
            else:
                attributes[
                    'piT'
                ] = _f2 * (attributes['voltage_ratio'] - 0.35) * exp(
                    -_f0 * (
                        1.0 / (attributes['temperature_junction'] + 273.0)
                        - 1.0 / 298.0
                    ),
                )
        else:
            attributes['piT'] = exp(
                -_factors * (
                    1.0 / (attributes['temperature_junction'] + 273.0)
                    - 1.0 / 298.0
                ),
            )
    except (KeyError, IndexError):
        attributes['piT'] = 0.0

    return attributes


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the semiconductor type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the semiconductor being
        calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
               'calculating semiconductor, hardware ID: {0:d} and active ' \
               'environment ID: {1:d}.\n'.format(
                   attributes['hardware_id'],
                   attributes['environment_active_id'],
               )

    if attributes['piQ'] <= 0.0:
        _msg = 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
               'semiconductor, hardware ID: {0:d} and quality ID: ' \
               '{1:d}.\n'.format(
                   attributes['hardware_id'],
                   attributes['quality_id'],
               )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piA'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piA is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'application ID: {2:d}, and ' \
                'duty cycle: {3:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['application_id'],
                    attributes['duty_cycle'],
                )

        if attributes['piC'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piC is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d} and construction  ' \
                'ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['construction_id'],
                )

        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d} and active environment ' \
                'ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['environment_active_id'],
                )

        if attributes['piI'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piI is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d} and operating current: ' \
                '{1:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['current_operating'],
                )

        if attributes['piM'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piM is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d} and network matching ' \
                'ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['matching_id'],
                )

        if attributes['piP'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piP is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d} and power ratio: ' \
                '{1:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['power_ratio'],
                )

        if attributes['piR'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piR is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'type ID: {2:d}, ' \
                'rated current: {3:f}, and ' \
                'rated power: {4:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['type_id'],
                    attributes['current_rated'],
                    attributes['power_rated'],
                )

        if attributes['piS'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piS is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'type ID: {2:d}, and ' \
                'voltage ratio: {3:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['type_id'],
                    attributes['voltage_ratio'],
                )

        if attributes['piT'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piT is 0.0 when calculating ' \
                'semiconductor, hardware ID: {0:d}, ' \
                'subcategory ID: {1:d}, ' \
                'type ID: {2:d}, ' \
                'junction temperature: {3:f}, and ' \
                'voltage ratio: {4:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['subcategory_id'],
                    attributes['type_id'],
                    attributes['temperature_junction'],
                    attributes['voltage_ratio'],
                )
    print(_msg)
    return _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a semiconductor.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_count_lambda_b(attributes)
    attributes = _get_part_count_quality_factor(attributes)

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):  # pylint: disable=R0912
    """
    Calculate the part stress hazard rate for a semiconductor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _calculate_junction_temperature(attributes)
    attributes = _get_part_stress_quality_factor(attributes)
    attributes = _calculate_temperature_factor(attributes)
    attributes = _calculate_application_factor(attributes)
    attributes = _calculate_power_rating_factor(attributes)
    attributes = _calculate_electrical_stress_factor(attributes)

    # Calculate the matching network factor (piM).
    if attributes['subcategory_id'] in [7, 8]:
        attributes['piM'] = PI_M[attributes['matching_id'] - 1]

    # Retrieve the construction factor (piC).
    if attributes['subcategory_id'] == 1:
        attributes['piC'] = PI_C[attributes['construction_id'] - 1]

    # Calculate forward current factor (piI).
    if attributes['subcategory_id'] == 13:
        attributes['piI'] = attributes['current_operating']**0.68

    # Calculate the power degradation factor (piP).
    if attributes['subcategory_id'] == 13:
        attributes['piP'] = 1.0 / (2.0 * (1.0 - attributes['power_ratio']))

    _msg = _do_check_variables(attributes)

    attributes = _calculate_active_hazard_rate(attributes)

    return attributes, _msg


def _get_part_count_quality_factor(attributes):
    """
    Select the MIL-HDBK-217F quality factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    # Dictionary containing piQ values for parts count method.  The key is the
    # subcategory_id.  The quality_id attribute is used to select the proper
    # value of piQ from the returned list.
    _dic_piQ = {
        1: [0.7, 1.0, 2.4, 5.5, 8.0],
        2: [[0.5, 1.0, 5.0, 25, 50], [0.5, 1.0, 1.8, 2.5]],
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
        13: [1.0, 1.0, 3.3],
    }

    try:
        if attributes['subcategory_id'] == 2:
            if attributes['type_id'] == 5:
                attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][1][
                    attributes['quality_id'] - 1
                ]
            else:
                attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][0][
                    attributes['quality_id'] - 1
                ]
        else:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    return attributes


def _get_part_stress_quality_factor(attributes):
    """
    Select the MIL-HDBK-217F quality factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _dic_piQ = {
        1: [0.7, 1.0, 2.4, 5.5, 8.0],
        2: {
            1: [0.5, 1.0, 5.0, 25.0, 50.0],
            2: [0.5, 1.0, 5.0, 25.0, 50.0],
            3: [0.5, 1.0, 5.0, 25.0, 50.0],
            4: [0.5, 1.0, 5.0, 25.0, 50.0],
            5: [0.5, 1.0, 1.8, 2.5],
            6: [0.5, 1.0, 5.0, 25.0, 50.0],
        },
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
        13: [1.0, 1.0, 3.3],
    }

    try:
        if attributes['subcategory_id'] == 2:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['type_id']
            ][attributes['quality_id'] - 1]
        else:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    return attributes
