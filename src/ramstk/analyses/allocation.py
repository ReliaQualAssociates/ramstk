# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Allocation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Allocation Module."""

# Standard Library Imports
from math import exp, log
from typing import Any, Dict

# Third Party Imports
from pubsub import pub


def _calculate_agree_apportionment(
        parent_goal: float, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an AGREE apportionment of a reliability requirement.

    .. note:: the AGREE method uses MTBF as the parent goal.

    :param parent_goal: the reliability goal of the parent hardware
        item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
    values.
    :rtype: dict
    """
    _time_i: Any = float(attributes['mission_time']) * float(
        attributes['duty_cycle']) / 100.0
    _weight_factor: Any = float(attributes['weight_factor'])
    _n_sub_systems: Any = int(attributes['n_sub_systems'])
    _n_sub_elements: Any = int(attributes['n_sub_elements'])
    try:
        _mtbf_alloc: Any = ((_n_sub_systems * _weight_factor * _time_i) /
                            (_n_sub_elements * (-log(float(parent_goal)))))
        _hazard_rate_alloc: Any = 1.0 / _mtbf_alloc
        _reliability_alloc: Any = exp(-1.0 * _hazard_rate_alloc * _time_i)

        attributes['mtbf_alloc'] = _mtbf_alloc
        attributes['hazard_rate_alloc'] = _hazard_rate_alloc
        attributes['reliability_alloc'] = _reliability_alloc
    except ValueError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_message=("Failed to apportion reliability using the "
                           "AGREE method; zero or negative value "
                           "passed for parent hardware item's goal.  "
                           "Parent goal is {0:f}.").format(parent_goal))
    except ZeroDivisionError:
        pub.sendMessage('fail_allocate_reliability',
                        error_message=("Failed to apportion reliability using "
                                       "the AGREE method; one or more inputs "
                                       "had a value of 0.0.  Subsystem "
                                       "mission time={0:f}, weight "
                                       "factor={1:f}, # of subsystems={2:d}, "
                                       "# of subelements={3:d}.").format(
                                           _time_i, _weight_factor,
                                           _n_sub_systems, _n_sub_elements))

    return attributes


def _calculate_arinc_apportionment(
        parent_goal: float, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an ARINC apportionment of the reliability requirement.

    :param parent_goal: the reliability goal of the parent hardware
        item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    """
    _mission_time: Any = float(attributes['mission_time'])
    _weight_factor: Any = float(attributes['weight_factor'])
    try:
        _hazard_rate_alloc: Any = _weight_factor * float(parent_goal)
        _mtbf_alloc: Any = 1.0 / _hazard_rate_alloc
        _reliability_alloc: Any = exp(-1.0 * _hazard_rate_alloc
                                      * _mission_time)
    except ZeroDivisionError:
        _mtbf_alloc = _hazard_rate_alloc = _reliability_alloc = 0.0
        pub.sendMessage('fail_allocate_reliability',
                        error_message=("Failed to apportion reliability using "
                                       "the ARINC method; one or more inputs "
                                       "had a value of 0.0. Weight "
                                       "factor={0:f} and parent "
                                       "goal={1:f}.").format(
                                           _weight_factor, parent_goal))

    attributes['mtbf_alloc'] = _mtbf_alloc
    attributes['hazard_rate_alloc'] = _hazard_rate_alloc
    attributes['reliability_alloc'] = _reliability_alloc

    return attributes


def _calculate_equal_apportionment(
        parent_goal: float, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an equal apportionment of the reliability goal.

    :param parent_goal: the reliability goal of the parent hardware
        item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    """
    _mission_time: Any = float(attributes['mission_time'])
    _weight_factor: Any = float(attributes['weight_factor'])
    try:
        _reliability_alloc: Any = float(parent_goal)**_weight_factor
        _hazard_rate_alloc: Any = (-1.0 * log(_reliability_alloc)
                                   / _mission_time)
        _mtbf_alloc: Any = 1.0 / _hazard_rate_alloc

        attributes['hazard_rate_alloc'] = _hazard_rate_alloc
        attributes['mtbf_alloc'] = _mtbf_alloc
        attributes['reliability_alloc'] = _reliability_alloc
    except TypeError:
        if parent_goal < 0.0:
            pub.sendMessage(
                'fail_allocate_reliability',
                error_message=(
                    "Failed to apportion reliability using the "
                    "equal method; a negative or zero value passed for "
                    "parent hardware item's goal.  Parent goal is "
                    "{0:f}.").format(parent_goal))
        else:
            raise
    except ValueError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_message=("Failed to apportion reliability using the "
                           "equal method; a negative or zero value passed for "
                           "parent hardware item's goal.  Parent goal is "
                           "{0:f}.").format(parent_goal))
    except ZeroDivisionError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_message=("Failed to apportion reliability using the "
                           "equal method; one or more inputs had a "
                           "value of 0.0. Mission time={0:f} and "
                           "weight factor={1:f}.").format(
                               _mission_time, _weight_factor))

    return attributes


def _calculate_foo_apportionment(parent_goal: float, cum_weight: int,
                                 attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a feasibility of objectives (FOO) apportionment.

    :param parent_goal: the failure rate requirement to allocate.
    :param cum_weight: the cumulative weight factor for all subordinate
        assemblies.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    :rtype: dict
    """
    _intricacy: Any = int(attributes['int_factor'])
    _state_of_art: Any = int(attributes['soa_factor'])
    _operating_time: Any = int(attributes['op_time_factor'])
    _environment: Any = int(attributes['env_factor'])
    _mission_time: Any = float(attributes['mission_time'])

    try:
        _weight_factor: Any = (_intricacy * _state_of_art * _operating_time
                               * _environment)
        _percent_weight_factor: Any = (_weight_factor / int(cum_weight))

        _hazard_rate_alloc: Any = _percent_weight_factor * parent_goal
        _mtbf_alloc: Any = 1.0 / _hazard_rate_alloc
        _reliability_alloc: Any = exp(-1.0 * _hazard_rate_alloc
                                      * _mission_time)

        attributes['weight_factor'] = _weight_factor
        attributes['percent_weight_factor'] = _percent_weight_factor
        attributes['hazard_rate_alloc'] = _hazard_rate_alloc
        attributes['mtbf_alloc'] = _mtbf_alloc
        attributes['reliability_alloc'] = _reliability_alloc
    except ZeroDivisionError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_message=("Failed to apportion reliability using the "
                           "Feasibility of Objectives method; one or "
                           "more inputs had a value of 0.0. "
                           "Intricacy factor={0:d}, state of the art "
                           "factor={1:d}, operating time "
                           "factor={2:d}, environment factor={3:d}, "
                           "cumulative weight={4:d}, parent "
                           "goal={5:f}.").format(_intricacy, _state_of_art,
                                                 _operating_time, _environment,
                                                 cum_weight, parent_goal))

    return attributes


def _from_hazard_rate_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MTBF and reliability goals given the hazard rate goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes['mission_time'])
    _hazard_rate_goal: Any = float(attributes['hazard_rate_goal'])
    try:
        _mtbf_goal: Any = 1.0 / _hazard_rate_goal
        _reliability_goal: Any = exp(-1.0 * _mission_time / _mtbf_goal)
    except ZeroDivisionError:
        _mtbf_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage(
            'fail_calculate_allocation_goal',
            error_message=(
                "Failed to calculate the MTBF and "
                "reliability goals given the hazard rate "
                "goal.  Hazard rate goal={0:f}.").format(_hazard_rate_goal))

    attributes['mtbf_goal'] = _mtbf_goal
    attributes['reliability_goal'] = _reliability_goal

    return attributes


def _from_mtbf_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the hazard rate and reliability goals given the MTBF goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes['mission_time'])
    _mtbf_goal: Any = float(attributes['mtbf_goal'])
    try:
        _hazard_rate_goal: Any = 1.0 / _mtbf_goal
        _reliability_goal: Any = exp(-1.0 * _mission_time / _mtbf_goal)
    except ZeroDivisionError:
        _hazard_rate_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage(
            'fail_calculate_allocation_goal',
            error_message=("Failed to calculate the hazard rate and "
                           "reliability goals given the MTBF goal.  "
                           "MTBF goal={0:f}.").format(_mtbf_goal))

    attributes['hazard_rate_goal'] = _hazard_rate_goal
    attributes['reliability_goal'] = _reliability_goal

    return attributes


def _from_reliability_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MTBF and hazard rate goals given the reliability goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
        values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes['mission_time'])
    _reliability_goal: Any = float(attributes['reliability_goal'])
    try:
        _mtbf_goal: Any = (-1.0 * _mission_time / log(_reliability_goal))
        _hazard_rate_goal: Any = 1.0 / _mtbf_goal
    except ValueError:
        _mtbf_goal = 0.0
        _hazard_rate_goal = 0.0
        pub.sendMessage(
            'fail_calculate_allocation_goal',
            error_message=(
                "Failed to calculate the MTBF and "
                "hazard rate goals given the reliability "
                "goal.  Reliability goal={0:f}.").format(_reliability_goal))

    attributes['hazard_rate_goal'] = _hazard_rate_goal
    attributes['mtbf_goal'] = _mtbf_goal

    return attributes


def do_allocate_reliability(parent_goal: float, cumulative_weight: int,
                            **attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the reliability allocation.

    :param parent_goal: the parent assembly's reliability goal.
    :param cumulative_weight: the cumulative weighting of all child assemblies.
        Used for feasibility of objectives method only.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes['allocation_method_id'] == 1:
        attributes = _calculate_equal_apportionment(parent_goal, attributes)
    elif attributes['allocation_method_id'] == 2:
        attributes = _calculate_agree_apportionment(parent_goal, attributes)
    elif attributes['allocation_method_id'] == 3:
        attributes = _calculate_arinc_apportionment(parent_goal, attributes)
    elif attributes['allocation_method_id'] == 4:
        attributes = _calculate_foo_apportionment(parent_goal,
                                                  cumulative_weight,
                                                  attributes)
    else:
        _hazard_rate_alloc: Any = 0.0
        _mtbf_alloc: Any = 0.0
        _reliability_alloc: Any = 1.0
        attributes['hazard_rate_alloc'] = _hazard_rate_alloc
        attributes['mtbf_alloc'] = _mtbf_alloc
        attributes['reliability_alloc'] = _reliability_alloc

    pub.sendMessage('succeed_allocate_reliability', attributes=attributes)

    return attributes


def do_calculate_goals(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the other two reliability metrics from the third.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes['goal_measure_id'] == 1:  # Reliability goal
        attributes = _from_reliability_goal(attributes)
    elif attributes['goal_measure_id'] == 2:  # Hazard rate goal
        attributes = _from_hazard_rate_goal(attributes)
    elif attributes['goal_measure_id'] == 3:  # MTBF goal
        attributes = _from_mtbf_goal(attributes)
    else:
        _hazard_rate_goal: Any = 0.0
        _mtbf_goal: Any = 0.0
        _reliability_goal: Any = 1.0
        attributes['hazard_rate_goal'] = _hazard_rate_goal
        attributes['mtbf_goal'] = _mtbf_goal
        attributes['reliability_goal'] = _reliability_goal

    pub.sendMessage('succeed_calculate_allocation_goals',
                    attributes=attributes)

    return attributes


def get_allocation_goal(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve the reliability goal for the hardware item.

    Used to select the goal for the parent hardware item prior to calling
    the do_allocate_reliability() method.

    :param attributes: the selected item's Allocation attributes dict.
    :return: _goal
    :rtype: float
    :raise: KeyError if the passed attributes dict doesn't contain the
        allocation_method_id, hazard_rate_goal, and/or reliability_goal key.
    """
    if attributes['allocation_method_id'] in [2, 4]:  # ARINC or FOO.
        _goal = attributes['hazard_rate_goal']
    else:
        _goal = attributes['reliability_goal']

    return _goal
