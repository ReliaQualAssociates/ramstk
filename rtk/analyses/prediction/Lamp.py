#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.Lamp.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Lamp Calculations Module."""

import gettext

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a lamp.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    if attributes['hazard_rate_method_id'] == 1:
        attributes, _msg = calculate_217f_part_count(**attributes)
    elif attributes['hazard_rate_method_id'] == 2:
        attributes, _msg = calculate_217f_part_stress(**attributes)

    if attributes['mult_adj_factor'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Multiplicative adjustment factor is 0.0 ' \
            'when calculating lamp, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RTK WARNING: dty cycle is 0.0 when calculating ' \
            'lamp, hardware ID: {0:d}'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RTK WARNING: Quantity is less than 1 when ' \
            'calculating lamp, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    return attributes, _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # Index is the environment ID.
    _dic_lambda_b = {
        1: [
            3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0, 23.0, 19.0, 2.7,
            16.0, 23.0, 100.0
        ],
        2: [
            13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0, 77.0, 64.0, 9.0,
            51.0, 77.0, 350.0
        ]
    }
    _msg = ''

    # Select the base hazard rate.
    try:
        attributes['lambda_b'] = _dic_lambda_b[attributes['type_id']][
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating lamp, hardware ID: ' \
            '{0:d}, active environment ID: ' \
            '{1:d}'.format(attributes['hardware_id'],
                           attributes['environment_active_id'])

    # Calculate the hazard rate.
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
    _lst_piE = [
        1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 5.0, 6.0, 5.0, 0.7, 4.0, 6.0, 27.0
    ]
    _msg = ''

    # Calculate the base hazard rate.
    attributes['lambda_b'] = 0.074 * attributes['voltage_rated']**1.29

    # Determine the utilization factor (piU).
    _utilization = attributes['duty_cycle'] / 100.0
    if _utilization < 0.1:
        attributes['piU'] = 0.1
    elif _utilization >= 0.1 and _utilization < 0.9:
        attributes['piU'] = 0.72
    else:
        attributes['piU'] = 1.0

    # Determine the application factor (piA).
    try:
        attributes['piA'] = (3.3
                             if (attributes['application_id']) - (1) else 1.0)
    except IndexError:
        attributes['piA'] = 0.0

    # Determine the environmental factor (piE).
    try:
        attributes['piE'] = _lst_piE[attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['piE'] = 0.0

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'lamp, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (attributes['lambda_b'] * attributes[
        'piU'] * attributes['piA'] * attributes['piE'])

    return attributes, _msg
