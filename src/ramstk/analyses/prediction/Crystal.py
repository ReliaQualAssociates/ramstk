# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Crystal.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Crystal Reliability Calculations Module."""

PART_COUNT_217F_LAMBDA_B = [
        0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70, 0.90, 0.74, 0.016,
        0.42, 1.0, 16.0,
]


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the connection type which is why a WARKING message is issued
    rather than an ERROR message.

    :param dict attributes: the attributes for the connection being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating crystal, hardware ID: {0:d}.\n'.format(
                attributes['hardware_id'],
            )

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'crystal, hardware ID: {0:d} and quality ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'], attributes['quality_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'crystal, hardware ID: {0:d} and active environment ID: ' \
                '{1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['environment_active_id'],
                )
    print(_msg)
    return _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :param dict attributes: the attributes for the connection being calculated.
    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    try:
        attributes['lambda_b'] = PART_COUNT_217F_LAMBDA_B[
            attributes['environment_active_id'] - 1
        ]
    except IndexError:
        attributes['lambda_b'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param dict attributes: the attributes for the connection being calculated.
    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes['lambda_b'] = 0.013 * attributes['frequency_operating']**0.23

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE']
    )

    return attributes, _msg
