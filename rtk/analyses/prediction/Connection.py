#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.mil_hdbk_217f.Connection.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Connection Calculations Module."""

import gettext

from math import exp

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a connection.

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
            'when calculating connection, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RTK WARNING: dty cycle is 0.0 when calculating ' \
            'connection, hardware ID: {0:d}'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RTK WARNING: Quantity is less than 1 when ' \
            'calculating connection, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    attributes, _msg = calculate_dormant_hazard_rate(**attributes)
    attributes = overstressed(**attributes)

    return attributes, _msg


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a connection.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    # Dictionary containing MIL-HDBK-217FN2 parts count base hazard rates.
    # First key is the subcategory_id, second key is the specification id.  If
    # the connection subcategory is NOT specification dependent, then the
    # second key will be zero.  Current subcategory IDs are:
    #
    #   72. Circular/Rack and Panel/Coaxial
    #   73. PCB Edge
    #   74. IC Socket
    #   75. Plated Through Hole (PTH)
    #   76. Non-PTH
    #
    # These keys return a list of base hazard rates.  The hazard rate to use is
    # selected from the list depending on the active environment.
    _dic_lambda_b = {
        72: {
            1: [
                0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23, 0.34, 0.37,
                0.0054, 0.16, 0.42, 6.8
            ],
            2: [
                0.012, 0.015, 0.13, 0.075, 0.21, 0.06, 0.1, 0.22, 0.32, 0.38,
                0.0061, 0.18, 0.54, 7.3
            ]
        },
        73: [
            0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
            0.0027, 0.078, 0.21, 3.4
        ],
        74: [
            0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021, 0.025,
            0.048, 0.00097, 0.027, 0.070, 1.3
        ],
        75: [
            0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 0.43, 0.85, 1.5, 1.0, 0.027,
            0.53, 1.4, 27.0
        ],
        76: {
            1: [
                0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016, 0.016,
                0.021, 0.042, 0.0013, 0.023, 0.062, 1.1
            ],
            2: [
                0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056, 0.00084,
                0.00084, 0.0011, 0.0022, 0.00007, 0.0013, 0.0034, 0.059
            ],
            3: [
                0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010, 0.0016,
                0.0016, 0.0021, 0.0042, 0.00013, 0.0023, 0.0062, 0.11
            ],
            4: [
                0.000050, 0.000100, 0.000350, 0.000200, 0.000550, 0.000200,
                0.000300, 0.000300, 0.000400, 0.000800, 0.000025, 0.000450,
                0.001200, 0.021000
            ],
            5: [
                0.0000035, 0.000007, 0.000025, 0.000014, 0.000039, 0.000014,
                0.000021, 0.000021, 0.000028, 0.000056, 0.0000018, 0.000031,
                0.000084, 0.0015
            ],
            6: [
                0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048, 0.00072,
                0.00072, 0.00096, 0.0019, 0.00005, 0.0011, 0.0029, 0.050
            ],
            7: [
                0.000069, 0.000138, 0.000483, 0.000276, 0.000759, 0.000276,
                0.000414, 0.000414, 0.000552, 0.001104, 0.000035, 0.000621,
                0.001656, 0.02898
            ]
        }
    }

    # List containing piQ values for parts count method.  The list positions
    # corrspond to the following quality levels:
    #
    #   0. MIL-SPEC
    #   1. Non MIL-SPEC
    #
    # The quality_id attribute is used to select the proper value of piQ.
    _lst_piQ = [1.0, 2.0]

    # Select the base hazard rate.
    try:
        # Select circular/rack and panel or coaxial (72) or which type of
        # single connection (76).
        if attributes['subcategory_id'] in [72, 76]:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']][
                attributes['type_id']]
        else:
            _lst_base_hr = _dic_lambda_b[attributes['subcategory_id']]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1]
    except IndexError:
        attributes['lambda_b'] = 0.0

    # Select the piQ.
    attributes['piQ'] = _lst_piQ[attributes['quality_id'] - 1]

    # Confirm all inputs are within range.  If not, set the message.  The
    # hazard rate will be calculated anyway, but will be zero.
    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating connection, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piQ is 0.0 when calculating ' \
            'connection, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the hazard rate.
    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ'])

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a connection.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # Reference temperature is used to calculate base hazard rate for
    # circular/rack and panel connectors.  Key is insert material ID.
    _dic_ref_temp = {1: 473.0, 2: 423.0, 3: 373.0, 4: 358.0}

    # Factors are used to calculate base hazard rate for circular/rack and
    # panel connectors.  Key is insert material ID (1 - 4) or contact
    # gauge (22 - 12).
    _dic_factors = {
        72: {
            1: [0.2, -1592.0, 5.36],
            2: [0.431, -2073.6, 4.66],
            3: [0.19, -1298.0, 4.25],
            4: [0.77, -1528.8, 4.72],
            12: 0.1,
            16: 0.274,
            20: 0.64,
            22: 0.989
        },
        73: {
            20: 0.64,
            22: 0.989,
            26: 2.1
        }
    }
    _dic_piQ = {
        1: [3.0, 7.0],
        2: [1.0, 3.0, 10.0],
        3: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0],
        4: [0.03, 0.1, 0.3, 1.0, 3.0, 7.0, 20.0],
        5: [0.03, 0.1, 0.3, 1.0, 10.0],
        6: [0.02, 0.1, 0.3, 1.0, 10.0],
        7: [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 6.0, 15.0],
        8: [5.0, 15.0],
        9: [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0],
        10: [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0],
        11: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
        12: [0.001, 0.01, 0.03, 0.03, 0.1, 0.3, 1.0, 1.5, 10.0],
        13: [0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0],
        14: [0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
        15: [3.0, 10.0],
        16: [4.0, 20.0],
        17: [3.0, 10.0],
        18: [5.0, 20.0],
        19: [3.0, 20.0]
    }
    _dic_piE = {
        72: {
            1: [
                1.0, 1.0, 8.0, 5.0, 13.0, 3.0, 5.0, 8.0, 12.0, 19.0, 0.5, 10.0,
                27.0, 490.0
            ],
            2: [
                2.0, 5.0, 21.0, 10.0, 27.0, 12.0, 18.0, 17.0, 25.0, 37.0, 0.8,
                20.0, 54.0, 970.0
            ]
        },
        73: {
            1: [
                1.0, 3.0, 8.0, 5.0, 13.0, 6.0, 11.0, 6.0, 11.0, 19.0, 0.5,
                10.0, 27.0, 490.0
            ],
            2: [
                2.0, 7.0, 17.0, 10.0, 26.0, 14.0, 22.0, 14.0, 22.0, 37.0, 0.8,
                20.0, 54.0, 970.0
            ]
        }
    }
    _lst_piK = [1.0, 1.5, 2.0, 3.0, 4.0]

    _msg = ''

    # Calculate the insert temperature rise.
    try:
        _fo = _dic_factors[attributes['subcategory_id']][attributes[
            'contact_gauge']]
    except KeyError:
        _fo = 1.0
    attributes['temperature_rise'] = (
        _fo * attributes['current_operating']**1.85)

    # Calculate the base hazard rate.
    _contact_temp = (attributes['temperature_active'] +
                     attributes['temperature_rise'] + 273.0)
    if attributes['subcategory_id'] == 72:
        _ref_temp = _dic_ref_temp[attributes['insert_id']]
        _f0 = _dic_factors[attributes['subcategory_id']][attributes[
            'insert_id']][0]
        _f1 = _dic_factors[attributes['subcategory_id']][attributes[
            'insert_id']][1]
        _f2 = _dic_factors[attributes['subcategory_id']][attributes[
            'insert_id']][2]
    elif attributes['subcategory_id'] == 73:
        _ref_temp = 423.0
        _f0 = 0.216
        _f1 = -2073.6
        _f2 = 4.66
    elif attributes['subcategory_id'] == 74:
        _contact_temp = 0.0
        _ref_temp = 1.0
        _f0 = 0.00042
        _f1 = 0.0
        _f2 = 1.0

    attributes['lambda_b'] = _f0 * exp((_f1 / _contact_temp) +
                                       (_contact_temp / _ref_temp)**_f2)

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating connection, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    # Determine the mating/unmating factor.
    if attributes['n_cycles'] <= 0.05:
        attributes['piK'] = _lst_piK[0]
    elif attributes['n_cycles'] > 0.05 and attributes['n_cycles'] <= 0.5:
        attributes['piK'] = _lst_piK[1]
    elif attributes['n_cycles'] > 0.5 and attributes['n_cycles'] <= 5.0:
        attributes['piK'] = _lst_piK[2]
    elif attributes['n_cycles'] > 5.0 and attributes['n_cycles'] <= 50.0:
        attributes['piK'] = _lst_piK[3]
    else:
        attributes['piK'] = _lst_piK[4]

    # Determine active pins factor.
    attributes['piP'] = exp(((attributes['n_active_pins'] - 1) / 10.0)
                            **0.51064)

    # Determine the environmental factor (piE).
    attributes['piE'] = _dic_piE[attributes['subcategory_id']][attributes[
        'quality_id']][attributes['environment_active_id'] - 1]

    if attributes['piE'] <= 0.0:
        _msg = _msg + 'RTK WARNING: piE is 0.0 when calculating ' \
            'connection, hardware ID: {0:d}'.format(attributes['hardware_id'])

    # Calculate the active hazard rate.
    attributes['hazard_rate_active'] = attributes['lambda_b'] * attributes[
        'piK'] * attributes['piP'] * attributes['piE']

    return attributes, _msg


def calculate_dormant_hazard_rate(**attributes):
    """
    Calculate the dormant hazard rate for a connection.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below for connections).

    +-------+--------+--------+-------+-------+-------+-------+
    |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
    |Active |Active  |Active  |Active |Active |Active |Active |
    |to     |to      |to      |to     |to     |to     |to     |
    |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
    |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    +=======+========+========+=======+=======+=======+=======+
    | 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
    +-------+--------+--------+-------+-------+-------+-------+

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _dic_hr_dormant = {
        1: [0.0, 0.005, 0.0, 0.0],
        2: [0.0, 0.005, 0.0, 0.0],
        3: [0.0, 0.005, 0.0, 0.0],
        4: [0.0, 0.003, 0.008, 0.0],
        5: [0.0, 0.003, 0.008, 0.0],
        6: [0.0005, 0.003, 0.0, 0.0],
        7: [0.0005, 0.003, 0.0, 0.0],
        8: [0.0005, 0.003, 0.0, 0.0],
        9: [0.0005, 0.003, 0.0, 0.0],
        10: [0.0005, 0.003, 0.0, 0.0],
        11: [0.0, 0.03, 0.0, 0.02]
    }
    _msg = ''

    try:
        attributes['hazard_rate_dormant'] = \
            (_dic_hr_dormant[attributes['environment_active_id']]
             [attributes['environment_dormant_id'] - 1] *
             attributes['hazard_rate_active'])
    except KeyError:
        attributes['hazard_rate_dormant'] = 0.0
        _msg = 'RTK ERROR: Unknown active and/or dormant environment ID. ' \
               'Active ID: {0:d}, Dormant ID: ' \
               '{1:d}'.format(attributes['environment_active_id'],
                              attributes['environment_dormant_id'])

    return attributes, _msg


def overstressed(**attributes):
    """
    Determine whether the connection is overstressed.

    This determination is based on it's rated values and operating environment.
    Overstress conditions are:

        * Operating voltage > 70% rated voltage (harsh environment)
        * Operating current > 70% rated current (harsh environment)
        * Operating temperature < 25C from rated temperature (harsh environment)
        * Operating voltage > 90% rated voltage (mild environment)
        * Operating current > 90% rated current (mild environment)

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    _reason_num = 1
    _reason = ''

    _harsh = True

    attributes['overstress'] = False
    _voltage_operating = (attributes['voltage_ac_operating'] +
                          attributes['voltage_dc_operating'])

    # Calculate the voltage stress.
    try:
        attributes['voltage_ratio'] = (
            _voltage_operating / attributes['voltage_rated'])
    except ZeroDivisionError:
        attributes['voltage_ratio'] = 1.0

    # Calculate the current stress.
    try:
        attributes['current_ratio'] = (
            attributes['current_operating'] / attributes['current_rated'])
    except ZeroDivisionError:
        attributes['current_ratio'] = 1.0

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if attributes['environment_active_id'] in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if _voltage_operating > 0.70 * attributes['voltage_rated']:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 70% rated voltage in harsh "
                  u"environment.\n")
            _reason_num += 1
        if (attributes['current_operating'] >
                0.70 * attributes['current_rated']):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating current > 70% rated current in harsh "
                  u"environment.\n")
            _reason_num += 1
        if (attributes['temperature_rated_max'] -
                attributes['temperature_active'] <= 25.0):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating temperature within 25.0C of maximum rated "
                  u"temperature.\n")
            _reason_num += 1
    else:
        if _voltage_operating > 0.90 * attributes['voltage_rated']:
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating voltage > 90% rated voltage in mild "
                  u"environment.\n")
            _reason_num += 1
        if (attributes['current_operating'] >
                0.90 * attributes['current_rated']):
            attributes['overstress'] = True
            _reason = _reason + str(_reason_num) + \
                _(u". Operating current > 90% rated current in mild "
                  u"environment.\n")
            _reason_num += 1

    attributes['reason'] = _reason

    return attributes
