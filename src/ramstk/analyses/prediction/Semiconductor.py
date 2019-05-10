#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Semiconductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Reliability Calculations Module."""

import gettext

from math import exp, log, sqrt

_ = gettext.gettext

# Constants used to calculate the application factor (piA)
_dic_piA = {
    2: [0.5, 2.5, 1.0],
    3: [1.5, 0.7],
    4: [1.5, 0.7, 2.0, 4.0, 8.0, 10.0],
    8: [1.0, 4.0]
}

# Constants used to calculate the temperature factor (piT)
_dic_piT = {
    1: [3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 3091.0, 1925.0, 1925.0],
    2: [5260.0, 2100.0, 2100.0, 2100.0, 2100.0, 2100.0],
    3: 2114.0,
    4: 1925.0,
    5: 2483.0,
    6: 2114.0,
    7: {
        1: [2903.0, 0.1, 2.0],
        2: [5794.0, 0.38, 7.55]
    },
    8: 4485.0,
    9: 1925.0,
    10: 3082.0,
    11: 2790.0,
    12: 2790.0,
    13: 4635.0
}

# Constants used to calculate the junction temperature.
_lst_temp_case = [
    35.0, 45.0, 50.0, 45.0, 50.0, 60.0, 60.0, 75.0, 75.0, 60.0, 35.0, 50.0,
    60.0, 45.0
]
_lst_theta_jc = [
    70.0, 10.0, 70.0, 70.0, 70.0, 70.0, 70.0, 5.0, 70.0, 70.0, 10.0, 70.0,
    70.0, 70.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 70.0, 70.0, 5.0, 22.0,
    70.0, 5.0, 70.0, 5.0, 5.0, 1.0, 10.0, 70.0, 70.0, 5.0, 5.0, 5.0, 10.0, 5.0,
    5.0, 10.0, 5.0, 10.0, 10.0, 10.0, 5.0, 70.0, 5.0, 70.0, 70.0, 70.0, 70.0,
    70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0,
    70.0
]

# Constants used to calculate the construction factor (piC).
_lst_piC = [1.0, 2.0]

# Constants used to calculate the matching factor (piM).
_lst_piM = [1.0, 2.0, 4.0]


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a semiconductor.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Select the base hazard rate.
    attributes = _select_base_part_count_hazard_rate(attributes)
    if attributes['lambda_b'] <= 0.0:
        _msg = 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
               'calculating semiconductor, hardware ID: {0:d} and active ' \
               'environment ID: {1:d}.\n'.format(
                attributes['hardware_id'], attributes['environment_active_id'])

    # Select the piQ.
    attributes = _select_part_count_quality_factor(attributes)
    if attributes['piQ'] <= 0.0:
        _msg = 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
               'semiconductor, hardware ID: {0:d} and quality ID: ' \
               '{1:d}.'.format(attributes['hardware_id'],
                               attributes['quality_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'])

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
    _msg = ''

    # Calculate the base hazard rate.
    attributes = _calculate_base_part_stress_hazard_rate(attributes)
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating semiconductor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Calculate junction temperature.
    attributes = _calculate_junction_temperature(attributes)

    # Calculate the temperature factor (piT).
    attributes = _calculate_temperature_factor(attributes)

    # Calculate the application factor (piA).
    attributes = _calculate_application_factor(attributes)

    # Calculate the power rating factor (piR).
    attributes = _calculate_power_rating_factor(attributes)

    # Calculate the electrical stress factor (piS).
    attributes = _calculate_electrical_stress_factor(attributes)

    # Calculate the matching network factor (piM).
    if attributes['subcategory_id'] in [7, 8]:
        attributes['piM'] = _lst_piM[attributes['matching_id'] - 1]

    # Retrieve the construction factor (piC).
    if attributes['subcategory_id'] == 1:
        attributes['piC'] = _lst_piC[attributes['construction_id'] - 1]

    # Calculate forward current factor (piI).
    if attributes['subcategory_id'] == 13:
        attributes['piI'] = attributes['current_operating']**0.68

    # Calculate the power degradation factor (piP).
    if attributes['subcategory_id'] == 13:
        attributes['piP'] = 1.0 / (2.0 * (1.0 - attributes['power_ratio']))

    # Retrieve the quality factor (piQ).
    attributes = _select_part_stress_quality_factor(attributes)
    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'semiconductor, hardware ID: {0:d} and quality ID: ' \
            '{1:d}.\n'.format(attributes['hardware_id'],
                            attributes['quality_id'])

    # Retrieve the environmental factor (piE).
    attributes = _select_environmental_factor(attributes)
    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'semiconductor, hardware ID: {0:d} and active environment ID: ' \
            '{1:d}.\n'.format(attributes['hardware_id'],
                           attributes['environment_active_id'])

    # Calculate the active hazard rate.
    attributes = _calculate_active_hazard_rate(attributes)

    return attributes, _msg


def overstressed(**attributes):
    """
    Determine whether the semiconductor is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _reason_num = 1
    _reason = ''

    _harsh = True

    attributes['overstress'] = False

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if attributes['environment_active_id'] in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if attributes['power_ratio'] > 0.70:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(". Operating power > 70% rated power in harsh "
                  "environment.\n")
            _reason_num += 1
        if attributes['temperature_junction'] > 125.0:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(". Junction temperature > 125.0C in harsh environment.\n")
            _reason_num += 1
    else:
        if attributes['power_ratio'] > 0.90:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(". Operating power > 90% rated power in mild "
                  "environment.\n")
            _reason_num += 1

    attributes['reason'] = _reason

    return attributes


def _calculate_active_hazard_rate(attributes):
    """
    Calculate the active hazard rate for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piT'] * attributes['piQ'] *
        attributes['piE'])
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piS'] *
            attributes['piC'])
    elif attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piR'])
    elif attributes['subcategory_id'] == 3:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piR'] * attributes['piS'])
    elif attributes['subcategory_id'] == 4:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'])
    elif attributes['subcategory_id'] in [6, 10]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piR'] *
            attributes['piS'])
    elif attributes['subcategory_id'] in [7, 8]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piM'])
    elif attributes['subcategory_id'] == 13:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piI'] *
            attributes['piA'] * attributes['piP'])

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
            attributes['piA'] = _dic_piA[attributes['subcategory_id']][
                attributes['application_id'] - 1]
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


def _calculate_base_part_stress_hazard_rate(attributes):
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
            0.0086, 0.0013, 0.00023
        ],
        13: [3.23, 5.65]
    }

    try:
        if attributes['subcategory_id'] in [3, 5, 6, 10]:
            attributes['lambda_b'] = _dic_lambdab[attributes['subcategory_id']]
        elif attributes['subcategory_id'] == 7:
            attributes['lambda_b'] = 0.032 * exp(
                0.354 * attributes['frequency_operating'] +
                0.00558 * attributes['power_operating'])
        elif attributes['subcategory_id'] == 8:
            if (attributes['frequency_operating'] >= 1.0
                    and attributes['frequency_operating'] <= 10.0
                    and attributes['power_operating'] < 0.1):
                attributes['lambda_b'] = 0.052
            else:
                attributes['lambda_b'] = 0.0093 * exp(
                    0.429 * attributes['frequency_operating'] +
                    0.486 * attributes['power_operating'])
        elif attributes['subcategory_id'] == 12:
            if attributes['application_id'] in [1, 3]:
                attributes[
                    'lambda_b'] = 0.00043 * attributes['n_elements'] + 0.000043
            else:
                attributes['lambda_b'] = 0.00043 * attributes['n_elements']
        else:
            attributes['lambda_b'] = _dic_lambdab[attributes[
                'subcategory_id']][attributes['type_id'] - 1]
    except KeyError:
        attributes['lambda_b'] = 0.0

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
        attributes['temperature_case'] = _lst_temp_case[
            attributes['environment_active_id'] - 1]
    if attributes['theta_jc'] <= 0.0:
        attributes['theta_jc'] = _lst_theta_jc[attributes['package_id'] - 1]
    attributes['temperature_junction'] = (
        attributes['temperature_case'] +
        attributes['theta_jc'] * attributes['power_operating'])

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
                    'piR'] = 0.326 * log(attributes['power_rated']) - 0.25
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
            _factors = _dic_piT[attributes['subcategory_id']][
                attributes['type_id'] - 1]
        elif attributes['subcategory_id'] == 7:
            _factors = _dic_piT[attributes['subcategory_id']][attributes[
                'type_id']]
        else:
            _factors = _dic_piT[attributes['subcategory_id']]

        if attributes['subcategory_id'] == 7:
            _f0 = _factors[0]
            _f1 = _factors[1]
            _f2 = _factors[2]
            if attributes['voltage_ratio'] <= 0.4:
                attributes['piT'] = _f1 * exp(
                    -_f0 * (1.0 / (attributes['temperature_junction'] + 273.0)
                            - 1.0 / 298.0))
            else:
                attributes[
                    'piT'] = _f2 * (attributes['voltage_ratio'] - 0.35) * exp(
                        -_f0 * (1.0 /
                                (attributes['temperature_junction'] + 273.0) -
                                1.0 / 298.0))
        else:
            attributes['piT'] = exp(
                -_factors * (1.0 / (attributes['temperature_junction'] + 273.0)
                             - 1.0 / 298.0))
    except (KeyError, IndexError):
        attributes['piT'] = 0.0

    return attributes


def _select_base_part_count_hazard_rate(attributes):
    """
    Select the MIL-HDBK-217F base hazard rate for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id, second key is the type id.  Current
    # subcategory IDs are:
    #
    #    1. Diode, Low Frequency
    #    2. Diode, High Frequency
    #    3. Transistor, Low Frequency, Bipolar
    #    4. Transistor, Low Frequency, Si FET
    #    5. Transistor, Unijunction
    #    6. Transistor, High Frequency, Low Noise,Bipolar
    #    7. Transistor, High Frequency, High Power, Bipolar
    #    8. Transistor, High Frequency, GaAs FET
    #    9. Transistor, High Frequency, Si FET
    #   10. Thyristor/SCR
    #   11. Optoelectronic, Detector, Isolator, Emitter
    #   12. Optoelectronic, Alphanumeric Display
    #   13. Optoelectronic, Laser Diode
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
        1: {
            1: [
                0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210, 0.200,
                0.44, 0.170, 0.00180, 0.076, 0.23, 1.50
            ],
            2: [
                0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054, 0.054,
                0.12, 0.045, 0.00047, 0.020, 0.06, 0.40
            ],
            3: [
                0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700, 3.700,
                8.00, 3.100, 0.03200, 1.400, 4.10, 28.0
            ],
            4: [
                0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160, 0.160,
                0.35, 0.130, 0.00140, 0.060, 0.18, 1.20
            ],
            5: [
                0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170, 0.170,
                0.36, 0.140, 0.00150, 0.062, 0.18, 1.20
            ],
            6: [
                0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150, 0.130,
                0.27, 0.120, 0.00160, 0.060, 0.16, 1.30
            ],
            7: [
                0.00580, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250, 0.220,
                0.460, 0.21, 0.00280, 0.100, 0.28, 2.10
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
                0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032, 0.057,
                0.097, 0.10, 0.002, 0.048, 0.15, 1.2
            ],
            4: [
                0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69, 0.71,
                0.014, 0.34, 1.1, 8.5
            ],
            5: [
                0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2,
                0.023, 0.56, 1.8, 14.0
            ],
            6: [
                0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062, 0.11,
                0.11, 0.0022, 0.052, 0.17, 1.3
            ]
        },
        3: {
            1: [
                0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067,
                0.0060, 0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056
            ],
            2: [
                0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23, 0.50,
                0.22, 0.0029, 0.11, 0.29, 1.1
            ]
        },
        4: [
            0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51,
            0.0069, 0.25, 0.68, 5.3
        ],
        5: [
            0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6, 0.66, 0.0079,
            0.31, 0.88, 6.4
        ],
        6: [
            0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3, 2.4, 0.047,
            1.1, 3.6, 28.0
        ],
        7: [
            0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52, 0.88, 0.037, 0.33,
            0.66, 1.8, 18.0
        ],
        8: {
            1: [
                0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2, 0.083, 2.8,
                11.0, 63.0
            ],
            2: [
                0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0, 0.21,
                6.9, 27.0, 160.0
            ]
        },
        9: [
            0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51,
            0.0069, 0.25, 0.68, 5.3
        ],
        10: [
            0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14, 0.14, 0.31, 0.12,
            0.0012, 0.053, 0.16, 1.1
        ],
        11: {
            1: [
                0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100,
                0.2100, 0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70
            ],
            2: [
                0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500,
                0.4900, 0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70
            ],
            3: [
                0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044,
                0.0086, 0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15
            ]
        },
        12: [
            0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11, 0.19, 0.18,
            0.0031, 0.082, 0.28, 2.0
        ],
        13: {
            1: [
                5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0, 100.0, 170.0, 230.0,
                2.6, 87.0, 350.0, 2000.0
            ],
            2: [
                8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0, 180.0, 300.0,
                400.0, 4.5, 150.0, 600.0, 3500.0
            ]
        }
    }

    try:
        if attributes['subcategory_id'] in [1, 2, 3, 8, 11, 13]:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
                attributes['type_id']]
        else:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    return attributes


def _select_environmental_factor(attributes):
    """
    Select the MIL-HDBK-217F environmental factor for the semiconductor device.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _dic_piE = {
        1: [
            1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
            32.0, 320.0
        ],
        2: [
            1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
            24.0, 250.0
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
            1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
            24.0, 250.0
        ],
        7: [
            1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
            24.0, 250.0
        ],
        8: [
            1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 7.5,
            24.0, 250.0
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

    try:
        attributes['piE'] = _dic_piE[attributes['subcategory_id']][
            attributes['environment_active_id'] - 1]
    except (KeyError, IndexError):
        attributes['piE'] = 0.0

    return attributes


def _select_part_count_quality_factor(attributes):
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
                    attributes['quality_id'] - 1]
            else:
                attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][0][
                    attributes['quality_id'] - 1]
        else:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['quality_id'] - 1]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    return attributes


def _select_part_stress_quality_factor(attributes):
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
            6: [0.5, 1.0, 5.0, 25.0, 50.0]
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
        13: [1.0, 1.0, 3.3]
    }

    try:
        if attributes['subcategory_id'] == 2:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['type_id']][attributes['quality_id'] - 1]
        else:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['quality_id'] - 1]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    return attributes
