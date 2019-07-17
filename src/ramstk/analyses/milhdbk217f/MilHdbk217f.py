# -*- coding: utf-8 -*-
#
#       ramstk.analyses.MilHdbk217f.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""MilHdbk217f Calculations Class."""

# Third Party Imports
from pubsub import pub

# RAMSTK Local Imports
from .models import (
    Capacitor, Connection, Crystal, Filter, Fuse, Inductor,
    IntegratedCircuit, Lamp, Meter, Relay, Resistor, Semiconductor, Switch
)


def _do_calculate_part_count(**attributes):
    """
    Calculate the MIL-HDBK-217F parts count active hazard rate.

    :param dict attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID or subcategory ID.
    """
    _part_count = {
        1: IntegratedCircuit.calculate_part_count,
        2: Semiconductor.calculate_part_count,
        3: Resistor.calculate_part_count,
        4: Capacitor.calculate_part_count,
        5: Inductor.calculate_part_count,
        6: Relay.calculate_part_count,
        7: Switch.calculate_part_count,
        8: Connection.calculate_part_count,
        9: Meter.calculate_part_count,
        10: {
            1: Crystal.calculate_part_count,
            2: Filter.calculate_part_count,
            3: Fuse.calculate_part_count,
            4: Lamp.calculate_part_count
        }
    }

    if attributes['category_id'] == 2:
        attributes = _part_count[attributes['category_id']](**attributes)
    elif attributes['category_id'] == 10:
        attributes['lambda_b'] = _part_count[attributes['category_id']][
            attributes['subcategory_id']](**attributes)
    else:
        attributes['lambda_b'] = _part_count[attributes['category_id']](
            **attributes)

    if attributes['category_id'] != 2:
        attributes['piQ'] = _get_part_count_quality_factor(
            attributes['category_id'],
            attributes['subcategory_id'],
            attributes['quality_id'],
        )
    else:
        attributes['piQ'] = Semiconductor.get_part_count_quality_factor(
            attributes['subcategory_id'], attributes['quality_id'],
            attributes['type_id'])

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piQ'])

    return attributes


def _do_calculate_part_stress(**attributes):
    """
    Calculate the MIL-HDBK-217F parts stress active hazard rate.

    :param dict attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID or subcategory ID.
    """
    _functions = {
        1: IntegratedCircuit.calculate_part_stress,
        2: Semiconductor.calculate_part_stress,
        3: Resistor.calculate_part_stress,
        4: Capacitor.calculate_part_stress,
        5: Inductor.calculate_part_stress,
        6: Relay.calculate_part_stress,
        7: Switch.calculate_part_stress,
        8: Connection.calculate_part_stress,
        9: Meter.calculate_part_stress,
        10: {
            1: Crystal.calculate_part_stress,
            2: Filter.calculate_part_stress,
            3: Fuse.calculate_part_stress,
            4: Lamp.calculate_part_stress
        },
    }

    if attributes['category_id'] != 6:
        attributes['piE'] = _get_environment_factor(
            attributes['category_id'],
            attributes['environment_active_id'],
            subcategory_id=attributes['subcategory_id'],
            quality_id=attributes['quality_id'],
        )

    if attributes['category_id'] not in [2, 5]:
        attributes['piQ'] = _get_part_stress_quality_factor(
            attributes['category_id'],
            attributes['subcategory_id'],
            attributes['quality_id'],
        )

    if attributes['category_id'] == 10:
        _part_stress = _functions[attributes['category_id']][
            attributes['subcategory_id']]
    else:
        _part_stress = _functions[attributes['category_id']]

    return _part_stress(**attributes)


def _get_environment_factor(
        category_id,
        environment_active_id,
        subcategory_id=None,
        quality_id=None,
):
    """
    Retrieve the MIL-HDBK-217F environment factor (piE) for the component.

    Most component types have a single list of piE factors, but some require
    additional indices to select the correct list of factors.

    :param int category_id: the category ID of the component.
    :param int environment_active_id: the active environment ID for the
        component.
    :keyword int subcategory_id: the subcategory ID of the component.
    :keyword int quality_id: the quality level ID of the component.
    :return: _pi_e; the selected piE value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed active
        environment ID.
    :raise: KeyError if there is no piE list for the passed category ID (or
        subcategory ID, quality ID when appllicable).
    """
    _pi_e_lists = {
        1: IntegratedCircuit.PI_E,
        2: Semiconductor.PI_E,
        3: Resistor.PI_E,
        4: Capacitor.PI_E,
        5: Inductor.PI_E,
        7: Switch.PI_E,
        8: Connection.PI_E,
        9: Meter.PI_E,
        10: {
            1: Crystal.PI_E,
            2: Filter.PI_E,
            3: Fuse.PI_E,
            4: Lamp.PI_E
        },
    }

    if category_id == 8 and subcategory_id in [1, 2]:
        _pi_e = _pi_e_lists[category_id][subcategory_id][quality_id][
            environment_active_id - 1]
    elif category_id in [
            2, 3, 5, 7, 9, 10
    ] or (category_id == 8 and subcategory_id not in [1, 2]):
        _pi_e = _pi_e_lists[category_id][subcategory_id][environment_active_id
                                                         - 1]
    else:
        _pi_e = _pi_e_lists[category_id][environment_active_id - 1]

    return _pi_e


def _get_part_count_quality_factor(category_id, subcategory_id, quality_id):
    """
    Retrieve the MIL-HDBK-217F parts count quality factor (piQ).

    .. note:: Fuses and Lamps have no piQ input.

    .. note:: Semiconductors have a more complicated piQ listing and the
    function to select the correct value is included in the semiconductor model
    file.

    :param int category_id: the category ID of the component.
    :param int subcategory_id: the subcategory ID of the component.
    :param int quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed active
        environment ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {
        1: IntegratedCircuit.PI_Q,
        3: Resistor.PART_COUNT_PI_Q,
        4: Capacitor.PART_COUNT_PI_Q,
        5: Inductor.PART_COUNT_PI_Q,
        6: Relay.PART_COUNT_PI_Q,
        7: Switch.PART_COUNT_PI_Q,
        8: Connection.PART_COUNT_PI_Q,
        9: Meter.PART_COUNT_PI_Q,
        10: {
            1: Crystal.PART_COUNT_PI_Q,
            2: Filter.PI_Q
        },
    }

    if category_id in [6, 7, 9]:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]
    elif category_id == 10 and subcategory_id in [1, 2]:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]
    elif category_id == 10 and subcategory_id in [3, 4]:
        _pi_q = 1.0
    else:
        _pi_q = _pi_q_lists[category_id][quality_id - 1]

    return _pi_q


def _get_part_stress_quality_factor(category_id, subcategory_id, quality_id):
    """
    Retrieve the MIL-HDBK-217F part stress quality factor (piQ).

    .. note:: Fuses and Lamps have no piQ input.

    :param int category_id: the category ID of the component.
    :param int subcategory_id: the subcategory ID of the component.
    :param int quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed quality ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {
        1: IntegratedCircuit.PI_Q,
        3: Resistor.PART_STRESS_PI_Q,
        4: Capacitor.PART_STRESS_PI_Q,
        6: Relay.PART_STRESS_PI_Q,
        7: Switch.PART_STRESS_PI_Q,
        8: Connection.PART_STRESS_PI_Q,
        9: Meter.PART_STRESS_PI_Q,
        10: {
            1: Crystal.PART_STRESS_PI_Q,
            2: Filter.PI_Q
        },
    }

    if category_id == 1:
        _pi_q = _pi_q_lists[category_id][quality_id - 1]
    elif (category_id == 8
          and subcategory_id in [4, 5]) or (category_id == 7
                                            and subcategory_id == 5):
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]
    elif (category_id == 7 and subcategory_id != 5):
        _pi_q = 0.0
    elif (category_id == 8 and subcategory_id not in [4, 5]):
        _pi_q = 0.0
    elif (category_id == 9 and subcategory_id == 1):
        _pi_q = 0.0
    elif (category_id == 10 and subcategory_id in [3, 4]):
        _pi_q = 0.0
    else:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]

    return _pi_q


def do_predict_active_hazard_rate(**attributes):
    """
    Calculate the active hazard rate for a hardware item.

    .. attention:: The programmer is responsible for ensuring appropriate
        stress analyses (e.g., voltage ratios) are performed and results
        assigned to the attributes dict prior to calling the MIL-HDBK-217F
        methods.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    :return: None
    :rtype: None
    """
    try:
        if attributes['hazard_rate_method_id'] == 1:
            attributes = _do_calculate_part_count(**attributes)
        elif attributes['hazard_rate_method_id'] == 2:
            attributes = _do_calculate_part_stress(**attributes)

        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active']
            + attributes['add_adj_factor']) * (
                (attributes['duty_cycle'] / 100.0)
                * attributes['mult_adj_factor'] * attributes['quantity'])

        pub.sendMessage('succeed_predict_reliability', attributes=attributes)
    except ValueError:
        pub.sendMessage('fail_predict_reliability',
                        error_msg=("Failed to predict MIL-HDBK-217F hazard "
                                   "rate for hardware ID {0:d}; one or more "
                                   "inputs has a negative or missing value. "
                                   "Hardware item category ID={1:d}, "
                                   "subcategory ID={2:d}, rated power={3:f}, "
                                   "number of elements={4:d}.").format(
                                       attributes['hardware_id'],
                                       attributes['category_id'],
                                       attributes['subcategory_id'],
                                       attributes['power_rated'],
                                       attributes['n_elements']))
    except ZeroDivisionError:
        pub.sendMessage('fail_predict_reliability',
                        error_msg=("Failed to predict MIL-HDBK-217F hazard "
                                   "rate for hardware ID {0:d}; one or more "
                                   "inputs has a value of 0.0.  Hardware item "
                                   "category ID={1:d}, subcategory ID={2:d}, "
                                   "operating ac voltage={3:f}, operating DC "
                                   "voltage={4:f}, operating "
                                   "temperature={5:f}, temperature "
                                   "rise={10:f}, rated maximum "
                                   "temperature={6:f}, feature size={7:f}, "
                                   "surface area={8:f}, and item "
                                   "weight={9:f}.").format(
                                       attributes['hardware_id'],
                                       attributes['category_id'],
                                       attributes['subcategory_id'],
                                       attributes['voltage_ac_operating'],
                                       attributes['voltage_dc_operating'],
                                       attributes['temperature_active'],
                                       attributes['temperature_rated_max'],
                                       attributes['feature_size'],
                                       attributes['area'],
                                       attributes['weight'],
                                       attributes['temperature_rise']))
