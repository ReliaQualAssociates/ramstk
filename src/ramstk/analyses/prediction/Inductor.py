# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor Reliability Calculations Module."""

# Standard Library Imports
from math import exp

PART_COUNT_217F_LAMBDA_B = {
    1: {
        1: [
            0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
            0.11, 0.0018, 0.053, 0.16, 2.3,
        ],
        2: [
            0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
            0.035, 0.11, 0.31, 4.7,
        ],
        3: [
            0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
            0.37, 1.2, 16.0,
        ],
        4: [
            0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
            0.42, 1.2, 19.0,
        ],
    },
    2: {
        1: [
            0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
            0.052, 0.00083, 0.25, 0.073, 1.1,
        ],
        2: [
            0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
            0.10, 0.0017, 0.05, 0.15, 2.2,
        ],
    },
}
PI_Q = {
    1: {
        1: [1.5, 5.0],
        2: [3.0, 7.5],
        3: [8.0, 30.0],
        4: [12.0, 30.0],
    },
    2: [0.03, 0.1, 0.3, 1.0, 4.0, 20.0],
}
REF_TEMPS = {
    1: {
        1: 329.0,
        2: 352.0,
        3: 364.0,
        4: 400.0,
        5: 398.0,
        6: 477.0,
    },
    2: {
        1: 329.0,
        2: 352.0,
        3: 364.0,
        4: 409.0,
    },
}


def _calculate_hot_spot_temperature(**attributes):
    """
    Calculate the coil or transformer hot spot temperature.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    if (
            attributes['subcategory_id'] == 2
            and attributes['specification_id'] == 2
    ):
        if attributes['page_number'] in [1, 2, 3, 5, 7, 9, 10, 13, 14]:
            attributes['temperature_rise'] = 15.0
        elif attributes['page_number'] in [4, 6, 8, 11, 12]:
            attributes['temperature_rise'] = 35.0
        else:
            try:
                attributes[
                    'temperature_rise'
                ] = 125.0 * attributes['power_operating'] / attributes['area']
            except ZeroDivisionError:
                try:
                    attributes[
                        'temperature_rise'
                    ] = 11.5 * (
                        attributes['power_operating']
                        / attributes['weight']**0.6766
                    )
                except ZeroDivisionError:
                    try:
                        attributes[
                            'temperature_rise'
                        ] = 2.1 * (
                            attributes['power_operating']
                            / attributes['weight']**0.6766
                        )
                    except ZeroDivisionError:
                        attributes['temperature_rise'] = 0.0

    attributes['temperature_hot_spot'] = (
        attributes['temperature_active']
        + 1.1 * attributes['temperature_rise']
    )

    return attributes


def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param dict attributes: the attributes for the connection being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    _dic_factors = {
        1: {
            1: [0.0018, 15.6],
            2: [0.002, 14.0],
            3: [0.0018, 8.7],
            4: [0.002, 10.0],
            5: [0.00125, 3.8],
            6: [0.00159, 8.4],
        },
        2: {
            1: [0.000335, 15.6],
            2: [0.000379, 14.0],
            3: [0.000319, 8.7],
            4: [0.00035, 10.0],
        },
    }

    try:
        _ref_temp = REF_TEMPS[attributes['subcategory_id']][
            attributes[
                'insulation_id'
            ]
        ]
        _f0 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'insulation_id'
            ]
        ][0]
        _f1 = _dic_factors[attributes['subcategory_id']][
            attributes[
                'insulation_id'
            ]
        ][1]
        attributes['lambda_b'] = _f0 * exp(
            ((attributes['temperature_hot_spot'] + 273.0) / _ref_temp)**_f1,
        )
    except (KeyError, ZeroDivisionError):
        attributes['lambda_b'] = 0.0

    return attributes


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the fuse type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the fuse being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating inductor, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, family ID: {2:d}, and active ' \
            'environment ID: {3:d}.\n'.format(
                attributes['hardware_id'],
                attributes['subcategory_id'],
                attributes['family_id'],
                attributes['environment_active_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'inductor, hardware ID: {0:d}, quality ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['quality_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'inductor, hardware ID: {0:d}, ' \
                'active environment ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['environment_active_id'],
                )

        if attributes['piC'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piC is 0.0 when calculating ' \
                'inductor, hardware ID: {0:d}, ' \
                'construction ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['construction_id'],
                )

    return _msg


def _get_part_stress_quality_factor(attributes):
    """
    Select the MIL-HDBK-217F quality factor for the inductor device.

    :param dict attributes: the hardware attributes for the inductor.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] == 1:
            attributes['piQ'] = PI_Q[attributes['subcategory_id']][
                attributes['family_id']
            ][attributes['quality_id'] - 1]
        else:
            attributes['piQ'] = PI_Q[attributes['subcategory_id']][
                attributes['quality_id'] - 1
            ]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

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
        #. family id; if the inductor subcategory is NOT family dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |           Inductor \          | MIL-HDBK-217F \ |
    |       ID       |             Style             |    Section      |
    +================+===============================+=================+
    |        1       | Transformer                   |       11.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Coil                          |       11.2      |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the inductor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
            attributes['subcategory_id']
        ][
            attributes['family_id']
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
    Calculate the part stress hazard rate for a inductor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_hot_spot_temperature(**attributes)
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _get_part_stress_quality_factor(attributes)

    # Get the construction factor (piC).
    try:
        attributes['piC'] = (
            2.0 if (attributes['construction_id']) - (1)
            else 1.0
        )
    except IndexError:
        attributes['piC'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piC']
        )

    return attributes, _msg
