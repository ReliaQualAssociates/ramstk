# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.derating_utils.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Derating Calculations Module Utility Functions."""

# Standard Library Imports
from typing import Tuple


def do_update_overstress_status(
    overstress: int, reason: str, result: Tuple[int, str]
) -> Tuple[int, str]:
    """Update overstress and reason based on check results.

    :param overstress: the current overstress status.
    :param reason: the current overstress reason string.
    :param result: the overstress status and reason string from the latest check.
    :return: the updated overstress status and reason string.
    :rtype: tuple
    """
    _ostress, _rsn = result
    return overstress or _ostress, reason + _rsn


def do_check_current_limit(
    current_ratio: float,
    current_limit: float,
) -> Tuple[int, str]:
    """Check if the current ratio exceeds the limit.

    :param current_ratio: the operating to rated current ratio of the component being
        checked for overstress.
    :param current_limit: the derating current ratio limit for the component being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: TypeError when passed a non-numeric value for the current ratio or current
        limit.
    """
    try:
        if current_ratio <= current_limit:
            return 0, ""

        return (
            1,
            f"Current ratio of {current_ratio} exceeds the allowable limit of "
            f"{current_limit}.\n",
        )
    except TypeError as exc:
        raise TypeError(
            f"do_check_current_limit: Invalid current limit type {type(current_limit)} "
            f"or current ratio type {type(current_ratio)}.  Both should be "
            f"<type 'float'>."
        ) from exc


def do_check_power_limit(
    power_ratio: float,
    power_limit: float,
) -> Tuple[int, str]:
    """Check if the power ratio exceeds the limit.

    :param power_ratio: the operating to rated power ratio of the component being
        checked for overstress.
    :param power_limit: the derating power ratio limit for the component being checked
        for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: TypeError when passed a non-numeric value for the power ratio or power
        limit.
    """
    try:
        if power_ratio <= power_limit:
            return 0, ""

        return (
            1,
            f"Power ratio of {power_ratio} exceeds the allowable limit of "
            f"{power_limit}.\n",
        )
    except TypeError as exc:
        raise TypeError(
            f"do_check_power_limit: Invalid power limit type {type(power_limit)} "
            f"or power ratio type {type(power_ratio)}.  Both should be "
            f"<type 'float'>."
        ) from exc


def do_check_temperature_limit(
    actual_temperature: float,
    max_rated_temperature: float,
    limit: float,
) -> Tuple[int, str]:
    """Check if actual temperature exceeds the limit.

    :param actual_temperature: the current temperature of the component being checked
        for overstress.
    :param max_rated_temperature: the maximum rated temperature of the component being
        checked for overstress.
    :param limit: the percentage of max rated temperature allowed (0.0 to 1.0) of the
        component being checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: TypeError when passed a non-numeric value for the temperature limit,
        maximum rated temperature, or operating temperature.
    """
    try:
        if actual_temperature <= (max_rated_temperature - limit):
            return 0, ""

        if limit < 1.0:
            _reason = (
                f"Temperature of {actual_temperature}C exceeds the derated maximum "
                f"temperature of {max_rated_temperature}C.\n"
            )
        else:
            _reason = (
                f"Temperature of {actual_temperature}C exceeds the derated maximum "
                f"temperature of {limit}C less than maximum rated temperature of "
                f"{max_rated_temperature}C.\n"
            )

        return (
            1,
            _reason,
        )
    except TypeError as exc:
        raise TypeError(
            f"do_check_temperature_limit: Invalid temperature limit type"
            f" {type(limit)}, maximum rated temperature type "
            f"{type(max_rated_temperature)}, or operating temperature type "
            f"{type(actual_temperature)}.  All should be <type 'float'>."
        ) from exc


def do_check_voltage_limit(
    voltage_ratio: float,
    voltage_limit: float,
) -> Tuple[int, str]:
    """Check if the voltage ratio exceeds the limit.

    :param voltage_ratio: the operating to rated voltage ratio of the component being
        checked for overstress.
    :param voltage_limit: the derating voltage ratio limit of the component being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: TypeError when passed a non-numeric value for the voltage limit or voltage
        ratio.
    """
    try:
        if voltage_ratio <= voltage_limit:
            return 0, ""

        return (
            1,
            f"Voltage ratio of {voltage_ratio} exceeds the allowable limit of "
            f"{voltage_limit}.\n",
        )
    except TypeError as exc:
        raise TypeError(
            f"do_check_voltage_limit: Invalid voltage limit type {type(voltage_limit)} "
            f"or voltage ratio type {type(voltage_ratio)}.  Both should be "
            f"<type 'float'>."
        ) from exc
