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
    """Update overstress and reason based on check results."""
    _ostress, _rsn = result
    return overstress or _ostress, reason + _rsn


def do_check_current_limit(
    current_ratio: float,
    current_limit: float,
) -> Tuple[int, str]:
    """Check if the current ratio exceeds the limit.

    :param current_ratio:
    :param current_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if current_ratio <= current_limit:
        return 0, ""

    return (
        1,
        f"Current ratio of {current_ratio} exceeds the allowable limit of "
        f"{current_limit}.\n",
    )


def do_check_power_limit(
    power_ratio: float,
    power_limit: float,
) -> Tuple[int, str]:
    """Check if the power ratio exceeds the limit.

    :param power_ratio:
    :param power_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if power_ratio <= power_limit:
        return 0, ""

    return (
        1,
        f"Power ratio of {power_ratio} exceeds the allowable limit of {power_limit}.\n",
    )


def do_check_temperature_limit(
    actual_temperature: float, max_rated_temperature: float, limit: float
) -> Tuple[int, str]:
    """Generalized temperature limit check."""
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


def do_check_voltage_limit(
    voltage_ratio: float,
    voltage_limit: float,
) -> Tuple[int, str]:
    """Check if the voltage ratio exceeds the limit.

    :param voltage_ratio:
    :param voltage_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if voltage_ratio <= voltage_limit:
        return 0, ""

    return (
        1,
        f"Voltage ratio of {voltage_ratio} exceeds the allowable limit of "
        f"{voltage_limit}.\n",
    )
