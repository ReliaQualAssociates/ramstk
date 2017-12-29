#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.mil_hdbk_217f.Capacitor.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Capacitor Calculations Module."""

import gettext

from math import exp

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a capacitor.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    if attributes['hazard_rate_method_id'] == 1:
        attributes, _msg = calculate_217f_part_count(**attributes)
    elif attributes['hazard_rate_method_id'] == 2:
        attributes, _msg = calculate_217f_part_stress(**attributes)

    if attributes['mult_adj_factor'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Multiplicative adjustment factor is 0.0 ' \
            'when calculating capacitor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RTK WARNING: dty cycle is 0.0 when calculating ' \
            'capacitor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RTK WARNING: Quantity is less than 1 when ' \
            'calculating capacitor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    attributes, _msg = calculate_dormant_hazard_rate(**attributes)
    attributes = overstressed(**attributes)

    return attributes, _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a capacitor.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id, second key is the specification id.  If
    # the capacitor subcategory is NOT specification dependent, then the second
    # key will be zero.  Current subcategory IDs are:
    #
    #    1. Fixed, Paper, Bypass (CA, CP)
    #    2. Fixed, Feed-Through (CZ, CZR)
    #    3. Fixed, Paper and Plastic Film (CPV, CQ, CQR)
    #    4. Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)
    #    5. Fixed, Plastic and Metallized Plastic
    #    6. Fixed, Super-Metallized Plastic (CRH)
    #    7. Fixed, Mica (CM, CMR)
    #    8. Fixed, Mica, Button (CB)
    #    9. Fixed, Glass (CY, CYR)
    #   10. Fixed, Ceramic, General Purpose (CK, CKR)
    #   11. Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)
    #   12. Fixed, Electrolytic, Tantalum, Solid (CSR)
    #   13. Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)
    #   14. Fixed, Electrolytic, Aluminum (CU, CUR)
    #   15. Fixed, Electrolytic (Dry), Aluminum (CE)
    #   16. Variable, Ceramic (CV)
    #   17. Variable, Piston Type (PC)
    #   18. Variable, Air Trimmer (CT)
    #   19. Variable and Fixed, Gas or Vacuum (CG)
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
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
            0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030, 0.040, 0.094, 0.15,
            0.11, 0.0024, 0.058, 0.18, 2.7
        ],
        3: [
            0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068, 0.013, 0.026, 0.048,
            0.044, 0.0010, 0.023, 0.063, 1.1
        ],
        4: [
            0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012, 0.018, 0.037, 0.066,
            0.060, 0.0014, 0.032, 0.088, 1.5
        ],
        5: [
            0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026, 0.048, 0.086, 0.14,
            0.10, 0.0020, 0.054, 0.15, 2.5
        ],
        6: [
            0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096, 0.014, 0.034, 0.053,
            0.048, 0.0011, 0.026, 0.07, 1.2
        ],
        7: [
            0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095, 0.054,
            0.069, 0.031, 0.00025, 0.012, 0.046, 0.45
        ],
        8: [
            0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60, 0.48,
            0.0091, 0.25, 0.68, 11.0
        ],
        9: [
            0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062, 0.035,
            0.045, 0.020, 0.00016, 0.0076, 0.030, 0.29
        ],
        10: [
            0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015, 0.015, 0.032, 0.048,
            0.077, 0.0014, 0.049, 0.13, 2.3
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
            0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6, 1.2, .012,
            0.49, 1.7, 21.0
        ],
        15: [
            0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4, 2.0, 0.015,
            0.68, 2.8, 28.0
        ],
        16: [
            0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9,
            5.9, 85.0
        ],
        17: [
            0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16,
            0.93, 3.2, 37.0
        ],
        18: [
            0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5,
            8.9, 100.0
        ],
        19: [
            0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0,
            0.0, 0.0
        ]
    }

    # List containing piQ values for parts count method.  The list positions
    # corrspond to the following quality levels:
    #
    #   0. Established reliability level S
    #   1. Established reliability level R
    #   2. Established reliability level P
    #   3. Established reliability level M
    #   4. Established reliability level L
    #   5. Non-established reliability MIL-SPEC
    #   6. Non-established reliability lower
    #
    # The quality_id attribute is used to select the proper value of piQ.
    _lst_piQ = [0.030, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0]

    # Select the base hazard rate.
    try:
        if attributes['subcategory_id'] == 1:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
                attributes['specification_id']]
        else:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']]
    except KeyError:
        _lst_base_hr = [0.0]
    try:
        _lambdab = _lst_base_hr[attributes['environment_active_id'] - 1]
    except IndexError:
        _lambdab = 0.0
    attributes['lambda_b'] = _lambdab

    # Select the piQ.
    _piQ = _lst_piQ[attributes['quality_id'] - 1]
    attributes['piQ'] = _piQ

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if _lambdab <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating capacitor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if _piQ <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'capacitor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the hazard rate.
    _hr_active = _lambdab * _piQ
    attributes['hazard_rate_active'] = _hr_active

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a capacitor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_ref_temp = {
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
    _dic_factors = {
        1: [0.00086, 0.4, 5.0, 2.5, 1.8, 1.2, 0.095],
        2: [0.00115, 0.4, 5.0, 2.5, 1.8, 1.4, 0.12],
        3: [0.0005, 0.4, 5.0, 2.5, 1.8, 1.6, 0.13],
        4: [0.00069, 0.4, 5.0, 2.5, 1.8, 1.2, 0.092],
        5: [0.00099, 0.4, 5.0, 2.5, 1.8, 1.1, 0.085],
        6: [0.00055, 0.4, 5.0, 2.5, 1.8, 1.2, 0.092],
        7: [8.6E-10, 0.4, 3.0, 16.0, 1.0, 0.45, 0.14],
        8: [0.0053, 0.4, 3.0, 1.2, 6.3, 0.31, 0.23],
        9: [8.25E-10, 0.5, 4.0, 16.0, 1.0, 0.62, 0.14],
        10: [0.0003, 0.3, 3.0, 1.0, 1.0, 0.41, 0.11],
        11: [2.6E-9, 0.3, 3.0, 14.3, 1.0, 0.59, 0.12],
        12: [0.00375, 0.4, 3.0, 2.6, 9.0, 1.0, 0.12],
        13: [0.00165, 0.4, 3.0, 2.6, 9.0, 0.82, 0.066],
        14: [0.00254, 0.5, 3.0, 5.09, 5.0, 0.34, 0.18],
        15: [0.0028, 0.55, 3.0, 4.09, 5.9, 0.321, 0.19],
        16: [0.00224, 0.17, 3.0, 1.59, 10.1, 1.0, 0.0],
        17: [7.3E-7, 0.33, 3.0, 12.1, 1.0, 1.0, 0.0],
        18: [1.92E-6, 0.33, 3.0, 10.8, 1.0, 1.0, 0.0],
        19: [0.0112, 0.17, 3.0, 1.59, 10.1, 1.0, 0.0]
    }
    _dic_piQ = {
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
    _dic_piE = {
        1: [
            1.0, 2.0, 9.0, 5.0, 15.0, 6.0, 8.0, 17.0, 32.0, 22.0, 0.5, 12.0,
            32.0, 570.0
        ],
        2: [
            1.0, 2.0, 9.0, 7.0, 15.0, 6.0, 8.0, 17.0, 28.0, 22.0, 0.5, 12.0,
            32.0, 570.0
        ],
        3: [
            1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 6.0, 11.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0
        ],
        4: [
            1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 6.0, 11.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0
        ],
        5: [
            1.0, 2.0, 10.0, 5.0, 16.0, 6.0, 11.0, 18.0, 30.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ],
        6: [
            1.0, 4.0, 8.0, 5.0, 14.0, 4.0, 6.0, 13.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0
        ],
        7: [
            1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ],
        8: [
            1.0, 2.0, 10.0, 5.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ],
        9: [
            1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ],
        10: [
            1.0, 2.0, 9.0, 5.0, 15.0, 4.0, 4.0, 8.0, 12.0, 20.0, 0.4, 13.0,
            34.0, 610.0
        ],
        11: [
            1.0, 2.0, 10.0, 5.0, 17.0, 4.0, 8.0, 16.0, 35.0, 24.0, 0.5, 13.0,
            34.0, 610.0
        ],
        12: [
            1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0, 12.0, 20.0, 24.0, 0.4, 11.0,
            29.0, 530.0
        ],
        13: [
            1.0, 2.0, 10.0, 6.0, 16.0, 4.0, 8.0, 14.0, 30.0, 23.0, 0.5, 13.0,
            34.0, 610.0
        ],
        14: [
            1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0, 27.0, 0.5, 14.0,
            38.0, 690.0
        ],
        15: [
            1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0, 27.0, 0.5, 18.0,
            38.0, 690.0
        ],
        16: [
            1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.4, 20.0,
            52.0, 950.0
        ],
        17: [
            1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0, 0.5, 18.0,
            46.0, 830.0
        ],
        18: [
            1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.5, 20.0,
            52.0, 950.0
        ],
        19: [
            1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0, 0.5,
            None, None, None
        ]
    }
    _dic_piSR = {
        0.1: 0.33,
        0.2: 0.27,
        0.4: 0.2,
        0.6: 0.13,
        0.8: 0.1,
        1.0: 0.066
    }
    _dic_piC = {1: 0.3, 2: 1.0, 3: 2.0, 4: 2.5, 5: 3.0}
    _dic_piCF = {1: 0.1, 2: 1.0}

    _msg = ''

    # Calculate the voltage stress.
    try:
        _stress = (
            attributes['voltage_dc_operating'] +
            attributes['voltage_ac_operating']) / attributes['voltage_rated']
    except ZeroDivisionError:
        _stress = 1.0
    attributes['voltage_ratio'] = _stress

    # Calculate the base hazard rate.
    _ref_temp = _dic_ref_temp[attributes['temperature_rated_max']]
    _f0 = _dic_factors[attributes['subcategory_id']][0]
    _f1 = _dic_factors[attributes['subcategory_id']][1]
    _f2 = _dic_factors[attributes['subcategory_id']][2]
    _f3 = _dic_factors[attributes['subcategory_id']][3]
    _f4 = _dic_factors[attributes['subcategory_id']][4]
    attributes['lambda_b'] = _f0 * ((_stress / _f1)**_f2 + 1.0) * exp(
        _f3 * ((attributes['temperature_active'] + 273.0) / _ref_temp)**_f4)

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating capacitor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Calculate the capacitance factor (piCV).
    _f0 = _dic_factors[attributes['subcategory_id']][5]
    _f1 = _dic_factors[attributes['subcategory_id']][6]
    attributes['piCV'] = _f0 * attributes['capacitance']**_f1

    # Determine the quality factor (piQ).
    attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
        attributes['quality_id'] - 1]

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'capacitor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the environmental factor (piE).
    attributes['piE'] = _dic_piE[attributes['subcategory_id']][
        attributes['environment_active_id'] - 1]

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'capacitor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the series resistance factor (piSR).
    if attributes['subcategory_id'] == 12:
        _cr = attributes['resistance'] / (attributes['voltage_dc_operating'] +
                                          attributes['voltage_ac_operating'])
        attributes['piSR'] = _dic_piSR[_cr]
        attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
            'piCV'] * attributes['piQ'] * attributes['piE'] * attributes[
                'piSR']
    elif attributes['subcategory_id'] == 13:
        attributes['piC'] = _dic_piC[attributes['construction_id']]
        attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
            'piCV'] * attributes['piQ'] * attributes['piE'] * attributes['piC']
    elif attributes['subcategory_id'] in [16, 17, 18]:
        attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
            'piQ'] * attributes['piE']
    elif attributes['subcategory_id'] == 19:
        attributes['piCF'] = _dic_piCF[attributes['configuration_id']]
        attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
            'piCF'] * attributes['piQ'] * attributes['piE']
    else:
        attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
            'piCV'] * attributes['piQ'] * attributes['piE']

    return attributes, _msg


def calculate_dormant_hazard_rate(**attributes):
    """
    Calculate the dormant hazard rate for a capacitor.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below for capacitors).

    +-------+--------+--------+-------+-------+-------+-------+
    |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
    |Active |Active  |Active  |Active |Active |Active |Active |
    |to     |to      |to      |to     |to     |to     |to     |
    |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
    |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    +=======+========+========+=======+=======+=======+=======+
    | 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
    +-------+--------+--------+-------+-------+-------+-------+

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_hr_dormant = {
        1: {
            2: 0.1
        },
        2: {
            2: 0.1
        },
        3: {
            2: 0.1
        },
        4: {
            2: 0.04,
            3: 0.1
        },
        5: {
            2: 0.04,
            3: 0.1
        },
        6: {
            1: 0.1,
            2: 0.03
        },
        7: {
            1: 0.1,
            2: 0.03
        },
        8: {
            1: 0.1,
            2: 0.03
        },
        9: {
            1: 0.1,
            2: 0.03
        },
        10: {
            1: 0.1,
            2: 0.03
        },
        11: {
            2: 0.4,
            4: 0.2
        }
    }
    _msg = ''

    try:
        attributes['hazard_rate_dormant'] = \
            (_dic_hr_dormant[attributes['environment_active_id']]
             [attributes['environment_dormant_id']] *
             attributes['hazard_rate_active'])
    except KeyError:
        attributes['hazard_rate_dormant'] = 0.0
        _msg = 'RTK ERROR: Unknown active and/or dormant environment ID. ' \
               'Active ID: {0:d}, Dormant ID: ' \
               '{1:d}'.format(attributes['environment_active_id'],
                              attributes['environment_dormant_id'])

    return attributes, _msg


def overstressed(**attributes):
    """
    Determine whether the capacitor is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _reason_num = 1
    _reason = ''

    _harsh = True

    attributes['overstress'] = False
    _voltage_operating = attributes['voltage_ac_operating'] + attributes['voltage_dc_operating']

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if attributes['environment_active_id'] in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if (_voltage_operating > 0.60 * attributes['voltage_rated']):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 60% rated voltage.\n")
            _reason_num += 1
        if (attributes['temperature_rated_max'] -
                attributes['temperature_active'] <= 10.0):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating temperature within 10.0C of maximum rated "
                  u"temperature.\n")
            _reason_num += 1
    else:
        if (_voltage_operating > 0.90 * attributes['voltage_rated']):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 90% rated voltage.\n")
            _reason_num += 1

    attributes['reason'] = _reason

    return attributes
