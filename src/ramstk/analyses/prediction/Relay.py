# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Reliability Calculations Module."""

# Standard Library Imports
import gettext
from math import exp

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a relay.

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
    #    1. Mechanical
    #    2. Solid-State
    #
    # These keys return a list of base hazard rate lists.  The proper internal
    # list is selected by the type ID.  The hazard rate in to use is selected
    # from the list depending on the active environment.
    _dic_lambda_b = {
        1: [
            [
                0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5,
                10.0, 0.0,
            ], [
                0.43, 0.89, 6.9, 3.6, 12.0, 3.4, 4.4, 6.2, 6.7, 22.0, 0.21,
                11.0, 32.0, 0.0,
            ], [
                0.13, 0.26, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0, 0.66, 3.5,
                10.0, 0.0,
            ], [
                0.11, 0.23, 1.8, 0.92, 3.3, 0.96, 1.2, 2.1, 2.3, 6.5, 0.54,
                3.0, 9.0, 0.0,
            ], [
                0.29, 0.60, 4.8, 2.4, 8.2, 2.3, 2.9, 4.1, 4.5, 15.0, 0.14, 7.6,
                22.0, 0.0,
            ], [
                0.88, 1.8, 14.0, 7.4, 26.0, 7.1, 9.1, 13.0, 14.0, 46.0, 0.44,
                24.0, 67.0, 0.0,
            ],
        ],
        2: [
            [
                0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2, 0.16, 4.8,
                13.0, 240.0,
            ], [
                0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0, 12.0, 0.20,
                5.0, 17.0, 300.0,
            ],
        ],
    }

    # Select the base hazard rate.
    try:
        _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
            attributes['type_id'] - 1
        ]
    except (KeyError, IndexError):
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
            'calculating relay, hardware ID: {0:d}, subcategory ID: {1:d}, ' \
            'type ID: {3:d}, and active environment ID: ' \
            '{2:d}.\n'.format(
                attributes['hardware_id'],
                attributes['subcategory_id'],
                attributes['environment_active_id'],
                attributes['type_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'relay, hardware ID: {0:d}, subcategory ID: {2:d}, and quality ' \
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
    Calculate the part stress hazard rate for a relay.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_factors = {
        1: [[0.00555, 352.0, 15.7], [0.0054, 377.0, 10.4]],
        2: [0.4, 0.5, 0.5],
    }
    _dic_piC = {1: [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]}
    _dic_piF = {
        1: [[
            [4.0, 8.0], [6.0, 18.0], [1.0, 3.0], [4.0, 8.0], [7.0, 14.0],
            [7.0, 14.0],
        ]],
        2:
        [
            [
                [3.0, 6.0], [5.0, 10.0],
                [6.0, 12.0],
            ], [
                [5.0, 10.0], [2.0, 6.0], [6.0, 12.0], [100.0, 100.0],
                [10.0, 20.0],
            ], [[10.0, 20.0], [100.0, 100.0]],
            [[6.0, 12.0], [1.0, 3.0]], [[25.0, 0.0], [6.0, 0.0]],
            [[10.0, 20.0]], [[9.0, 12.0]], [
                [10.0, 20.0], [5.0, 10.0],
                [5.0, 10.0],
            ],
        ],
        3: [
            [[20.0, 40.0], [5.0, 10.0]], [
                [3.0, 6.0], [1.0, 3.0], [2.0, 6.0],
                [3.0, 6.0], [2.0, 6.0], [2.0, 6.0],
            ],
        ],
        4: [[[7.0, 14.0], [12.0, 24.0], [10.0, 20.0], [5.0, 10.0]]],
    }
    _dic_piQ = {1: [0.1, 0.3, 0.45, 0.6, 1.0, 1.5, 3.0], 2: [1.0, 4.0]}
    _dic_piE = {
        1: [
            [
                1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0, 0.50,
                25.0, 66.0, 0.0,
            ], [
                2.0, 5.0, 44.0, 24.0, 78.0, 15.0, 20.0, 28.0, 38.0, 140.0, 1.0,
                72.0, 200.0, 0.0,
            ],
        ],
        2: [
            1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0, 0.4, 12.0,
            33.0, 590.0,
        ],
    }
    _msg = ''

    # Calculate the base hazard rate.
    if attributes['subcategory_id'] == 1:
        _f0 = _dic_factors[attributes['subcategory_id']][
            attributes['type_id']
            - 1
        ][0]
        _f1 = _dic_factors[attributes['subcategory_id']][
            attributes['type_id']
            - 1
        ][1]
        _f2 = _dic_factors[attributes['subcategory_id']][
            attributes['type_id']
            - 1
        ][2]
        attributes['lambda_b'] = _f0 * exp(
            ((attributes['temperature_active'] + 273.0) / _f1)**_f2,
        )
    elif attributes['subcategory_id'] == 2:
        attributes['lambda_b'] = _dic_factors[attributes['subcategory_id']][
            attributes['type_id'] - 1
        ]
    else:
        attributes['lambda_b'] = 0.0

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating relay, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Calculate the load stress factor (piL).
    if attributes['subcategory_id'] == 1:
        if attributes['technology_id'] == 1:
            attributes['piL'] = (attributes['current_ratio'] / 0.8)**2.0
        elif attributes['technology_id'] == 2:
            attributes['piL'] = (attributes['current_ratio'] / 0.4)**2.0
        elif attributes['technology_id'] == 3:
            attributes['piL'] = (attributes['current_ratio'] / 0.2)**2.0
        else:
            attributes['piL'] = 1.0

    # Determine the contact form factor (piC).
    if attributes['subcategory_id'] == 1:
        attributes['piC'] = _dic_piC[attributes['subcategory_id']][
            attributes['contact_form_id'] - 1
        ]

    # Determine cycling factor (piCYC).
    if attributes['subcategory_id'] == 1:
        if (
                attributes['quality_id'] in [1, 2, 3, 4, 5, 6]
                and attributes['n_cycles'] < 1.0
        ):
            attributes['piCYC'] = 0.1
        elif attributes['quality_id'] == 7 and attributes['n_cycles'] > 1000:
            attributes['piCYC'] = (attributes['n_cycles'] / 100.0)**2.0
        elif (
                attributes['quality_id'] == 7 and attributes['n_cycles'] > 10
                and attributes['n_cycles'] < 1000
        ):
            attributes['piCYC'] = attributes['n_cycles'] / 10.0
        else:
            attributes['piCYC'] = 1.0

    # Determine application and construction factor (piF).
    if attributes['subcategory_id'] == 1:
        if attributes['quality_id'] in [1, 2, 3, 4, 5, 6]:
            _quality = 0
        else:
            _quality = 1
        attributes['piF'] = _dic_piF[attributes['contact_rating_id']][
            attributes['application_id'] - 1
        ][
            attributes['construction_id'] - 1
        ][_quality]

    # Determine the quality factor (piQ).
    try:
        attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
            attributes['quality_id'] - 1
        ]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'relay, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the environmental factor (piE).
    if attributes['subcategory_id'] == 1:
        try:
            attributes['piE'] = _dic_piE[1][_quality][
                attributes['environment_active_id'] - 1
            ]
        except IndexError:
            attributes['piE'] = 0.0
    else:
        try:
            attributes['piE'] = _dic_piE[2][
                attributes['environment_active_id']
                - 1
            ]
        except (KeyError, IndexError):
            attributes['piE'] = 0.0

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'relay, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piL'] *
            attributes['piC'] * attributes['piCYC'] * attributes['piF']
        )

    return attributes, _msg
