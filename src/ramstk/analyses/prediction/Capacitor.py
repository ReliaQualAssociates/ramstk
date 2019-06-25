# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Reliability Calculations Module."""

# Standard Library Imports
from math import exp

PART_COUNT_217F_LAMBDA_B = {
    1: {
        1: [
            0.0036, 0.0072, 0.330, 0.016, 0.055, 0.023, 0.030, 0.07, 0.13,
            0.083, 0.0018, 0.044, 0.12, 2.1,
        ],
        2: [
            0.0039, 0.0087, 0.042, 0.022, 0.070, 0.035, 0.047, 0.19, 0.35,
            0.130, 0.0020, 0.056, 0.19, 2.5,
        ],
    },
    2: [
        0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030, 0.040, 0.094, 0.15,
        0.11, 0.0024, 0.058, 0.18, 2.7,
    ],
    3: [
        0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068, 0.013, 0.026, 0.048,
        0.044, 0.0010, 0.023, 0.063, 1.1,
    ],
    4: [
        0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012, 0.018, 0.037, 0.066,
        0.060, 0.0014, 0.032, 0.088, 1.5,
    ],
    5: [
        0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026, 0.048, 0.086, 0.14,
        0.10, 0.0020, 0.054, 0.15, 2.5,
    ],
    6: [
        0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096, 0.014, 0.034, 0.053,
        0.048, 0.0011, 0.026, 0.07, 1.2,
    ],
    7: [
        0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095, 0.054,
        0.069, 0.031, 0.00025, 0.012, 0.046, 0.45,
    ],
    8: [
        0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60, 0.48,
        0.0091, 0.25, 0.68, 11.0,
    ],
    9: [
        0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062, 0.035,
        0.045, 0.020, 0.00016, 0.0076, 0.030, 0.29,
    ],
    10: [
        0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015, 0.015, 0.032, 0.048,
        0.077, 0.0014, 0.049, 0.13, 2.3,
    ],
    11: [
        0.00078, 0.0022, 0.013, 0.0056, 0.023, 0.0077, 0.015, 0.053, 0.12,
        0.048, 0.00039, 0.017, 0.065, 0.68,
    ],
    12: [
        0.0018, 0.0039, 0.016, 0.0097, 0.028, 0.0091, 0.011, 0.034, 0.057,
        0.055, 0.00072, 0.022, 0.066, 1.0,
    ],
    13: [
        0.0061, 0.013, 0.069, 0.039, 0.11, 0.031, 0.061, 0.13, 0.29, 0.18,
        0.0030, 0.069, 0.26, 4.0,
    ],
    14: [
        0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6, 1.2, .012,
        0.49, 1.7, 21.0,
    ],
    15: [
        0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4, 2.0, 0.015,
        0.68, 2.8, 28.0,
    ],
    16: [
        0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9,
        5.9, 85.0,
    ],
    17: [
        0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16,
        0.93, 3.2, 37.0,
    ],
    18: [
        0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5,
        8.9, 100.0,
    ],
    19: [
        0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0,
        0.0, 0.0,
    ],
}
PI_C = {1: 0.3, 2: 1.0, 3: 2.0, 4: 2.5, 5: 3.0}
PI_CF = {1: 0.1, 2: 1.0}
REF_TEMPS = {
    65.0: 338.0,
    70.0: 343.0,
    85.0: 358.0,
    105.0: 378.0,
    125.0: 398.0,
    150.0: 423.0,
    170.0: 443.0,
    175.0: 448.0,
    200.0: 473.0,
}


def _calculate_capacitance_factor(attributes):
    """
    Calculate the capacitance facotr (piCV.

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: dict
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
        19: [1.0, 0.0],
    }
    _f0 = _dic_factors[attributes['subcategory_id']][0]
    _f1 = _dic_factors[attributes['subcategory_id']][1]
    attributes['piCV'] = _f0 * attributes['capacitance']**_f1

    return attributes


def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
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
        19: [0.0112, 0.17, 3.0, 1.59, 10.1],
    }

    try:
        _ref_temp = REF_TEMPS[attributes['temperature_rated_max']]
        _f0 = _dic_factors[attributes['subcategory_id']][0]
        _f1 = _dic_factors[attributes['subcategory_id']][1]
        _f2 = _dic_factors[attributes['subcategory_id']][2]
        _f3 = _dic_factors[attributes['subcategory_id']][3]
        _f4 = _dic_factors[attributes['subcategory_id']][4]
        attributes['lambda_b'] = _f0 * (
            (attributes['voltage_ratio'] / _f1)**_f2 + 1.0
        ) * exp(
            _f3 * (
                (attributes['temperature_active'] + 273.0) / _ref_temp
            )**_f4,
        )
    except KeyError:
        attributes['lambda_b'] = 0.0

    return attributes


def _calculate_series_resistance_factor(attributes):
    """
    Calculate the series resistance factor (piSR).

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        _ckt_resistance = attributes['resistance'] / (
            attributes['voltage_dc_operating']
            + attributes['voltage_ac_operating']
        )
    except ZeroDivisionError:
        _ckt_resistance = 0

    if 0 < _ckt_resistance <= 0.1:
        attributes['piSR'] = 0.33
    elif 0.1 < _ckt_resistance <= 0.2:
        attributes['piSR'] = 0.27
    elif 0.2 < _ckt_resistance <= 0.4:
        attributes['piSR'] = 0.2
    elif 0.4 < _ckt_resistance <= 0.6:
        attributes['piSR'] = 0.13
    elif 0.6 < _ckt_resistance <= 0.8:
        attributes['piSR'] = 0.1
    else:
        attributes['piSR'] = 0.066

    return attributes


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the capacitor type which is why a WARKING message is issued
    rather than an ERROR message.

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating capacitor, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'capacitor, hardware ID: {0:d}.\n'.format(
                attributes['hardware_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'capacitor, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

        if attributes['piC'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piC is 0.0 when calculating ' \
                'capacitor, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

        if attributes['piCF'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piCF is 0.0 when calculating ' \
                'capacitor, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

        if attributes['piCR'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piCR is 0.0 when calculating ' \
                'capacitor, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

        if attributes['piSR'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piSR is 0.0 when calculating ' \
                'capacitor, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

    return _msg


def calculate_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. specification id; if the capacitor subcategory is NOT specification
            dependent, then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |           Capacitor \         | MIL-HDBK-217F \ |
    |       ID       |             Style             |    Section      |
    +================+===============================+=================+
    |        1       | Fixed, Paper, Bypass (CA, CP) |       10.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Feed-Through (CZ, CZR) |       10.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Paper and Plastic \    |       10.3      |
    |                | Film (CPV, CQ, CQR)           |                 |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Metallized Paper, \    |       10.4      |
    |                | Paper-Plastic and Plastic \   |                 |
    |                | (CH, CHR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Plastic and \          |       10.5      |
    |                | Metallized Plastic (CFR)      |                 |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Super-Metallized \     |       10.6      |
    |                | Plastic (CRH)                 |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Mica (CM, CMR)         |       10.7      |
    +----------------+-------------------------------+-----------------+
    |        8       | Fixed, Mica, Button (CB)      |       10.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Fixed, Glass (CY, CYR)        |       10.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Fixed, Ceramic, General \     |      10.10      |
    |                | Purpose (CK, CKR)             |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Fixed, Ceramic, Temperature \ |      10.11      |
    |                | Compensating and Chip \       |                 |
    |                | (CC, CCR, CDR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Fixed, Electrolytic, \        |      10.12      |
    |                | Tantalum, Solid (CSR)         |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Fixed, Electrolytic, \        |      10.13      |
    |                | Tantalum, Non-Solid (CL, CLR) |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Fixed, Electrolytic, \        |      10.14      |
    |                | Aluminum (CU, CUR)            |                 |
    +----------------+-------------------------------+-----------------+
    |       15       | Fixed, Electrolytic (Dry), \  |      10.15      |
    |                | Aluminum (CE)                 |                 |
    +----------------+-------------------------------+-----------------+
    |       16       | Variable, Ceramic (CV)        |      10.16      |
    +----------------+-------------------------------+-----------------+
    |       17       | Variable, Piston Type (PC)    |      10.17      |
    +----------------+-------------------------------+-----------------+
    |       18       | Variable, Air Trimmer (CT)    |      10.18      |
    +----------------+-------------------------------+-----------------+
    |       19       | Variable and Fixed, Gas or \  |      10.19      |
    |                | Vacuum (CG)                   |                 |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] == 1:
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


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a capacitor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param dict attributes: the attributes for the capacitor being calculated.
    :return: (attributes, _msg); the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _calculate_capacitance_factor(attributes)
    attributes = _calculate_series_resistance_factor(attributes)

    # Get the construction factor (piC).
    try:
        attributes['piC'] = PI_C[attributes['construction_id']]
    except (IndexError, KeyError):
        attributes['piC'] = 0.0

    # Get the configuration factor (piCF).
    try:
        attributes['piCF'] = PI_CF[attributes['configuration_id']]
    except (IndexError, KeyError):
        attributes['piCF'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 12:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCV']
            * attributes['piSR']
        )
    elif attributes['subcategory_id'] == 13:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCV']
            * attributes['piC']
        )
    elif attributes['subcategory_id'] == 19:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCF']
        )
    else:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCV']
        )

    return attributes, _msg
