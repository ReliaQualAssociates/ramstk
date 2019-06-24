#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Fuse.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Fuse Reliability Calculations Module."""

# Standard Library Imports
import gettext

_ = gettext.gettext


LAMBDA_B_217F_PART_COUNT = [
    0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15, 0.18, 0.18, 0.009, 0.1,
    0.21, 2.3,
]

def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Select the base hazard rate.
    try:
        attributes['lambda_b'] = LAMBDA_B_217F_PART_COUNT[
            attributes['environment_active_id'] - 1
        ]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating fuse, hardware ID: ' \
            '{0:d}, active environment ID: ' \
            '{1:d}'.format(
                attributes['hardware_id'],
                attributes['environment_active_id'],
            )

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
    _msg = ''

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'fuse, hardware ID: {0:d}.\n'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (0.010 * attributes['piE'])

    return attributes, _msg
