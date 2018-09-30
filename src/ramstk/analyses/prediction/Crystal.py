#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Crystal.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Crystal Reliability Calculations Module."""

import gettext

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # Index is the environment ID.
    _lst_lambda_b = [
        0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70, 0.90, 0.74, 0.016,
        0.42, 1.0, 16.0
    ]
    _lst_piQ = [1.0, 2.1]
    _msg = ''

    # Select the base hazard rate.
    try:
        attributes['lambda_b'] = _lst_lambda_b[
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Select the piQ.
    try:
        attributes['piQ'] = _lst_piQ[attributes['quality_id'] - 1]
    except IndexError:
        attributes['piQ'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating crystal, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, active environment ID: ' \
            '{2:d}'.format(attributes['hardware_id'],
                           attributes['subcategory_id'],
                           attributes['environment_active_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'crystal, hardware ID: {0:d} and quality ID: ' \
            '{1:d}'.format(attributes['hardware_id'], attributes['quality_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'])

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _lst_piE = [
        1.0, 3.0, 10.0, 6.0, 16.0, 12.0, 17.0, 22.0, 28.0, 23.0, 0.5, 13.0,
        32.0, 500.0
    ]
    _lst_piQ = [1.0, 3.4]
    _msg = ''

    # Calculate the base hazard rate.
    attributes['lambda_b'] = 0.013 * attributes['frequency_operating']**0.23

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating crystal, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Determine the quality factor (piQ).
    try:
        attributes['piQ'] = _lst_piQ[attributes['quality_id'] - 1]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'crystal, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the environmental factor (piE).
    try:
        attributes['piE'] = _lst_piE[attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['piE'] = 0.0

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
            'crystal, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE'])

    return attributes, _msg
