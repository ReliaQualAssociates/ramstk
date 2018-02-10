#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.Component.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Component Calculations Module."""

import gettext

from . import (Capacitor, Connection, Crystal, Filter, Fuse, Inductor,
               IntegratedCircuit, Lamp, Meter, Relay, Resistor, Semiconductor,
               Switch)

_ = gettext.gettext


def calculate(**attributes):
    """
    Calculate the hazard rate for a resistor.

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

    if attributes['mult_adj_factor'] <= 0.0:
        _msg = _msg + 'RTK WARNING: Multiplicative adjustment factor is 0.0 ' \
            'when calculating resistor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RTK WARNING: dty cycle is 0.0 when calculating ' \
            'resistor, hardware ID: {0:d}'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RTK WARNING: Quantity is less than 1 when ' \
            'calculating resistor, hardware ID: ' \
            '{0:d}'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (attributes['hazard_rate_active'] +
                                        attributes['add_adj_factor']) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    attributes, _msg = do_calculate_dormant_hazard_rate(**attributes)
    attributes = do_check_overstress(**attributes)

    return attributes, _msg


def do_calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a resistor.

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
        elif attributes['subcategory_id'] == 2:
            attributes, __ = Lamp.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 3:
            attributes, __ = Fuse.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 4:
            attributes, __ = Filter.calculate_217f_part_count(**attributes)

    return attributes, _msg


def do_calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a resistor.

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
        elif attributes['subcategory_id'] == 2:
            attributes, _msg = Lamp.calculate_217f_part_stress(**attributes)
        elif attributes['subcategory_id'] == 3:
            attributes, _msg = Fuse.calculate_217f_part_stress(**attributes)
        elif attributes['subcategory_id'] == 4:
            attributes, _msg = Filter.calculate_217f_part_stress(**attributes)

    return attributes, _msg


def do_calculate_dormant_hazard_rate(**attributes):
    """
    Calculate the dormant hazard rate.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below for integrated
    circuits).

    +-------+--------+--------+-------+-------+-------+-------+
    |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
    |Active |Active  |Active  |Active |Active |Active |Active |
    |to     |to      |to      |to     |to     |to     |to     |
    |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
    |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    +=======+========+========+=======+=======+=======+=======+
    | 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
    +-------+--------+--------+-------+-------+-------+-------+

    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    # First key is the category ID; second key is the active environment ID;
    # third key is the dormant environment ID.
    _dic_hr_dormant = {
        1: {
            1: {
                2: 0.08
            },
            2: {
                2: 0.08
            },
            3: {
                2: 0.08
            },
            4: {
                2: 0.05,
                3: 0.06
            },
            5: {
                2: 0.05,
                3: 0.06
            },
            6: {
                1: 0.06,
                2: 0.04
            },
            7: {
                1: 0.06,
                2: 0.04
            },
            8: {
                1: 0.06,
                2: 0.04
            },
            9: {
                1: 0.06,
                2: 0.04
            },
            10: {
                1: 0.06,
                2: 0.04
            },
            11: {
                2: 0.1,
                4: 0.3
            }
        },
        2: {
            1: {
                2: [0.04, 0.05]
            },
            2: {
                2: [0.04, 0.05]
            },
            3: {
                2: [0.04, 0.05]
            },
            4: {
                2: [0.03, 0.03],
                3: [0.04, 0.05]
            },
            5: {
                2: [0.03, 0.03],
                3: [0.04, 0.05]
            },
            6: {
                1: [0.05, 0.06],
                2: [0.01, 0.02]
            },
            7: {
                1: [0.05, 0.06],
                2: [0.01, 0.02]
            },
            8: {
                1: [0.05, 0.06],
                2: [0.01, 0.02]
            },
            9: {
                1: [0.05, 0.06],
                2: [0.01, 0.02]
            },
            10: {
                1: [0.05, 0.06],
                2: [0.01, 0.02]
            },
            11: {
                2: [0.8, 1.0],
                4: [0.2, 0.2]
            }
        },
        3: {
            1: {
                2: 0.2
            },
            2: {
                2: 0.2
            },
            3: {
                2: 0.2
            },
            4: {
                2: 0.06,
                3: 0.1
            },
            5: {
                2: 0.06,
                3: 0.1
            },
            6: {
                1: 0.06,
                2: 0.2
            },
            7: {
                1: 0.06,
                2: 0.2
            },
            8: {
                1: 0.06,
                2: 0.2
            },
            9: {
                1: 0.06,
                2: 0.2
            },
            10: {
                1: 0.06,
                2: 0.2
            },
            11: {
                2: 1.0,
                4: 0.5
            }
        },
        4: {
            1: {
                2: 0.1
            },
            2: {
                2: 0.1
            },
            3: {
                2: 0.1
            },
            4: {
                2: 0.04,
                3: 0.1
            },
            5: {
                2: 0.04,
                3: 0.1
            },
            6: {
                1: 0.1,
                2: 0.03
            },
            7: {
                1: 0.1,
                2: 0.03
            },
            8: {
                1: 0.1,
                2: 0.03
            },
            9: {
                1: 0.1,
                2: 0.03
            },
            10: {
                1: 0.1,
                2: 0.03
            },
            11: {
                2: 0.4,
                4: 0.2
            }
        },
        5: {
            1: {
                2: 0.2
            },
            2: {
                2: 0.2
            },
            3: {
                2: 0.2
            },
            4: {
                2: 0.3,
                3: 0.3
            },
            5: {
                2: 0.3,
                3: 0.3
            },
            6: {
                1: 0.2,
                2: 0.2
            },
            7: {
                1: 0.2,
                2: 0.2
            },
            8: {
                1: 0.2,
                2: 0.2
            },
            9: {
                1: 0.2,
                2: 0.2
            },
            10: {
                1: 0.2,
                2: 0.2
            },
            11: {
                2: 1.0,
                4: 0.5
            }
        },
        6: {
            1: {
                2: 0.2
            },
            2: {
                2: 0.2
            },
            3: {
                2: 0.2
            },
            4: {
                2: 0.08,
                3: 0.3
            },
            5: {
                2: 0.08,
                3: 0.3
            },
            6: {
                1: 0.2,
                2: 0.04
            },
            7: {
                1: 0.2,
                2: 0.04
            },
            8: {
                1: 0.2,
                2: 0.04
            },
            9: {
                1: 0.2,
                2: 0.04
            },
            10: {
                1: 0.2,
                2: 0.04
            },
            11: {
                2: 0.9,
                4: 0.4
            }
        },
        7: {
            1: {
                2: 0.4
            },
            2: {
                2: 0.4
            },
            3: {
                2: 0.4
            },
            4: {
                2: 0.2,
                3: 0.4
            },
            5: {
                2: 0.2,
                3: 0.4
            },
            6: {
                1: 0.2,
                2: 0.1
            },
            7: {
                1: 0.2,
                2: 0.1
            },
            8: {
                1: 0.2,
                2: 0.1
            },
            9: {
                1: 0.2,
                2: 0.1
            },
            10: {
                1: 0.2,
                2: 0.1
            },
            11: {
                2: 1.0,
                4: 0.8
            }
        },
        8: {
            1: {
                2: 0.005
            },
            2: {
                2: 0.005
            },
            3: {
                2: 0.005
            },
            4: {
                2: 0.003,
                3: 0.008
            },
            5: {
                2: 0.003,
                3: 0.008
            },
            6: {
                1: 0.0005,
                2: 0.003
            },
            7: {
                1: 0.0005,
                2: 0.003
            },
            8: {
                1: 0.0005,
                2: 0.003
            },
            9: {
                1: 0.0005,
                2: 0.003
            },
            10: {
                1: 0.0005,
                2: 0.003
            },
            11: {
                2: 0.03,
                4: 0.02
            }
        }
    }
    _msg = ''

    if attributes['category_id'] == 2:
        try:
            # [1, 2] = diodes, else transistors.
            if attributes['subcategory_id'] in [1, 2]:
                attributes['hazard_rate_dormant'] = \
                    (_dic_hr_dormant[attributes['environment_active_id']]
                     [attributes['environment_dormant_id']][0] *
                     attributes['hazard_rate_active'])
            elif attributes['subcategory_id'] in [3, 4, 5, 6, 7, 8, 9]:
                attributes['hazard_rate_dormant'] = \
                    (_dic_hr_dormant[attributes['environment_active_id']]
                     [attributes['environment_dormant_id']][1] *
                     attributes['hazard_rate_active'])
            else:
                attributes['hazard_rate_dormant'] = 0.0
        except KeyError:
            attributes['hazard_rate_dormant'] = 0.0
            _msg = 'RTK ERROR: Unknown active and/or dormant environment ID. ' \
                'Active ID: {0:d}, Dormant ID: ' \
                '{1:d}'.format(attributes['environment_active_id'],
                               attributes['environment_dormant_id'])

    else:
        try:
            attributes['hazard_rate_dormant'] = \
                (_dic_hr_dormant[attributes['category_id']][
                    attributes['environment_active_id']]
                 [attributes['environment_dormant_id']] *
                 attributes['hazard_rate_active'])
        except KeyError:
            attributes['hazard_rate_dormant'] = 0.0
            _msg = 'RTK ERROR: Unknown active and/or dormant environment ID. ' \
                'Active ID: {0:d}, Dormant ID: ' \
                '{1:d}'.format(attributes['environment_active_id'],
                               attributes['environment_dormant_id'])

    return attributes, _msg


def do_calculate_stress_ratios(**attributes):
    """
    Calculate the stress ratios.

    Calculates the current, power, and voltage stress ratios.
    """
    try:
        attributes['current_ratio'] = attributes[
            'current_operating'] / attributes['current_rated']
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
    _msg = ''

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
