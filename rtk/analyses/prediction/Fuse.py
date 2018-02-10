#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.Fuse.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Fuse Reliability Calculations Module."""

import gettext

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # Type ID is the key.  Index is the environment ID.
    _lst_lambda_b = [
        0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15, 0.18, 0.18, 0.009, 0.1,
        0.21, 2.3
    ]
    _msg = ''

    # Select the base hazard rate.
    try:
        attributes['lambda_b'] = _lst_lambda_b[
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating fuse, hardware ID: ' \
            '{0:d}, active environment ID: ' \
            '{1:d}'.format(attributes['hardware_id'],
                           attributes['environment_active_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = attributes['lambda_b']

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
    _lst_piE = [
        1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0, 0.9, 10.0, 21.0,
        230.0
    ]
    _msg = ''

    # Determine the environmental factor (piE).
    try:
        attributes['piE'] = _lst_piE[attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['piE'] = 0.0

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'fuse, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (0.010 * attributes['piE'])

    return attributes, _msg
