# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Allocation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Allocation Module."""

# Standard Library Imports
from math import exp, log

# Third Party Imports
from pubsub import pub


def _calculate_agree_apportionment(mission_time, duty_cycle, weight_factor,
                                   n_sub_systems, n_sub_elements, parent_goal):
    """
    Perform an AGREE apportionment of a reliability requirement.

    .. note:: the AGREE method uses MTBF as the parent goal.

    :param float mission_time: the mission time for the entire system.
    :param float duty_cycle: the duty cycle of the sub-system currently being
        allocated.
    :param float weight_factor: the importance factor for the sub-system
        currently being allocated.
    :param int n_sub_systems: the total number of sub-elements in all the
        sub-systems comprising the hardware item to be allocated.
    :param int n_sub_elements: the number of sub-elements in the sub-system
        currently being allocated.
    :param float parent_goal: the reliability goal of the parent hardware
        item.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    """
    try:
        _time_i = mission_time * duty_cycle / 100.0

        _mtbf_alloc = ((n_sub_systems * weight_factor * _time_i) /
                       (n_sub_elements * (-log(parent_goal))))
        _hazard_rate_alloc = 1.0 / _mtbf_alloc
        _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time, )

        return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc
    except ValueError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_msg=("Failed to apportion reliability using the "
                       "AGREE method; zero or negative value "
                       "passed for parent hardware item's goal.  "
                       "Parent goal is {0:f}.").format(parent_goal))
    except ZeroDivisionError:
        pub.sendMessage('fail_allocate_reliability',
                        error_msg=("Failed to apportion reliability using the "
                                   "AGREE method; one or more inputs had a "
                                   "value of 0.0. Mission time={0:f}, duty "
                                   "cycle={1:f}, weight factor={2:f}, # of "
                                   "subsystems={3:d}, # of "
                                   "subelements={4:d}.").format(
                                       mission_time, duty_cycle, weight_factor,
                                       n_sub_systems, n_sub_elements))


def _calculate_arinc_apportionment(mission_time, weight_factor, parent_goal):
    """
    Perform an ARINC apportionment of the reliability requirement.

    :param float mission_time: the mission time of the system.
    :param float weight_factor: the ratio of the hardware item's current hazard
        rate and the current system hazard rate.
    :param float parent_goal: the goal hazard rate of the parent hardware
        item.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    """
    print(mission_time, weight_factor, parent_goal)
    try:
        _hazard_rate_alloc = weight_factor * parent_goal
        _mtbf_alloc = 1.0 / _hazard_rate_alloc
        _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time)

        return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc
    except ZeroDivisionError:
        pub.sendMessage('fail_allocate_reliability',
                        error_msg=("Failed to apportion reliability using the "
                                   "ARINC method; one or more inputs had a "
                                   "value of 0.0. Weight factor={0:f} and "
                                   "parent goal={1:f}.").format(
                                       weight_factor, parent_goal))


def _calculate_equal_apportionment(mission_time, weight_factor, parent_goal):
    """
    Perform an equal apportionment of the reliability goal.

    :param float weight_factor: the inverse of the number of child hardware
        items to allocate the goal.
    :param float parent_goal: the reliability goal of the parent hardware
        item.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    """
    try:
        _reliability_alloc = parent_goal**weight_factor
        _hazard_rate_alloc = (-1.0 * log(_reliability_alloc) / mission_time)
        _mtbf_alloc = 1.0 / _hazard_rate_alloc

        return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc
    except TypeError:
        if parent_goal < 0.0:
            pub.sendMessage(
                'fail_allocate_reliability',
                error_msg=("Failed to apportion reliability using the "
                           "equal method; a negative or zero value passed for "
                           "parent hardware item's goal.  Parent goal is "
                           "{0:f}.").format(parent_goal))
        else:
            raise
    except ValueError:
        pub.sendMessage(
            'fail_allocate_reliability',
            error_msg=("Failed to apportion reliability using the "
                       "equal method; a negative or zero value passed for "
                       "parent hardware item's goal.  Parent goal is "
                       "{0:f}.").format(parent_goal))
    except ZeroDivisionError:
        pub.sendMessage('fail_allocate_reliability',
                        error_msg=("Failed to apportion reliability using the "
                                   "equal method; one or more inputs had a "
                                   "value of 0.0. Mission time={0:f} and "
                                   "weight factor={1:f}.").format(
                                       mission_time, weight_factor))


def _calculate_foo_apportionment(factors, mission_time, cum_weight,
                                 parent_goal):
    """
    Perform a feasibility of objectives (FOO) apportionment.

    :param int cum_weight: the cumulative weight factor for all subordinate
        assemblies.
    :param float parent_goal: the failure rate requirement to allocate.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc,
        _weight_factor, _percent_weight_factor); the allocated values for each
        reliability measure and the weighting factors.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    """
    try:
        _weight_factor = (factors['intricacy'] * factors['state_of_art']
                          * factors['operating_time'] * factors['environment'])
        _percent_weight_factor = (float(_weight_factor) / float(cum_weight))

        _hazard_rate_alloc = _percent_weight_factor * parent_goal
        _mtbf_alloc = 1.0 / _hazard_rate_alloc
        _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time)

        return (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc,
                _weight_factor, _percent_weight_factor)
    except ZeroDivisionError:
        pub.sendMessage('fail_allocate_reliability',
                        error_msg=("Failed to apportion reliability using the "
                                   "Feasibility of Objectives method; one or "
                                   "more inputs had a value of 0.0. "
                                   "Intricacy factor={0:d}, state of the art "
                                   "factor={1:d}, operating time "
                                   "factor={2:d}, environment factor={3:d}, "
                                   "cumulative weight={4:d}, parent "
                                   "goal={5:f}.").format(
                                       factors['intricacy'],
                                       factors['state_of_art'],
                                       factors['operating_time'],
                                       factors['environment'], cum_weight,
                                       parent_goal))


def _from_hazard_rate_goal(mission_time, hazard_rate_goal):
    """
    Calculate the MTBF and reliability goals given the hazard rate goal.

    :param float mission_time: the mission time of the hardware item.
    :param float hazard_rate_goal: the hazard rate goal for the hardware item.
    :return: _mtbf_goal, _reliability_goal; the calculate dMTBF and reliability
        goals.
    :rtype: tuple
    """
    try:
        _mtbf_goal = 1.0 / hazard_rate_goal
        _reliability_goal = exp(-1.0 * mission_time / _mtbf_goal)
    except ZeroDivisionError:
        _mtbf_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage(
            'fail_calculate_allocation_goal',
            error_msg=(
                "Failed to calculate the MTBF and "
                "reliability goals given the hazard rate "
                "goal.  Hazard rate goal={0:f}.").format(hazard_rate_goal))

    return _mtbf_goal, _reliability_goal


def _from_mtbf_goal(mission_time, mtbf_goal):
    """
    Calculate the hazard rate and reliability goals given the MTBF goal.

    :param float mission_time: the mission time of the hardware item.
    :param float mtbf_goal: the MTBF goal for the hardware item.
    :return: _hazard_rate_goal, _reliability_goal; the calculated hazard rate
        and reliability goals.
    :rtype: tuple
    """
    try:
        _hazard_rate_goal = 1.0 / mtbf_goal
        _reliability_goal = exp(-1.0 * mission_time / mtbf_goal)
    except ZeroDivisionError:
        _hazard_rate_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage('fail_calculate_allocation_goal',
                        error_msg=("Failed to calculate the hazard rate and "
                                   "reliability goals given the MTBF goal.  "
                                   "MTBF goal={0:f}.").format(mtbf_goal))

    return _hazard_rate_goal, _reliability_goal


def _from_reliability_goal(mission_time, reliability_goal):
    """
    Calculate the MTBF and hazard rate goals given the reliability goal.

    :param float mission_time: the mission time of the hardware item.
    :param float reliability_goal: the reliability goal for the hardware item.
    :return: _mtbf_goal, _hazard_rate_goal; the calculated MTBF and hazard rate
        goals.
    :rtype: tuple
    """
    try:
        _mtbf_goal = (-1.0 * mission_time / log(reliability_goal))
        _hazard_rate_goal = 1.0 / _mtbf_goal
    except ValueError:
        _mtbf_goal = 0.0
        _hazard_rate_goal = 0.0
        pub.sendMessage(
            'fail_calculate_allocation_goal',
            error_msg=(
                "Failed to calculate the MTBF and "
                "hazard rate goals given the reliability "
                "goal.  Reliability goal={0:f}.").format(reliability_goal))

    return _mtbf_goal, _hazard_rate_goal


def do_allocate_reliability(parent_goal, cumulative_weight, **attributes):
    """
    Calculate the reliability allocation.

    :param float parent_goal: the parent assembly's reliability goal.
    :param cumulative_weight: the cumulative weighting of all child assemblies.
        Used for feasibility of objectives method only.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes['allocation_method_id'] == 1:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_agree_apportionment(
             attributes['mission_time'], attributes['duty_cycle'],
             attributes['weight_factor'], attributes['n_sub_systems'],
             attributes['n_sub_elements'], parent_goal)
    elif attributes['allocation_method_id'] == 2:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_arinc_apportionment(
             attributes['mission_time'], attributes['weight_factor'],
             parent_goal)
    elif attributes['allocation_method_id'] == 3:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_equal_apportionment(
             attributes['mission_time'], attributes['weight_factor'],
             parent_goal)
    elif attributes['allocation_method_id'] == 4:
        _factors = {
            'intricacy': attributes['int_factor'],
            'state_of_art': attributes['soa_factor'],
            'operating_time': attributes['op_time_factor'],
            'environment': attributes['env_factor']
        }
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc'], attributes['weight_factor'],
         attributes['_percent_weight_factor']) = _calculate_foo_apportionment(
             _factors, attributes['mission_time'], cumulative_weight,
             parent_goal)
    else:
        attributes['hazard_rate_alloc'] = 0.0
        attributes['mtbf_alloc'] = 0.0
        attributes['reliability_alloc'] = 1.0

    pub.sendMessage('succeed_allocate_reliability', attributes=attributes)


def do_calculate_goals(**attributes):
    """
    Calculate the other two reliability metrics from the third.

    :param dict attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes['goal_measure_id'] == 1:  # Reliability goal
        (attributes['mtbf_goal'],
         attributes['hazard_rate_goal']) = _from_reliability_goal(
             attributes['mission_time'], attributes['reliability_goal'])
    elif attributes['goal_measure_id'] == 2:  # Hazard rate goal
        (attributes['mtbf_goal'],
         attributes['reliability_goal']) = _from_hazard_rate_goal(
             attributes['mission_time'], attributes['hazard_rate_goal'])
    elif attributes['goal_measure_id'] == 3:  # MTBF goal
        (attributes['hazard_rate_goal'],
         attributes['reliability_goal']) = _from_mtbf_goal(
             attributes['mission_time'], attributes['mtbf_goal'])
    else:
        attributes['hazard_rate_goal'] = 0.0
        attributes['mtbf_goal'] = 0.0
        attributes['reliability_goal'] = 1.0

    return attributes


def get_allocation_goal(**attributes):
    """
    Retrieve the reliability goal for the hardware item.

    Used to select the goal for the parent hardware item prior to calling
    the do_allocate_reliability() method.

    :param dict attributes: the selected item's Allocation attributes dict.
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
