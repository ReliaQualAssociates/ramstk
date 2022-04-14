# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for relays.

    :param environment_id: the index for the environment the relay
        is operating in; 0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for
        relays.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown type ID is passed.
    :raise: TypeError if a non-numeric value is passed for the current ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _type = {
        1: "resistive_load",
        2: "inductive_load",
        3: "capacitive_load",
    }[kwargs["type_id"]]

    _overstress, _reason = _do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_type]["current"][environment_id],
    )

    _ostress, _rsn = _do_check_temperature_limit(
        kwargs["temperature_active"],
        kwargs["temperature_rated_max"],
        stress_limits[_type]["temperature"][environment_id],
    )
    _overstress = _overstress or _ostress
    _reason += _rsn

    return _overstress, _reason


def _do_check_current_limit(
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


def _do_check_temperature_limit(
    active_temperature: float,
    max_rated_temperature: float,
    temperature_limit: float,
) -> Tuple[int, str]:
    """Check if the relay temperature exceeds the limit.

    :param active_temperature:
    :param max_rated_temperature:
    :param temperature_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if active_temperature <= (max_rated_temperature - temperature_limit):
        return 0, ""

    return (
        1,
        f"Ambient temperature of {active_temperature}C exceeds the derated maximum "
        f"temperature of {temperature_limit}C less than maximum rated temperature "
        f"of {max_rated_temperature}C.\n",
    )
