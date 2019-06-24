# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Filter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Filter Reliability Calculations Module."""

PART_COUNT_217F_LAMBDA_B = {
    1: [
        0.022, 0.044, 0.13, 0.088, 0.20, 0.15, 0.20, 0.24, 0.29, 0.24,
        0.018, 0.15, 0.33, 2.6,
    ],
    2: [
        0.12, 0.24, 0.72, 0.48, 1.1, 0.84, 1.1, 1.3, 1.6, 1.3, 0.096, 0.84,
        1.8, 1.4,
    ],
    3: [
        0.27, 0.54, 1.6, 1.1, 2.4, 1.9, 2.4, 3.0, 3.5, 3.0, 0.22, 1.9, 4.1,
        32.0,
    ],
}
PART_STRESS_217F_LAMBDA_B = {1: 0.022, 2: 0.12, 3: 0.12, 4: 0.27}


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the connection type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the filter being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating filter, hardware ID: {0:d}, ' \
            'type ID: {2:d}, ' \
            'active environment ID: {1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['environment_active_id'],
                attributes['type_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'filter, hardware ID: {0:d}, quality ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['quality_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'filter, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )
    print(_msg)
    return _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a filter.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    try:
        attributes['lambda_b'] = PART_COUNT_217F_LAMBDA_B[
            attributes['type_id']
        ][
            attributes['environment_active_id'] - 1
        ]
    except (KeyError, IndexError):
        attributes['lambda_b'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a filter.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    try:
        attributes['lambda_b'] = PART_STRESS_217F_LAMBDA_B[
            attributes['type_id']
        ]
    except (KeyError, IndexError):
        attributes['lambda_b'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )

    return attributes, _msg
