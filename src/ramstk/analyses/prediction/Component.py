# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Component.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Reliability Calculations Module."""

# Standard Library Imports
import gettext

# RAMSTK Package Imports
from ramstk.analyses.data import DORMANT_MULT

# RAMSTK Local Imports
from . import (
    Capacitor, Connection, Crystal, Filter, Fuse, Inductor,
    IntegratedCircuit, Lamp, Meter, Relay, Resistor, Semiconductor, Switch,
)

_ = gettext.gettext


def calculate(limits, **attributes):
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
    attributes = do_check_overstress(limits, **attributes)

    if attributes['mult_adj_factor'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Multiplicative adjustment factor is ' \
            '0.0 when calculating hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['duty_cycle'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Duty cycle is 0.0 when calculating ' \
            'hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['quantity'] < 1:
        _msg = _msg + 'RAMSTK WARNING: Quantity is less than 1 when ' \
            'calculating hardware item, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    attributes['hazard_rate_active'] = (
        attributes['hazard_rate_active']
        + attributes['add_adj_factor']
    ) * \
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
    attributes = _get_quality_factor(**attributes)

    if attributes['category_id'] == 1:
        attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
            **attributes, )
    elif attributes['category_id'] == 2:
        attributes, _msg = Semiconductor.calculate_217f_part_count(
            **attributes,
        )
    elif attributes['category_id'] == 3:
        attributes, _msg = Resistor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 4:
        attributes, _msg = Capacitor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 5:
        attributes, _msg = Inductor.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 6:
        attributes, _msg = Relay.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 7:
        attributes, _msg = Switch.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 8:
        attributes, _msg = Connection.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 9:
        attributes, _msg = Meter.calculate_217f_part_count(**attributes)
    elif attributes['category_id'] == 10:
        if attributes['subcategory_id'] == 1:
            attributes, _msg = Crystal.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 4:
            attributes, _msg = Lamp.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 3:
            attributes, _msg = Fuse.calculate_217f_part_count(**attributes)
        elif attributes['subcategory_id'] == 2:
            attributes, _msg = Filter.calculate_217f_part_count(**attributes)

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
    attributes = _get_quality_factor(**attributes)

    if attributes['category_id'] == 1:
        attributes, _msg = IntegratedCircuit.calculate_217f_part_stress(
            **attributes, )
    elif attributes['category_id'] == 2:
        attributes, _msg = Semiconductor.calculate_217f_part_stress(
            **attributes, )
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
                    (
                        DORMANT_MULT[
                            attributes['category_id']
                        ][
                            attributes['environment_active_id']
                        ]
                        [attributes['environment_dormant_id']][0]
                        * attributes['hazard_rate_active']
                    )
            elif attributes['subcategory_id'] in [3, 4, 5, 6, 7, 8, 9]:
                attributes['hazard_rate_dormant'] = \
                    (
                        DORMANT_MULT[
                            attributes['category_id']
                        ][
                            attributes['environment_active_id']
                        ]
                        [attributes['environment_dormant_id']][1]
                        * attributes['hazard_rate_active']
                    )
            else:
                attributes['hazard_rate_dormant'] = 0.0
        else:
            attributes['hazard_rate_dormant'] = \
                (
                    DORMANT_MULT[
                        attributes['category_id']
                    ][
                        attributes['environment_active_id']
                    ]
                    [attributes['environment_dormant_id']]
                    * attributes['hazard_rate_active']
                )
    except KeyError:
        attributes['hazard_rate_dormant'] = 0.0
        _msg = 'RAMSTK ERROR: Unknown active and/or dormant environment ID for ' \
               'hardware item.  Hardware ID: {0:d}, active environment ID: ' \
               '{1:d}, and dormant environment ID: ' \
               '{2:d}.\n'.format(
                   attributes['hardware_id'],
                   attributes['environment_active_id'],
                   attributes['environment_dormant_id'],
               )

    return attributes, _msg


def do_calculate_stress_ratios(**attributes):
    """
    Calculate the stress ratios for a hardware item.

    Calculates the current, power, and voltage stress ratios.
    """
    try:
        attributes['current_ratio'] = attributes[
            'current_operating'
        ] / attributes['current_rated']
    except ZeroDivisionError:
        attributes['current_ratio'] = 1.0

    try:
        attributes['power_ratio'] = (
            attributes['power_operating'] / attributes['power_rated']
        )
    except ZeroDivisionError:
        attributes['power_ratio'] = 1.0

    try:
        attributes['voltage_ratio'] = (
            attributes['voltage_ac_operating'] +
            attributes['voltage_dc_operating']
        ) / attributes['voltage_rated']
    except ZeroDivisionError:
        attributes['voltage_ratio'] = 1.0

    return attributes


def do_check_overstress(limits, **attributes):
    """
    Determine whether the hardware item is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values
    :rtype: dict
    """
    _reason_num = 1
    _overstress_reason = ''

    _harsh = True

    attributes['overstress'] = False

    if attributes['category_id'] in [1, 2]:
        _op_temp = attributes['temperature_junction']
        _limit_temp = attributes['temperature_junction']
        _limit_temp_str = "Junction"
    elif attributes['category_id'] == 5:
        _op_temp = attributes['temperature_active']
        _limit_temp = attributes['temperature_hot_spot']
        _limit_temp_str = "Hot Spot"
    else:
        _op_temp = attributes['temperature_active']
        _limit_temp = attributes['temperature_rated_max']
        _limit_temp_str = "Maximum Rated"

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if attributes['environment_active_id'] in [1, 2, 4, 11]:
        _harsh = False

    (_overstress, _reason) = _do_check_current_stress(
        _harsh,
        limits[attributes['category_id']][0],
        limits[attributes['category_id']][1],
        attributes['current_ratio'],
    )
    if _overstress:
        attributes['overstress'] = attributes['overstress'] or _overstress
        _overstress_reason = _overstress_reason + str(_reason_num) + _reason
        _reason_num += 1

    (_overstress, _reason) = _do_check_power_stress(
        _harsh,
        limits[attributes['category_id']][2],
        limits[attributes['category_id']][3],
        attributes['power_ratio'],
    )
    if _overstress:
        attributes['overstress'] = attributes['overstress'] or _overstress
        _overstress_reason = _overstress_reason + str(_reason_num) + _reason
        _reason_num += 1

    if attributes['category_id'] == 1:
        if attributes['voltage_ratio'] > 1.05:
            _overstress = True
            _overstress_reason = _overstress_reason + str(_reason_num) + _(
                ". Operating voltage > 105% rated voltage.\n", )
        if attributes['voltage_ratio'] < 0.95:
            _overstress = True
            _overstress_reason = _overstress_reason + str(_reason_num) + _(
                ". Operating voltage < 95% rated voltage.\n", )
        attributes['overstress'] = attributes['overstress'] or _overstress
    else:
        (_overstress, _reason) = _do_check_voltage_stress(
            _harsh,
            limits[attributes['category_id']][4],
            limits[attributes['category_id']][5],
            attributes['voltage_ratio'],
        )
        if _overstress:
            attributes['overstress'] = attributes['overstress'] or _overstress
            _overstress_reason = _overstress_reason + str(
                _reason_num, ) + _reason
            _reason_num += 1
        (_overstress, _reason) = _do_check_deltat_stress(
            _harsh,
            limits[attributes['category_id']][6],
            limits[attributes['category_id']][7],
            attributes['temperature_active'],
            _limit_temp,
            _limit_temp_str,
        )
        if _overstress:
            attributes['overstress'] = attributes['overstress'] or _overstress
            _overstress_reason = _overstress_reason + str(
                _reason_num, ) + _reason
            _reason_num += 1

    (_overstress, _reason) = _do_check_maxtemp_stress(
        _harsh,
        limits[attributes['category_id']][8],
        limits[attributes['category_id']][9],
        _op_temp,
        _limit_temp_str,
    )
    if _overstress:
        attributes['overstress'] = attributes['overstress'] or _overstress
        _overstress_reason = _overstress_reason + str(_reason_num) + _reason
        _reason_num += 1

    attributes['reason'] = _overstress_reason

    return attributes


def _do_check_current_stress(harsh, harsh_limit, mild_limit, current_ratio):
    """
    Check the current ratio against the stress limit.

    :param bool harsh: indicates whether environment is harsh or not.
    :param float harsh_limit: the current ratio limit for a harsh environment.
    :param float mild_limit: the current ratio limit for a mild environment.
    :param float current_ratio: the operating current ratio of the component.
    :return: _overstress, _reason
    :rtype: tuple
    """
    if harsh:
        _limit = harsh_limit
        _environ = 'harsh'
    else:
        _limit = mild_limit
        _environ = 'mild'
    _overstress = False
    _reason = ''

    if current_ratio > _limit:
        _overstress = True
        _reason = _(
            ". Operating current > {0:s}% rated current in {1:s} "
            "environment.\n", ).format(str(_limit * 100.0), _environ)

    return _overstress, _reason


def _do_check_deltat_stress(
        harsh,
        harsh_limit,
        mild_limit,
        op_temp,
        limit_temp,
        limit_temp_str,
):
    """
    Check the operating delta temperature against the stress limit.

    :param bool harsh: indicates whether environment is harsh or not.
    :param float harsh_limit: the delta temperature limit for a harsh
        environment.
    :param float mild_limit: the delta temperature limit for a mild
        environment.
    :param float op_temp: the operating temperature of the component.
    :param float limit_temp: the limiting temperature of the component.
    :param str limit_temp_str: the limiting temperature name.
    :return: _overstress, _reason
    :rtype: tuple
    """
    if harsh:
        _limit = harsh_limit
        _environ = 'harsh'
    else:
        _limit = mild_limit
        _environ = 'mild'
    _overstress = False
    _reason = ''

    if (limit_temp - op_temp) <= _limit:
        _overstress = True
        _reason = _(
            ". Operating temperature within {0:s}C of {1:s} "
            "temperature in {2:s} environment."
            "\n", ).format(str(_limit), limit_temp_str, _environ)

    return _overstress, _reason


def _do_check_maxtemp_stress(
        harsh,
        harsh_limit,
        mild_limit,
        op_temp,
        limit_temp_str,
):
    """
    Check the operating temperature against the maximum temperature rating.

    :param bool harsh: indicates whether environment is harsh or not.
    :param float harsh_limit: the delta temperature limit for a harsh
        environment.
    :param float mild_limit: the delta temperature limit for a mild
        environment.
    :param float op_temp: the operating temperature of the component.
    :param float limit_temp: the limiting temperature of the component.
    :param str limit_temp_str: the limiting temperature name.
    :return: _overstress, _reason
    :rtype: tuple
    """
    if harsh:
        _limit = harsh_limit
        _environ = 'harsh'
    else:
        _limit = mild_limit
        _environ = 'mild'
    _overstress = False
    _reason = ''

    if op_temp > _limit:
        _overstress = True
        _reason = _(
            ". Operating temperature > {0:s}C {1:s} temperature limit "
            "in {2:s} environment.\n", ).format(
                str(_limit),
                limit_temp_str,
                _environ,
            )

    return _overstress, _reason


def _do_check_power_stress(harsh, harsh_limit, mild_limit, power_ratio):
    """
    Check the electrical power ratio against the stress limit.

    :param bool harsh: indicates whether environment is harsh or not.
    :param float harsh_limit: the power ratio limit for a harsh environment.
    :param float mild_limit: the power ratio limit for a mild environment.
    :param float power_ratio: the operating power ratio of the component.
    :return: _overstress, _reason
    :rtype: tuple
    """
    if harsh:
        _limit = harsh_limit
        _environ = 'harsh'
    else:
        _limit = mild_limit
        _environ = 'mild'
    _overstress = False
    _reason = ''

    if power_ratio > _limit:
        _overstress = True
        _reason = _(
            ". Operating power > {0:s}% rated power in {1:s} "
            "environment.\n", ).format(str(_limit * 100.0), _environ)

    return _overstress, _reason


def _do_check_voltage_stress(harsh, harsh_limit, mild_limit, voltage_ratio):
    """
    Check the voltage ratio against the stress limit.

    :param bool harsh: indicates whether environment is harsh or not.
    :param float harsh_limit: the voltage ratio limit for a harsh environment.
    :param float mild_limit: the voltage ratio limit for a mild environment.
    :param float voltage_ratio: the operating voltage ratio of the component.
    :return: _overstress, _reason
    :rtype: tuple
    """
    if harsh:
        _limit = harsh_limit
        _environ = 'harsh'
    else:
        _limit = mild_limit
        _environ = 'mild'
    _overstress = False
    _reason = ''

    if voltage_ratio > _limit:
        _overstress = True
        _reason = _(
            ". Operating voltage > {0:s}% rated voltage in {1:s} "
            "environment.\n", ).format(str(_limit * 100.0), _environ)

    return _overstress, _reason


def _get_quality_factor(**attributes):
    """
    Retrieve the quality factor (pi_Q).

    :param dict attributes: the attributes dictionary of the component being
        calculated.
    :return: attributes; the attributes dictionary updated with pi_Q.
    :rtype: dict
    """
    # Dictionaries containing piQ values.
    if attributes['hazard_rate_method_id'] == 1:
        _dic_piQ = {
            1: [0.25, 1.0, 2.0],
            3: [0.030, 0.10, 0.30, 1.0, 3.0, 10.0],
            4: [0.030, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0],
            5: [0.25, 1.0, 10.0],
            6: {
                1: [0.6, 3.0, 9.0],
                2: [0.0, 1.0, 4.0],
            },
            7: {
                1: [1.0, 20.0],
                2: [1.0, 20.0],
                3: [1.0, 50.0],
                4: [1.0, 10.0],
                5: [1.0, 8.4],
            },
            8: [1.0, 2.0],
            9: {
                1: [1.0, 1.0],
                2: [1.0, 3.4],
            },
            10: {
                1: [1.0, 2.1],
                2: [1.0, 2.9],
            },
        }
    if attributes['hazard_rate_method_id'] == 2:
        _dic_piQ = {
            1: [0.25, 1.0, 2.0],
            3: {
                1: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
                2: [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0],
                3: [1.0, 3.0],
                4: [1.0, 3.0],
                5: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
                6: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
                7: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
                8: [1.0, 15.0],
                9: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
                10: [2.5, 5.0],
                11: [2.0, 4.0],
                12: [2.0, 4.0],
                13: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
                14: [2.5, 5.0],
                15: [2.0, 4.0],
            },
            4: {
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
                19: [3.0, 20.0],
            },
            6: {1: [0.1, 0.3, 0.45, 0.6, 1.0, 1.5, 3.0], 2: [1.0, 4.0]},
            7: {5: [1.0, 8.4]},
            8: {4: [1.0, 2.0], 5: [1.0, 1.0, 2.0, 20.0]},
            9: {2: [1.0, 3.4]},
            10: {1: [1.0, 3.4], 2: [1.0, 2.9]},
        }

    # Select the piQ.
    try:
        attributes['piQ'] = _dic_piQ[attributes['category_id']][
            attributes['subcategory_id']
        ][attributes['quality_id'] - 1]
    except (IndexError, KeyError, TypeError):
        try:
            attributes['piQ'] = _dic_piQ[attributes['category_id']][
                attributes['quality_id'] - 1
            ]
        except (IndexError, KeyError):
            attributes['piQ'] = 0.0

    return attributes
