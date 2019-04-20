#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Component.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Reliability Calculations Module."""

import gettext

from ramstk.analyses.data import DORMANT_MULT
from . import (Capacitor, Connection, Crystal, Filter, Fuse, Inductor,
               IntegratedCircuit, Lamp, Meter, Relay, Resistor, Semiconductor,
               Switch)

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a hardware item.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    attributes = do_calculate_stress_ratios(**attributes)

    if attributes['hazard_rate_method_id'] == 1:
        attributes, _msg = do_calculate_217f_part_count(**attributes)
    elif attributes['hazard_rate_method_id'] == 2:
        attributes, _msg = do_calculate_217f_part_stress(**attributes)

    attributes, _msg = do_calculate_dormant_hazard_rate(**attributes)
    attributes = do_check_overstress(**attributes)

    if attributes['mult_adj_factor'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Multiplicative adjustment factor is 0.0 ' \
            'when calculating hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Duty cycle is 0.0 when calculating ' \
            'hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RAMSTK WARNING: Quantity is less than 1 when ' \
            'calculating hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    return attributes, _msg


def do_calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a hardware item.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    if attributes['category_id'] == 1:
        attributes, __ = IntegratedCircuit.calculate_217f_part_count(
            **attributes)
    elif attributes['category_id'] == 2:
        attributes, __ = Semiconductor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 3:
        attributes, __ = Resistor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 4:
        attributes, __ = Capacitor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 5:
        attributes, __ = Inductor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 6:
        attributes, __ = Relay.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 7:
        attributes, __ = Switch.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 8:
        attributes, __ = Connection.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 9:
        attributes, __ = Meter.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 10:
        if attributes['subcategory_id'] == 1:
            attributes, __ = Crystal.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 4:
            attributes, __ = Lamp.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 3:
            attributes, __ = Fuse.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 2:
            attributes, __ = Filter.calculate_217f_part_count(**attributes)

    return attributes, _msg


def do_calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a hardware item.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    if attributes['category_id'] == 1:
        attributes, _msg = IntegratedCircuit.calculate_217f_part_stress(
            **attributes)
    elif attributes['category_id'] == 2:
        attributes, _msg = Semiconductor.calculate_217f_part_stress(
            **attributes)
    elif attributes['category_id'] == 3:
        attributes, _msg = Resistor.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 4:
        attributes, _msg = Capacitor.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 5:
        attributes = Inductor.calculate_hot_spot_temperature(**attributes)
        attributes, _msg = Inductor.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 6:
        attributes, _msg = Relay.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 7:
        attributes, _msg = Switch.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 8:
        attributes, _msg = Connection.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 9:
        attributes, _msg = Meter.calculate_217f_part_stress(**attributes)
    elif attributes['category_id'] == 10:
        if attributes['subcategory_id'] == 1:
            attributes, _msg = Crystal.calculate_217f_part_stress(**attributes)
        elif attributes['subcategory_id'] == 4:
            attributes, _msg = Lamp.calculate_217f_part_stress(**attributes)
        elif attributes['subcategory_id'] == 3:
            attributes, _msg = Fuse.calculate_217f_part_stress(**attributes)
        elif attributes['subcategory_id'] == 2:
            attributes, _msg = Filter.calculate_217f_part_stress(**attributes)

    return attributes, _msg


def do_calculate_dormant_hazard_rate(**attributes):
    """
    Calculate the dormant hazard rate for a hardware item.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.4, Table 6.3.4-1.

    Active environments are:
        1 - 3: Ground
        4 - 5: Naval
        6 - 10: Airborne
        11: Space
        12 - 13: Missile (no conversion factors)

    Dormant environments are:
        1: Airborne
        2: Ground
        3: Naval
        4: Space

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    _msg = ''

    try:
        if attributes['category_id'] == 2:
            # [1, 2] = diodes, else transistors.
            if attributes['subcategory_id'] in [1, 2]:
                attributes['hazard_rate_dormant'] = \
                    (DORMANT_MULT[attributes['category_id']][attributes['environment_active_id']]
                     [attributes['environment_dormant_id']][0] *
                     attributes['hazard_rate_active'])
            elif attributes['subcategory_id'] in [3, 4, 5, 6, 7, 8, 9]:
                attributes['hazard_rate_dormant'] = \
                    (DORMANT_MULT[attributes['category_id']][attributes['environment_active_id']]
                     [attributes['environment_dormant_id']][1] *
                     attributes['hazard_rate_active'])
            else:
                attributes['hazard_rate_dormant'] = 0.0
        else:
            attributes['hazard_rate_dormant'] = \
                    (DORMANT_MULT[attributes['category_id']][attributes['environment_active_id']]
                     [attributes['environment_dormant_id']] *
                     attributes['hazard_rate_active'])
    except KeyError:
        attributes['hazard_rate_dormant'] = 0.0
        _msg = 'RAMSTK ERROR: Unknown active and/or dormant environment ID for ' \
               'hardware item.  Hardware ID: {0:d}, active environment ID: ' \
               '{1:d}, and dormant environment ID: ' \
               '{2:d}.\n'.format(attributes['hardware_id'],
                                 attributes['environment_active_id'],
                                 attributes['environment_dormant_id'])

    return attributes, _msg


def do_calculate_stress_ratios(**attributes):
    """
    Calculate the stress ratios for a hardware item.

    Calculates the current, power, and voltage stress ratios.
    """
    try:
        attributes[
            'current_ratio'] = attributes['current_operating'] / attributes['current_rated']
    except ZeroDivisionError:
        attributes['voltage_ratio'] = 1.0

    try:
        attributes['power_ratio'] = (
            attributes['power_operating'] / attributes['power_rated'])
    except ZeroDivisionError:
        attributes['power_ratio'] = 1.0

    try:
        attributes['voltage_ratio'] = (
            attributes['voltage_ac_operating'] +
            attributes['voltage_dc_operating']) / attributes['voltage_rated']
    except ZeroDivisionError:
        attributes['voltage_ratio'] = 1.0

    return attributes


def do_check_overstress(**attributes):
    """
    Determine whether the hardware item is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: attributes; the keyword argument (hardware attribute) dictionary
             with updated values
    :rtype: dict
    """
    if attributes['category_id'] == 1:
        attributes = IntegratedCircuit.overstressed(**attributes)
    elif attributes['category_id'] == 2:
        attributes = Semiconductor.overstressed(**attributes)
    elif attributes['category_id'] == 3:
        attributes = Resistor.overstressed(**attributes)
    elif attributes['category_id'] == 4:
        attributes = Capacitor.overstressed(**attributes)
    elif attributes['category_id'] == 5:
        attributes = Inductor.overstressed(**attributes)
    elif attributes['category_id'] == 6:
        attributes = Relay.overstressed(**attributes)
    elif attributes['category_id'] == 7:
        attributes = Switch.overstressed(**attributes)
    elif attributes['category_id'] == 8:
        attributes = Connection.overstressed(**attributes)

    return attributes
