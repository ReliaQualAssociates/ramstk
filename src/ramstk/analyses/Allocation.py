# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Allocation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Allocation Module."""

# Standard Library Imports
from math import exp, log


def _calculate_agree_apportionment(mission_time, duty_cycle, weight_factor,
                                   n_sub_systems, n_sub_elements, parent_goal):
    """
    Perform an AGREE apportionment of a reliability requirement.

    :param int n_sub_systems: the number of immediate children comprising the
        parent hardware item.
    :param float parent_goal: the reliability goal of the parent hardware
        item.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    :raise: ValueError if passed a negative value for the parent goal.
    :raise: ZeroDivisionError if passed n_sub_elements=0.0
    """
    _time_i = mission_time * duty_cycle / 100.0

    _mtbf_alloc = ((n_sub_systems * weight_factor * _time_i) /
                   (-1.0 * n_sub_elements * log(parent_goal)))
    _hazard_rate_alloc = 1.0 / _mtbf_alloc
    _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time, )

    return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc


def _calculate_arinc_apportionment(mission_time, system_hr, parent_goal,
                                   hazard_rate):
    """
    Perform an ARINC apportionment of the reliability requirement.

    :param float system_hr: the current system hazard rate.
    :param float parent_goal: the goal hazard rate of the parent hardware
        item.
    :param float hazard_rate: the current (historic) hazard rate of this
        hardware item.
    :param float mission_time: the mission time of the system.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for any argument.
    :raise: ZeroDivisionError if passed a system hazard rate = 0.0.
    """
    _weight_factor = hazard_rate / system_hr

    _hazard_rate_alloc = _weight_factor * parent_goal
    _mtbf_alloc = 1.0 / _hazard_rate_alloc
    _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time)

    return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc


def _calculate_equal_apportionment(mission_time, n_children, parent_goal):
    """
    Perform an equal apportionment of the reliability goal.

    :param int n_children: the number of immediate children comprising the
        parent hardware item.
    :param float parent_goal: the reliability goal of the parent hardware
        item.
    :return: (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc); the
        allocated values for each reliability measure.
    :rtype: tuple
    :raise: TypeError if passed a string for mission time or parent goal or a
        negative value for the parent goal.
    :raise: ZeroDivisionError if passed n_children or mission_time equal to 0.
    """
    _weight_i = 1.0 / float(n_children)

    _reliability_alloc = parent_goal**_weight_i
    _hazard_rate_alloc = (-1.0 * log(_reliability_alloc) / mission_time)
    _mtbf_alloc = 1.0 / _hazard_rate_alloc

    return _mtbf_alloc, _hazard_rate_alloc, _reliability_alloc


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
    :raise: ZeroDivisionError if passed a cumulative weight=0.0.
    """
    # TODO: Add range check on input factors (1 - 10) in RAMSTKAllocation.foo_apportionment().
    _weight_factor = (factors['intricacy'] * factors['state_of_art']
                      * factors['operating_time'] * factors['environment'])
    _percent_weight_factor = (float(_weight_factor) / float(cum_weight))

    _hazard_rate_alloc = _percent_weight_factor * parent_goal
    _mtbf_alloc = 1.0 / _hazard_rate_alloc
    _reliability_alloc = exp(-1.0 * _hazard_rate_alloc * mission_time)

    return (_mtbf_alloc, _hazard_rate_alloc, _reliability_alloc,
            _weight_factor, _percent_weight_factor)


def do_calculate_allocation(parent_goal, cumulative_weight, **attributes):
    """
    Calculate the reliability allocation.

    :param float parent_goal: the parent assembly's reliability goal.
    :param cumulative_weight: the cumulative weighting of all child assemblies.
        Used for feasibility of objectives method only.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes['method_id'] == 1:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_agree_apportionment(
             attributes['mission_time'], attributes['duty_cycle'],
             attributes['weight_factor'], attributes['n_sub_systems'],
             attributes['n_sub_elements'], parent_goal)
    elif attributes['method_id'] == 2:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_arinc_apportionment(
             attributes['mission_time'], attributes['system_hr'], parent_goal,
             attributes['hazard_rate'])
    elif attributes['method_id'] == 3:
        (attributes['mtbf_alloc'], attributes['hazard_rate_alloc'],
         attributes['reliability_alloc']) = _calculate_equal_apportionment(
             attributes['mission_time'], attributes['n_sub_systems'],
             parent_goal)
    elif attributes['method_id'] == 4:
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

    return attributes


def do_calculate_goals(**attributes):
    """
    Calculate the other two reliability metrics from the third.

    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    :raise: ValueError if passed a negative reliability goal.
    :raise: ZeroDivisionError if passed an MTBF goal=0.0 or hazard rate
        goal=0.0.
    """
    if attributes['goal_measure_id'] == 1:  # Reliability goal
        attributes['mtbf_goal'] = (-1.0 * attributes['mission_time']
                                   / log(attributes['reliability_goal']))
        attributes['hazard_rate_goal'] = 1.0 / attributes['mtbf_goal']

    elif attributes['goal_measure_id'] == 2:  # Hazard rate goal
        attributes['mtbf_goal'] = 1.0 / attributes['hazard_rate_goal']
        attributes['reliability_goal'] = exp(-1.0 * attributes['mission_time']
                                             / attributes['mtbf_goal'])

    elif attributes['goal_measure_id'] == 3:  # MTBF goal
        attributes['hazard_rate_goal'] = 1.0 / attributes['mtbf_goal']
        attributes['reliability_goal'] = exp(-1.0 * attributes['mission_time']
                                             / attributes['mtbf_goal'])

    return attributes
