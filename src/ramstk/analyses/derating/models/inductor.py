# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for inductors.

    :param environment_id: the index for the environment the inductor is operating
        in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the indcutor to check derating.
    :param stress_limits: the dict containing the stress derating limits for inductors.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown family ID is passed.
    :raise: TypeError if a non-numeric value is passed for the current ratio, hot spot
        temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _frequency = {
        1: {
            1: "low_frequency",
            2: "low_frequency",
            3: "low_frequency",
            4: "high_frequency",
        },
        2: "high_frequency",
    }[subcategory_id]
    if isinstance(_frequency, dict):
        _frequency = _frequency[kwargs["family_id"]]

    _overstress, _reason = _do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_frequency]["current"][environment_id],
    )

    _ostress, _rsn = _do_check_temperature_limit(
        kwargs["temperature_hot_spot"],
        kwargs["temperature_rated_max"],
        stress_limits[_frequency]["temperature"][environment_id],
    )
    _overstress = _overstress or _ostress
    _reason += _rsn

    if _frequency == "low_frequency":
        _ostress, _rsn = _do_check_voltage_limit(
            kwargs["voltage_ratio"],
            stress_limits[_frequency]["voltage"][environment_id],
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
    hot_spot_temperature: float,
    max_rated_temperature: float,
    temperature_limit: float,
) -> Tuple[int, str]:
    """Check if the hot spot temperature exceeds the limit.

    :param hot_spot_temperature:
    :param max_rated_temperature:
    :param temperature_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if hot_spot_temperature <= (max_rated_temperature - temperature_limit):
        return 0, ""

    return (
        1,
        f"Hot spot temperature of {hot_spot_temperature}C exceeds the derated "
        f"maximum hot spot temperature of {temperature_limit}C less than maximum "
        f"rated hot spot temperature of {max_rated_temperature}C.\n",
    )


def _do_check_voltage_limit(
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
