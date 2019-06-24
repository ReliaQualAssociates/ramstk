# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Lamp.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Lamp Reliability Calculations Module."""

PART_COUNT_217F_LAMBDA_B = {
    1: [
        3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0, 23.0, 19.0, 2.7,
        16.0, 23.0, 100.0,
    ],
    2: [
        13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0, 77.0, 64.0, 9.0,
        51.0, 77.0, 350.0,
    ],
}


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the lamp type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the lamp being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    try:
        1.0 / attributes['lambda_b']
    except ZeroDivisionError:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating lamp, hardware ID: ' \
            '{0:d}, active environment ID: ' \
            '{1:d}.\n'.format(
                attributes['hardware_id'],
                attributes['environment_active_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        try:
            1.0 / attributes['piA']
        except ZeroDivisionError:
            _msg = _msg + 'RAMSTK WARNING: piA is 0.0 when calculating ' \
                'lamp, hardware ID: {0:d}, ' \
                'application ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['application_id'],
                )

        try:
            1.0 / attributes['piE']
        except ZeroDivisionError:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'lamp, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

        try:
            1.0 / attributes['piU']
        except ZeroDivisionError:
            _msg = _msg + 'RAMSTK WARNING: piU is 0.0 when calculating ' \
                'lamp, hardware ID: {0:d}, ' \
                'duty cycle: {1:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['duty_cycle'],
                )

    return _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    try:
        attributes['lambda_b'] = PART_COUNT_217F_LAMBDA_B[
            attributes['application_id']
        ][
            attributes['environment_active_id'] - 1
        ]
    except (IndexError, KeyError):
        attributes['lambda_b'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = attributes['lambda_b']

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes['lambda_b'] = 0.074 * attributes['voltage_rated']**1.29

    # Determine the utilization factor (piU).
    if attributes['duty_cycle'] < 10.0:
        attributes['piU'] = 0.1
    elif 10.0 <= attributes['duty_cycle'] < 90.0:
        attributes['piU'] = 0.72
    else:
        attributes['piU'] = 1.0

    # Determine the application factor (piA).
    try:
        attributes['piA'] = (
            3.3
            if (attributes['application_id']) - (1) else 1.0
        )
    except IndexError:
        attributes['piA'] = 0.0

    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piU'] * attributes['piA'] *
        attributes['piE']
    )

    return attributes, _msg
