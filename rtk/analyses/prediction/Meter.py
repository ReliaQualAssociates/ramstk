#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.Meter.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Meter Calculations Module."""

import gettext

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a meter.

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
            'when calculating meter, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RTK WARNING: dty cycle is 0.0 when calculating ' \
            'meter, hardware ID: {0:d}'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RTK WARNING: Quantity is less than 1 when ' \
            'calculating meter, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    return attributes, _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id.  Current subcategory IDs are:
    #
    #    1. Panel
    #    2. Elapsed time
    #
    # These keys return a list of base hazard rate lists.  The proper internal
    # list is selected by the type ID.  The hazard rate to use is selected from
    # the list depending on the active environment.
    _dic_lambda_b = {
        1: [[
            0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6, 5.4, 0.099, 5.4,
            0.0, 0.0
        ], [
            0.15, 0.61, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0, 9.2, 0.17, 9.2,
            0.0, 0.0
        ]],
        2: [[
            10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0, 160.0, 250.0, 260.0,
            5.0, 140.0, 380.0, 0.0
        ], [
            15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0, 240.0, 375.0, 390.0,
            7.5, 210.0, 570.0, 0.0
        ], [
            40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0, 640.0, 1000.0,
            1040.0, 20.0, 560.0, 1520.0, 0.0
        ]]
    }

    # List containing piQ values for parts count method.  The list positions
    # corrspond to the following quality levels:
    #
    #   0. MIL-SPEC
    #   1. Non-MIL
    #
    # The quality_id attribute is used to select the proper value of piQ.
    _dic_piQ = {1: [1.0, 3.4]}
    _msg = ''

    # Select the base hazard rate.
    try:
        _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
            attributes['type_id'] - 1]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Select the piQ.
    if attributes['subcategory_id'] == 1:
        try:
            attributes['piQ'] = _dic_piQ[1][attributes['quality_id'] - 1]
        except IndexError:
            attributes['piQ'] = 0.0
    else:
        attributes['piQ'] = 1.0

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating meter, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, active environment ID: ' \
            '{2:d}'.format(attributes['hardware_id'],
                           attributes['subcategory_id'],
                           attributes['environment_active_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'meter, hardware ID: {0:d} and quality ID: ' \
            '{1:d}'.format(attributes['hardware_id'], attributes['quality_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'])

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_lambda_b = {1: 0.09, 2: [20.0, 30.0, 80.0]}
    _dic_piE = {
        1: [
            1.0, 4.0, 25.0, 12.0, 35.0, 28.0, 42.0, 58.0, 73.0, 60.0, 1.1,
            60.0, 0.0, 0.0
        ],
        2: [
            1.0, 2.0, 12.0, 7.0, 18.0, 5.0, 8.0, 16.0, 25.0, 26.0, 0.5, 14.0,
            38.0, 0.0
        ]
    }
    _lst_piF = [1.0, 1.0, 2.8]
    _lst_piQ = [1.0, 3.4]
    _msg = ''

    # Calculate the temperature ratio.
    try:
        _temperature_ratio = (attributes['temperature_active'] /
                              attributes['temperature_rated_max'])
    except ZeroDivisionError:
        _temperature_ratio = 1.0

    # Calculate the base hazard rate.
    if attributes['subcategory_id'] == 1:
        attributes['lambda_b'] = _dic_lambda_b[1]
    elif attributes['subcategory_id'] == 2:
        attributes['lambda_b'] = _dic_lambda_b[2][attributes['type_id'] - 1]
    else:
        attributes['lambda_b'] = 0.0

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating meter, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Determine the application factor (piA) and function factor (piF).
    if attributes['subcategory_id'] == 1:
        attributes['piA'] = (1.7
                             if (attributes['type_id']) - (1) else 1.0)
        attributes['piF'] = _lst_piF[attributes['application_id'] - 1]

    # Determine the temperature stress factor (piT).
    if attributes['subcategory_id'] == 2:
        if _temperature_ratio > 0.0 and _temperature_ratio <= 0.5:
            attributes['piT'] = 0.5
        elif _temperature_ratio > 0.5 and _temperature_ratio <= 0.6:
            attributes['piT'] = 0.6
        elif _temperature_ratio > 0.6 and _temperature_ratio <= 0.8:
            attributes['piT'] = 0.8
        elif _temperature_ratio > 0.8 and _temperature_ratio <= 1.0:
            attributes['piT'] = 1.0

    # Determine the quality factor (piQ).
    if attributes['subcategory_id'] == 1:
        try:
            attributes['piQ'] = _lst_piQ[attributes['quality_id'] - 1]
        except (KeyError, IndexError):
            attributes['piQ'] = 0.0

        if attributes['piQ'] <= 0.0:
            _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
                'meter, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the environmental factor (piE).
    attributes['piE'] = _dic_piE[attributes['subcategory_id']][
        attributes['environment_active_id'] - 1]

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'meter, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piE'])
    if attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piF'] * attributes['piQ'])
    elif attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piT'])

    return attributes, _msg
