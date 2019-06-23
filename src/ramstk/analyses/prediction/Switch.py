# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Reliability Calculations Module."""

# Standard Library Imports
import gettext
from math import exp

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a switch.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id.  Current subcategory IDs are:
    #
    #    1. Toggle or pushbutton
    #    2. Sensitive
    #    3. Rotary
    #    4. Thumbwheel
    #    5. Circuit breaker
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
        1: [
            0.0010, 0.0030, 0.018, 0.0080, 0.029, 0.010, 0.018, 0.013, 0.022,
            0.046, 0.0005, 0.025, 0.067, 1.2,
        ],
        2: [
            0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3, 6.8, 0.74, 3.7, 9.9,
            180.0,
        ],
        3: [
            0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2, 15.0, 0.16, 8.2,
            22.0, 390.0,
        ],
        4: [
            0.56, 1.7, 10.0, 4.5, 16.0, 5.6, 10.0, 7.3, 12.0, 26.0, 0.26, 14.0,
            38.0, 670.0,
        ],
        5: {
            1: [
                0.11, 0.23, 1.7, 0.91, 3.1, 0.8, 1.0, 1.3, 1.4, 5.2, 0.057,
                2.8, 7.5, 0.0,
            ],
            2: [
                0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66, 0.72, 2.8,
                0.030, 1.5, 4.0, 0.0,
            ],
        },
    }

    # Select the base hazard rate.
    try:
        if attributes['subcategory_id'] == 5:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
                attributes['construction_id']
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
        _msg = 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating switch, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, construction ID: {2:d}, and ' \
            'active environment ID: ' \
            '{3:d}.\n'.format(
                attributes['hardware_id'],
                attributes['subcategory_id'],
                attributes['construction_id'],
                attributes['environment_active_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'switch, hardware ID: {0:d}, subcategory ID: {2:d}, and quality ' \
            'ID: {1:d}.'.format(
                attributes['hardware_id'],
                attributes['quality_id'],
                attributes['subcategory_id'],
            )

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):  # pylint: disable=R0912
    """
    Calculate the part stress hazard rate for a switch.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_factors = {
        2: [[0.1, 0.00045, 0.0009], [0.1, 0.23, 0.63]],
        3: [[0.0067, 0.00003, 0.00003], [0.1, 0.02, 0.06]],
        4: [[0.0067, 0.062], [0.086, 0.089]],
    }
    _dic_lambda_b = {
        1: [[0.00045, 0.034], [0.0027, 0.04]],
        5: [0.02, 0.038, 0.038],
    }
    _dic_piC = {
        1: [1.0, 1.5, 1.7, 2.0, 2.5, 3.0, 4.2, 5.5, 8.0],
        5: [1.0, 2.0, 3.0, 4.0],
    }
    _msg = ''

    # Calculate the base hazard rate.
    if attributes['subcategory_id'] == 1:
        attributes['lambda_b'] = _dic_lambda_b[1][
            attributes[
                'construction_id'
            ]
        ][attributes['quality_id'] - 1]
    elif attributes['subcategory_id'] in [2, 3]:
        try:
            _lambda_bE = _dic_factors[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ][0]
            _lambda_bC = _dic_factors[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ][1]
            _lambda_b0 = _dic_factors[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ][2]
        except (IndexError, KeyError):
            _lambda_bE = 0.0
            _lambda_bC = 0.0
            _lambda_b0 = 0.0
        if attributes['construction_id'] == 1:
            attributes['lambda_b'] = (
                _lambda_bE + attributes['n_elements'] * _lambda_bC
            )
        else:
            attributes['lambda_b'] = (
                _lambda_bE + attributes['n_elements'] * _lambda_b0
            )
    elif attributes['subcategory_id'] == 4:
        try:
            _lambda_b1 = _dic_factors[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ][0]
            _lambda_b2 = _dic_factors[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ][1]
        except (IndexError, KeyError):
            _lambda_b1 = 0.0
            _lambda_b2 = 0.0
        attributes['lambda_b'] = (
            _lambda_b1 + attributes['n_elements'] * _lambda_b2
        )
    elif attributes['subcategory_id'] == 5:
        attributes['lambda_b'] = _dic_lambda_b[5][attributes['application_id'] - 1]
    else:
        attributes['lambda_b'] = 0.0

    if attributes['lambda_b'] <= 0.0:
        _msg = 'RAMSTK WARNING: Base hazard rate is 0.0 when calculating ' \
               'switch, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    # Determine the quality factor (piQ).
    if attributes['piQ'] <= 0.0:
        _msg = 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'switch, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    if attributes['piE'] <= 0.0:
        _msg = 'RAMSTK WARNING: piE is 0.0 when calculating switch, hardware ' \
               'ID: {0:d}.\n'.format(attributes['hardware_id'])

    # Determine the cycling factor (piCYC).
    if attributes['n_cycles'] <= 1:
        attributes['piCYC'] = 1.0
    else:
        attributes['piCYC'] = float(attributes['n_cycles'])

    # Calculate the load stress factor (piL).
    if attributes['subcategory_id'] != 5:
        if attributes['application_id'] == 1:  # Resistive
            attributes['piL'] = exp((attributes['current_ratio'] / 0.8)**2.0)
        elif attributes['application_id'] == 2:  # Inductive
            attributes['piL'] = exp((attributes['current_ratio'] / 0.4)**2.0)
        elif attributes['application_id'] == 3:  # Capacitive
            attributes['piL'] = exp((attributes['current_ratio'] / 0.2)**2.0)

    # Determine the contact form and quantity factor (piC).
    if attributes['subcategory_id'] in [1, 5]:
        attributes['piC'] = _dic_piC[attributes['subcategory_id']][
            attributes['contact_form_id'] - 1
        ]

    # Determine the use factor (piU).
    if attributes['subcategory_id'] == 5:
        attributes['piU'] = (
            10.0
            if (attributes['application_id']) - (1) else 1.0
        )

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCYC'] *
            attributes['piL'] * attributes['piC']
        )
    elif attributes['subcategory_id'] in [2, 3, 4]:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piCYC'] *
            attributes['piL']
        )
    elif attributes['subcategory_id'] == 5:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piC'] *
            attributes['piU'] * attributes['piQ']
        )
    else:
        attributes['hazard_rate_active'] = 0.0

    return attributes, _msg
