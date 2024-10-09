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
    parent_goal: float, attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """Perform an AGREE apportionment of a reliability requirement.

    .. note:: the AGREE method uses MTBF as the parent goal.

    :param parent_goal: the reliability goal of the parent hardware
        item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated
    values.
    :rtype: dict
    """
    _values = _calculate_common_values(attributes)
    _time_i = _values["time_i"]

    try:
        _weight_factor = float(attributes["weight_factor"])
        _n_sub_systems = int(attributes["n_sub_systems"])
        _n_sub_elements = int(attributes["n_sub_elements"])

        _mtbf_alloc = (_n_sub_systems * _weight_factor * _time_i) / (
            _n_sub_elements * (-log(parent_goal))
        )
        _hazard_rate_alloc = 1.0 / _mtbf_alloc
        _reliability_alloc = exp(-_hazard_rate_alloc * _time_i)

        attributes.update(
            {
                "mtbf_alloc": _mtbf_alloc,
                "hazard_rate_alloc": _hazard_rate_alloc,
                "reliability_alloc": _reliability_alloc,
            }
        )
    except (ValueError, ZeroDivisionError) as err:
        _send_pubsub_message(
            "fail_allocate_reliability",
            f"Failed to apportion reliability using the AGREE method: {str(err)}.",
        )

    return attributes


def _calculate_arinc_apportionment(
    parent_goal: float, attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """Perform an ARINC apportionment of the reliability requirement.

    :param parent_goal: the reliability goal of the parent hardware item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    """
    _mission_time = float(attributes["mission_time"])
    try:
        _weight_factor = float(attributes["weight_factor"])
        _hazard_rate_alloc = _weight_factor * parent_goal
        _mtbf_alloc = 1.0 / _hazard_rate_alloc
        _reliability_alloc = exp(-_hazard_rate_alloc * _mission_time)

        attributes.update(
            {
                "mtbf_alloc": _mtbf_alloc,
                "hazard_rate_alloc": _hazard_rate_alloc,
                "reliability_alloc": _reliability_alloc,
            }
        )
    except ZeroDivisionError:
        _send_pubsub_message(
            "fail_allocate_reliability",
            "Failed to apportion reliability using the ARINC method; weight "
            "factor or parent goal is zero.",
        )

    return attributes


def _calculate_common_values(attributes: Dict[str, Any]) -> Dict[str, float]:
    """Extract common values from attributes and calculate time_i.

    :param attributes: The allocation attributes dictionary.
    :type attributes: dict
    :return: A dictionary with common calculation values such as time_i and
        mission_time.
    :rtype: dict
    """
    mission_time = float(attributes["mission_time"])
    duty_cycle = float(attributes.get("duty_cycle", 100.0))
    time_i = mission_time * duty_cycle / 100.0
    return {"mission_time": mission_time, "time_i": time_i}


def _calculate_equal_apportionment(
    parent_goal: float, attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """Perform an equal apportionment of the reliability goal.

    :param parent_goal: the reliability goal of the parent hardware item.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    """
    _mission_time = float(attributes["mission_time"])
    try:
        _weight_factor = float(attributes["weight_factor"])
        _reliability_alloc = parent_goal**_weight_factor
        _hazard_rate_alloc = -log(_reliability_alloc) / _mission_time
        _mtbf_alloc = 1.0 / _hazard_rate_alloc

        attributes.update(
            {
                "hazard_rate_alloc": _hazard_rate_alloc,
                "mtbf_alloc": _mtbf_alloc,
                "reliability_alloc": _reliability_alloc,
            }
        )
    except (TypeError, ValueError, ZeroDivisionError) as err:
        _send_pubsub_message(
            "fail_allocate_reliability",
            f"Failed to apportion reliability using the equal " f"method: {str(err)}.",
        )

    return attributes


def _calculate_foo_apportionment(
    parent_goal: float, cum_weight: int, attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """Perform a feasibility of objectives (FOO) apportionment.

    :param parent_goal: the failure rate requirement to allocate.
    :param cum_weight: the cumulative weight factor for all subordinate assemblies.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    try:
        _intricacy = int(attributes["int_factor"])
        _state_of_art = int(attributes["soa_factor"])
        _operating_time = int(attributes["op_time_factor"])
        _environment = int(attributes["env_factor"])

        _weight_factor = _intricacy * _state_of_art * _operating_time * _environment
        _percent_weight_factor = _weight_factor / cum_weight

        _hazard_rate_alloc = _percent_weight_factor * parent_goal
        _mtbf_alloc = 1.0 / _hazard_rate_alloc
        _reliability_alloc = exp(
            -_hazard_rate_alloc * float(attributes["mission_time"])
        )

        attributes.update(
            {
                "weight_factor": _weight_factor,
                "percent_weight_factor": _percent_weight_factor,
                "hazard_rate_alloc": _hazard_rate_alloc,
                "mtbf_alloc": _mtbf_alloc,
                "reliability_alloc": _reliability_alloc,
            }
        )
    except ZeroDivisionError:
        _send_pubsub_message(
            "fail_allocate_reliability",
            "Failed to apportion reliability using the FOO method due to "
            "zero inputs.",
        )

    return attributes


def _from_hazard_rate_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MTBF and reliability goals given the hazard rate goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes["mission_time"])
    _hazard_rate_goal: Any = float(attributes["hazard_rate_goal"])
    try:
        _mtbf_goal: Any = 1.0 / _hazard_rate_goal
        _reliability_goal: Any = exp(-1.0 * _mission_time / _mtbf_goal)
    except ZeroDivisionError:
        _mtbf_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage(
            "fail_calculate_allocation_goal",
            error_message=(
                f"Failed to calculate the MTBF and "
                f"reliability goals given the hazard rate "
                f"goal.  Hazard rate goal={_hazard_rate_goal}."
            ),
        )

    attributes["mtbf_goal"] = _mtbf_goal
    attributes["reliability_goal"] = _reliability_goal

    return attributes


def _from_mtbf_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the hazard rate and reliability goals given the MTBF goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes["mission_time"])
    _mtbf_goal: Any = float(attributes["mtbf_goal"])
    try:
        _hazard_rate_goal: Any = 1.0 / _mtbf_goal
        _reliability_goal: Any = exp(-1.0 * _mission_time / _mtbf_goal)
    except ZeroDivisionError:
        _hazard_rate_goal = 0.0
        _reliability_goal = 0.0
        pub.sendMessage(
            "fail_calculate_allocation_goal",
            error_message=(
                f"Failed to calculate the hazard rate and "
                f"reliability goals given the MTBF goal.  "
                f"MTBF goal={_mtbf_goal}."
            ),
        )

    attributes["hazard_rate_goal"] = _hazard_rate_goal
    attributes["reliability_goal"] = _reliability_goal

    return attributes


def _from_reliability_goal(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the MTBF and hazard rate goals given the reliability goal.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    _mission_time: Any = float(attributes["mission_time"])
    _reliability_goal: Any = float(attributes["reliability_goal"])
    try:
        _mtbf_goal: Any = -1.0 * _mission_time / log(_reliability_goal)
        _hazard_rate_goal: Any = 1.0 / _mtbf_goal
    except ValueError:
        _mtbf_goal = 0.0
        _hazard_rate_goal = 0.0
        pub.sendMessage(
            "fail_calculate_allocation_goal",
            error_message=(
                f"Failed to calculate the MTBF and "
                f"hazard rate goals given the reliability "
                f"goal.  Reliability goal={_reliability_goal}."
            ),
        )

    attributes["hazard_rate_goal"] = _hazard_rate_goal
    attributes["mtbf_goal"] = _mtbf_goal

    return attributes


def _send_pubsub_message(message_type: str, message: str) -> None:
    """Send a failure message via pubsub.

    :param message_type: The type of message to send.
    :type message_type: str
    :param error_message: The error message to be sent.
    :type error_message: str
    :return: None
    """
    pub.sendMessage(message_type, error_message=message)


def do_allocate_reliability(
    parent_goal: float, cumulative_weight: int, **attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate the reliability allocation.

    :param parent_goal: the parent assembly's reliability goal.
    :param cumulative_weight: the cumulative weighting of all child assemblies. Used for
        feasibility of objectives method only.
    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    _method_id: int = attributes["allocation_method_id"]

    _allocation_methods = {
        1: _calculate_equal_apportionment,
        2: _calculate_agree_apportionment,
        3: _calculate_arinc_apportionment,
    }

    if _method_id in _allocation_methods:
        attributes = _allocation_methods[_method_id](parent_goal, attributes)
    elif _method_id == 4:
        attributes = _calculate_foo_apportionment(
            parent_goal, cumulative_weight, attributes
        )
    else:
        attributes.update(
            {"hazard_rate_alloc": 0.0, "mtbf_alloc": 0.0, "reliability_alloc": 1.0}
        )

    pub.sendMessage("succeed_allocate_reliability", attributes=attributes)

    return attributes


def do_calculate_goals(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the other two reliability metrics from the third.

    :param attributes: the Allocation attributes dict.
    :return: attributes; the Allocation attributes dict with updated values.
    :rtype: dict
    """
    if attributes["goal_measure_id"] == 1:  # Reliability goal
        attributes = _from_reliability_goal(attributes)
    elif attributes["goal_measure_id"] == 2:  # Hazard rate goal
        attributes = _from_hazard_rate_goal(attributes)
    elif attributes["goal_measure_id"] == 3:  # MTBF goal
        attributes = _from_mtbf_goal(attributes)
    else:
        _hazard_rate_goal: Any = 0.0
        _mtbf_goal: Any = 0.0
        _reliability_goal: Any = 1.0
        attributes["hazard_rate_goal"] = _hazard_rate_goal
        attributes["mtbf_goal"] = _mtbf_goal
        attributes["reliability_goal"] = _reliability_goal

    pub.sendMessage("succeed_calculate_allocation_goals", attributes=attributes)

    return attributes


def get_allocation_goal(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve the reliability goal for the hardware item.

    Used to select the goal for the parent hardware item prior to calling the
    do_allocate_reliability() method.

    :param attributes: the selected item's Allocation attributes dict.
    :return: _goal
    :rtype: float :raise: KeyError if the passed attributes dict doesn't contain the
        allocation_method_id, hazard_rate_goal, and/or reliability_goal key.
    """
    return (
        attributes["hazard_rate_goal"]
        if attributes["allocation_method_id"] in [2, 4]
        else attributes["reliability_goal"]
    )
