# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""milhdbk217f Calculations Class."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Local Imports
from .models import (
    capacitor, connection, crystal, efilter, fuse, inductor,
    integratedcircuit, lamp, meter, relay, resistor, semiconductor, switch
)


# noinspection PyTypeChecker
def _do_calculate_part_count(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MIL-HDBK-217F parts count active hazard rate.

    :param attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID or subcategory ID.
    """
    _part_count = {
        1: integratedcircuit.calculate_part_count,
        2: semiconductor.calculate_part_count,
        3: resistor.calculate_part_count,
        4: capacitor.calculate_part_count,
        5: inductor.calculate_part_count,
        6: relay.calculate_part_count,
        7: switch.calculate_part_count,
        8: connection.calculate_part_count,
        9: meter.calculate_part_count,
        10: {
            1: crystal.calculate_part_count,
            2: efilter.calculate_part_count,
            3: fuse.calculate_part_count,
            4: lamp.calculate_part_count
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
            attributes['category_id'], attributes['subcategory_id'],
            attributes['quality_id'])
    else:
        attributes = semiconductor.get_part_count_quality_factor(attributes)

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piQ'])

    return attributes


# noinspection PyTypeChecker
def _do_calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MIL-HDBK-217F parts stress active hazard rate.

    :param attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID or subcategory ID.
    """
    _functions = {
        1: integratedcircuit.calculate_part_stress,
        2: semiconductor.calculate_part_stress,
        3: resistor.calculate_part_stress,
        4: capacitor.calculate_part_stress,
        5: inductor.calculate_part_stress,
        6: relay.calculate_part_stress,
        7: switch.calculate_part_stress,
        8: connection.calculate_part_stress,
        9: meter.calculate_part_stress,
        10: {
            1: crystal.calculate_part_stress,
            2: efilter.calculate_part_stress,
            3: fuse.calculate_part_stress,
            4: lamp.calculate_part_stress
        }
    }

    if attributes['category_id'] != 6:
        attributes['piE'] = _get_environment_factor(
            attributes['category_id'],
            attributes['environment_active_id'],
            subcategory_id=attributes['subcategory_id'],
            quality_id=attributes['quality_id'])

    if attributes['category_id'] not in [2, 5]:
        attributes['piQ'] = _get_part_stress_quality_factor(
            attributes['category_id'], attributes['subcategory_id'],
            attributes['quality_id'])

    if attributes['category_id'] == 10:
        _part_stress = _functions[attributes['category_id']][
            attributes['subcategory_id']]
    else:
        _part_stress = _functions[attributes['category_id']]

    return _part_stress(**attributes)


def _get_environment_factor(category_id: int,
                            environment_active_id: int,
                            subcategory_id: int = -1,
                            quality_id: int = -1) -> float:
    """Retrieve the MIL-HDBK-217F environment factor (piE) for the component.

    Most component types have a single list of piE factors, but some require
    additional indices to select the correct list of factors.

    :param category_id: the category ID of the component.
    :param environment_active_id: the active environment ID for the
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
        1: integratedcircuit.PI_E,
        2: semiconductor.PI_E,
        3: resistor.PI_E,
        4: capacitor.PI_E,
        5: inductor.PI_E,
        7: switch.PI_E,
        8: connection.PI_E,
        9: meter.PI_E,
        10: {
            1: crystal.PI_E,
            2: efilter.PI_E,
            3: fuse.PI_E,
            4: lamp.PI_E
        }
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


def _get_part_count_quality_factor(category_id: int, subcategory_id: int,
                                   quality_id: int) -> float:
    """Retrieve the MIL-HDBK-217F parts count quality factor (piQ).

    .. note:: Fuses and Lamps have no piQ input.

    .. note:: Semiconductors have a more complicated piQ listing and the
        function to select the correct value is included in the semiconductor
        model file.

    :param category_id: the category ID of the component.
    :param subcategory_id: the subcategory ID of the component.
    :param quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed active
        environment ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {
        1: integratedcircuit.PI_Q,
        3: resistor.PART_COUNT_PI_Q,
        4: capacitor.PART_COUNT_PI_Q,
        5: inductor.PART_COUNT_PI_Q,
        6: relay.PART_COUNT_PI_Q,
        7: switch.PART_COUNT_PI_Q,
        8: connection.PART_COUNT_PI_Q,
        9: meter.PART_COUNT_PI_Q,
        10: {
            1: crystal.PART_COUNT_PI_Q,
            2: efilter.PI_Q
        }
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


def _get_part_stress_quality_factor(category_id: int, subcategory_id: int,
                                    quality_id: int) -> float:
    """Retrieve the MIL-HDBK-217F part stress quality factor (piQ).

    .. note:: Fuses and Lamps have no piQ input.

    :param category_id: the category ID of the component.
    :param subcategory_id: the subcategory ID of the component.
    :param quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed quality ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {
        1: integratedcircuit.PI_Q,
        3: resistor.PART_STRESS_PI_Q,
        4: capacitor.PART_STRESS_PI_Q,
        6: relay.PART_STRESS_PI_Q,
        7: switch.PART_STRESS_PI_Q,
        8: connection.PART_STRESS_PI_Q,
        9: meter.PART_STRESS_PI_Q,
        10: {
            1: crystal.PART_STRESS_PI_Q,
            2: efilter.PI_Q
        },
    }

    if category_id == 1:
        _pi_q = _pi_q_lists[category_id][quality_id - 1]
    elif (category_id == 8
          and subcategory_id in [4, 5]) or (category_id == 7
                                            and subcategory_id == 5):
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]
    elif category_id == 7 and subcategory_id != 5:
        _pi_q = 0.0
    elif category_id == 8 and subcategory_id not in [4, 5]:
        _pi_q = 0.0
    elif category_id == 9 and subcategory_id == 1:
        _pi_q = 0.0
    elif category_id == 10 and subcategory_id in [3, 4]:
        _pi_q = 0.0
    else:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]

    return _pi_q


# noinspection PyTypeChecker
def do_predict_active_hazard_rate(**attributes: Dict[str, Any]) -> float:
    """Calculate the active hazard rate for a hardware item.

    .. attention:: The programmer is responsible for ensuring appropriate
        stress analyses (e.g., voltage ratios) are performed and results
        assigned to the attributes dict prior to calling the MIL-HDBK-217F
        methods.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    :return: attributes['hazard_rate_active']
    :rtype: float
    """
    try:
        if attributes['hazard_rate_method_id'] == 1:
            attributes = _do_calculate_part_count(**attributes)
        elif attributes['hazard_rate_method_id'] == 2:
            attributes = _do_calculate_part_stress(**attributes)

        pub.sendMessage('succeed_predict_reliability', attributes=attributes)

        return attributes['hazard_rate_active']
    except ValueError:
        pub.sendMessage('fail_predict_reliability',
                        error_message=("Failed to predict MIL-HDBK-217F "
                                       "hazard rate for hardware ID {0:d}; "
                                       "one or more inputs has a negative or "
                                       "missing value. Hardware item category "
                                       "ID={1:d}, subcategory ID={2:d}, rated "
                                       "power={3:f}, number of "
                                       "elements={4:d}.").format(
                                           attributes['hardware_id'],
                                           attributes['category_id'],
                                           attributes['subcategory_id'],
                                           attributes['power_rated'],
                                           attributes['n_elements']))
    except ZeroDivisionError:
        pub.sendMessage('fail_predict_reliability',
                        error_message=("Failed to predict MIL-HDBK-217F "
                                       "hazard rate for hardware ID {0:d}; "
                                       "one or more inputs has a value of "
                                       "0.0.  Hardware item category "
                                       "ID={1:d}, subcategory ID={2:d}, "
                                       "operating ac voltage={3:f}, operating "
                                       "DC voltage={4:f}, operating "
                                       "temperature={5:f}, temperature "
                                       "rise={10:f}, rated maximum "
                                       "temperature={6:f}, "
                                       "feature size={7:f}, "
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
