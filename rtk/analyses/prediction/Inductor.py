#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.Inductor.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Inductor Reliability Calculations Module."""

import gettext

from math import exp

_ = gettext.gettext


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a inductor.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id, second key is the family id.  Current
    # subcategory IDs are:
    #
    #    1. Transformer
    #    2. Coil
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
        1: {
            1: [
                0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
                0.11, 0.0018, 0.053, 0.16, 2.3
            ],
            2: [
                0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10,
                0.22, 0.035, 0.11, 0.31, 4.7
            ],
            3: [
                0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82,
                0.011, 0.37, 1.2, 16.0
            ],
            4: [
                0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88,
                0.015, 0.42, 1.2, 19.0
            ]
        },
        2: {
            1: [
                0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016,
                0.022, 0.052, 0.00083, 0.25, 0.073, 1.1
            ],
            2: [
                0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
                0.10, 0.0017, 0.05, 0.15, 2.2
            ]
        }
    }

    # List containing piQ values for parts count method.  The list positions
    # corrspond to the following quality levels:
    #
    #   0. Established reliability
    #   1. Non-established reliability MIL-SPEC
    #   2. Non-established reliability non-MIL
    #
    # The quality_id attribute is used to select the proper value of piQ.
    _lst_piQ = [0.25, 1.0, 10.0]

    # Select the base hazard rate.
    try:
        _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][attributes[
            'family_id']]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
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
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating inductor, hardware ID: ' \
            '{0:d}, subcategory ID: {1:d}, family ID: {2:d}, and active ' \
            'environment ID: {3:d}.'.format(attributes['hardware_id'],
                                            attributes['subcategory_id'],
                                            attributes['family_id'],
                                            attributes['environment_active_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'inductor, hardware ID: {0:d}, quality ID: ' \
            '{1:d}.'.format(attributes['hardware_id'],
                            attributes['quality_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'])

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
    _dic_ref_temp = {
        1: {
            1: 329.0,
            2: 352.0,
            3: 364.0,
            4: 400.0,
            5: 398.0,
            6: 477.0
        },
        2: {
            1: 329.0,
            2: 352.0,
            3: 364.0,
            4: 409.0
        }
    }
    _dic_factors = {
        1: {
            1: [0.0018, 15.6],
            2: [0.002, 14.0],
            3: [0.0018, 8.7],
            4: [0.002, 10.0],
            5: [0.00125, 3.8],
            6: [0.00159, 8.4]
        },
        2: {
            1: [0.000335, 15.6],
            2: [0.000379, 14.0],
            3: [0.000319, 8.7],
            4: [0.00035, 10.0]
        }
    }
    _dic_piQ = {
        1: {
            1: [1.5, 5.0],
            2: [3.0, 7.5],
            3: [8.0, 30.0],
            4: [12.0, 30.0]
        },
        2: [0.03, 0.1, 0.3, 1.0, 4.0, 20.0]
    }
    _dic_piE = {
        1: [
            1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0
        ],
        2: [
            1.0, 4.0, 12.0, 5.0, 16.0, 5.0, 7.0, 6.0, 8.0, 24.0, 0.5, 13.0,
            34.0, 610.0
        ]
    }
    _msg = ''

    attributes = calculate_hot_spot_temperature(**attributes)

    # Calculate the base hazard rate.
    try:
        _ref_temp = _dic_ref_temp[attributes['subcategory_id']][attributes[
            'insulation_id']]
        _f0 = _dic_factors[attributes['subcategory_id']][attributes[
            'insulation_id']][0]
        _f1 = _dic_factors[attributes['subcategory_id']][attributes[
            'insulation_id']][1]
        attributes['lambda_b'] = _f0 * exp(
            ((attributes['temperature_hot_spot'] + 273.0) / _ref_temp)**_f1)
    except (KeyError, ZeroDivisionError):
        attributes['lambda_b'] = 0.0

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating inductor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Determine the quality factor (piQ).
    try:
        if attributes['subcategory_id'] == 1:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['family_id']][attributes['quality_id'] - 1]
        else:
            attributes['piQ'] = _dic_piQ[attributes['subcategory_id']][
                attributes['quality_id'] - 1]
    except (KeyError, IndexError):
        attributes['piQ'] = 0.0

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'inductor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Determine the environmental factor (piE).
    try:
        attributes['piE'] = _dic_piE[attributes['subcategory_id']][
            attributes['environment_active_id'] - 1]
    except (KeyError, IndexError):
        attributes['piE'] = 0.0

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'inductor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the construction factor (piC).
    if attributes['subcategory_id'] == 2:
        try:
            attributes['piC'] = (2.0 if (attributes['construction_id']) - (1)
                                 else 1.0)
        except IndexError:
            attributes['piC'] = 0.0

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'] * attributes['piE'])
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piC'])

    return attributes, _msg


def overstressed(**attributes):
    """
    Determine whether the inductor is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _reason_num = 1
    _reason = ''

    _harsh = True

    attributes['overstress'] = False

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if attributes['environment_active_id'] in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if attributes['voltage_ratio'] > 0.5:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 50% rated voltage in harsh "
                  u"environment.\n")
            _reason_num += 1
        if attributes['current_ratio'] > 0.6:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating current > 60% rated current in harsh "
                  u"environment.\n")
            _reason_num += 1
        if (attributes['temperature_rated_max'] -
                attributes['temperature_hot_spot'] < 15.0):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating temperature within 15.0C of maximum rated "
                  u"temperature.\n")
            _reason_num += 1
    else:
        if attributes['voltage_ratio'] > 0.9:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 90% rated voltage in mild "
                  u"environment.\n")
            _reason_num += 1
        if attributes['current_ratio'] > 0.9:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating current > 90% rated current in mild "
                  u"environment.\n")
            _reason_num += 1

    attributes['reason'] = _reason

    return attributes


def calculate_hot_spot_temperature(**attributes):
    """
    Calculate the coil or transformer hot spot temperature.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    if (attributes['subcategory_id'] == 2
            and attributes['specification_id'] == 2):
        if attributes['page_number'] in [1, 2, 3, 5, 7, 9, 10, 13, 14]:
            attributes['temperature_rise'] = 15.0
        elif attributes['page_number'] in [4, 6, 8, 11, 12]:
            attributes['temperature_rise'] = 35.0
        else:
            attributes['temperature_rise'] = 0.0

    if attributes['temperature_rise'] == 0.0:
        try:
            attributes['temperature_rise'] = 125.0 * attributes[
                'power_operating'] / attributes['area']
        except ZeroDivisionError:
            attributes['temperature_rise'] = 0.0

    if attributes['temperature_rise'] == 0.0:
        try:
            attributes['temperature_rise'] = 11.5 * attributes[
                'power_operating'] / attributes['weight']**0.6766
        except ZeroDivisionError:
            attributes['temperature_rise'] = 0.0

    if attributes['temperature_rise'] == 0.0:
        try:
            attributes['temperature_rise'] = 2.1 * attributes[
                'power_operating'] / attributes['weight']**0.6766
        except ZeroDivisionError:
            attributes['temperature_rise'] = 0.0

    attributes['temperature_hot_spot'] = (attributes['temperature_active'] +
                                          1.1 * attributes['temperature_rise'])

    return attributes
