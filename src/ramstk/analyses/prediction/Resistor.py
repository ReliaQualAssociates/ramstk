# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Reliability Calculations Module."""

# Standard Library Imports
import gettext
from math import exp

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a resistor.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id, second key is the specification id.  If
    # the resistor subcategory is NOT specification dependent, then the second
    # key will be zero.  Current subcategory IDs are:
    #
    #    1. Fixed, Composition (RC, RCR)
    #    2. Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)
    #    3. Fixed, Film, Power (RD)
    #    4. Fixed, Film, Network (RZ)
    #    5. Fixed, Wirewound, Power (RB, RBR)
    #    6. Fixed, Wirewound, Power, Chassis Mounted (RE, RER)
    #    7. Thermistor
    #    8. Variable, Wirewound (RT, RTR)
    #    9. Variable, Wirewound, Precision (RR)
    #   10. Variable, Wirewound, Semiprecision (RA, RK)
    #   11. Variable, Non-Wirewound (RJ, RJR)
    #   12. Variable, Composition (RV)
    #   13. Variable,Non-Wirewound, Film and Precision (RQ, RVC)
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
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

    # List containing piQ values for parts count method.  The list positions
    # corrspond to the following quality levels:
    #
    #   0. Established reliability level S
    #   1. Established reliability level R
    #   2. Established reliability level P
    #   3. Established reliability level M
    #   4. Non-established reliability MIL-SPEC
    #   5. Non-established reliability lower
    #
    # The quality_id attribute is used to select the proper value of piQ.
    _lst_piQ = [0.030, 0.10, 0.30, 1.0, 3.0, 10.0]

    # Select the base hazard rate.
    try:
        if attributes['subcategory_id'] in [2, 6]:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
                attributes['specification_id']
            ]
        else:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1
        ]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
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
            '{1:d}.'.format(
                attributes['hardware_id'],
                attributes['quality_id'],
            )

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):  # pylint: disable=R0912, R0914
    """
    Calculate the part stress hazard rate for a resistor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_ref_temp = {
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
    # Resistance factor (piR) dictionary of values.  The key is the
    # subcategory ID.  The index in the returned list is the resistance range
    # breakpoint (breakpoint values are in _lst_breakpoints below).  For
    # subcategory ID 6 and 7, the specification ID selects the correct set of
    # lists, then the style ID selects the proper list of piR values and then
    # the resistance range breakpoint is used to select
    _dic_piR = {
        1: [1.0, 1.1, 1.6, 2.5],
        2: [1.0, 1.1, 1.6, 2.5],
        3: [1.0, 1.2, 1.3, 3.5],
        5: [1.0, 1.7, 3.0, 5.0],
        6: [
            [
                [1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0,],
                [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6,],
                [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0,],
                [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,],
                [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0,],
            ],
            [
                [1.0, 1.0, 1.0, 1.0, 1.2, 1.6,],
                [1.0, 1.0, 1.0, 1.2, 1.6, 0.0,],
                [1.0, 1.0, 1.2, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 2.0, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 2.0, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 2.0, 0.0, 0.0,],
                [1.0, 1.2, 1.4, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.6, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 2.0, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.2, 0.0, 0.0,],
                [1.0, 1.0, 1.4, 0.0, 0.0, 0.0,],
                [1.0, 1.2, 1.6, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.4, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 1.5, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 1.6, 0.0,],
                [1.0, 1.0, 1.0, 1.4, 1.6, 2.0,],
                [1.0, 1.0, 1.0, 1.4, 1.6, 2.0,],
                [1.0, 1.0, 1.4, 2.4, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 2.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 0.0, 0.0, 0.0, 0.0,],
                [1.0, 1.2, 1.4, 0.0, 0.0, 0.0,],
                [1.0, 1.0, 1.2, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.0, 1.6, 0.0, 0.0,],
                [1.0, 1.0, 1.4, 0.0, 0.0, 0.0,],
                [1.0, 1.2, 1.5, 0.0, 0.0, 0.0,],
                [1.0, 1.2, 0.0, 0.0, 0.0, 0.0,],
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
    # Dictionary containing the number of element breakpoints for determining
    # the resistance factor list to use.
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
    _dic_piV = {
        9: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
        10: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
        11: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
        12: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
        13: [1.0, 1.05, 1.2],
        14: [1.0, 1.05, 1.2],
        15: [1.0, 1.05, 1.2],
    }
    _dic_piC = {10: [2.0, 1.0, 3.0, 1.5], 12: [2.0, 1.0]}
    _msg = ''

    # Calculate the base hazard rate.
    if attributes['subcategory_id'] == 2:
        _ref_temp = _dic_ref_temp[attributes['subcategory_id']][
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
        _ref_temp = _dic_ref_temp[attributes['subcategory_id']]
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

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating resistor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Calculate the resistance factor (piR).
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

        if attributes['subcategory_id'] in [6, 7]:
            attributes['piR'] = _dic_piR[attributes['subcategory_id']][
                attributes['specification_id'] - 1
            ][
                attributes['family_id'] - 1
            ][_index + 1]
        elif attributes['subcategory_id'] not in [4, 8]:
            attributes['piR'] = _dic_piR[attributes['subcategory_id']][
                _index + 1
            ]

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'resistor, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'resistor, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    # Calculate the temperature factor (piT).
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

    # Calculate the taps factor (piTAPS).
    if attributes['subcategory_id'] in [9, 10, 11, 12, 13, 14, 15]:
        attributes['piTAPS'] = (attributes['n_elements']**1.5 / 25.0) + 0.792

    # Calculate the voltage factor (piV).
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
        attributes['piV'] = _dic_piV[attributes['subcategory_id']][_index]

    # Determine the consruction class factor (piC).
    if attributes['subcategory_id'] in [10, 12]:
        attributes['piC'] = _dic_piC[attributes['subcategory_id']][
            attributes['construction_id'] - 1
        ]

    # Calculate the active hazard rate.
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
