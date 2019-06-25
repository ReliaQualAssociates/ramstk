# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Fuse.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Fuse Reliability Calculations Module."""

PART_COUNT_217F_LAMBDA_B = [
    0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15, 0.18, 0.18, 0.009, 0.1,
    0.21, 2.3,
]


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

    if (
            attributes['hazard_rate_method_id'] == 1
            and attributes['lambda_b'] <= 0.0
    ):
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating fuse, hardware ID: ' \
            '{0:d}, active environment ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['environment_active_id'],
            )

    if attributes['hazard_rate_method_id'] == 2 and attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'fuse, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    return _msg


def calculate_217f_part_count_lambda_b(attributes):
    """
    Calculate the part count hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

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

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (0.010 * attributes['piE'])

    return attributes, _msg
