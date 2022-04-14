# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.semiconductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for semiconductors.

    :param environment_id: the index for the environment the semiconductor
        is operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the semiconductor to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for
        semiconductors.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown subcategory ID, quality ID, or type ID are passed.
    :raise: TypeError if a non-numeric value is passed for the current ratio,
        power ratio, junction temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = {
        1: "diode",
        3: "transistor",
        4: "transistor",
        6: "transistor",
        7: "transistor",
        8: "transistor",
        9: "transistor",
        10: "thyristor",
    }[subcategory_id]
    _type = {
        1: {
            1: "general_purpose",
            2: "general_purpose",
            3: "power_rectifier",
            4: "schottky",
            5: "power_rectifier",
            6: "suppressor",
            7: "regulator",
            8: "regulator",
        },
        3: "bjt",
        4: "fet",
        6: "bjt",
        7: "bjt",
        9: "fet",
    }[subcategory_id]
    if isinstance(_type, dict):
        _type = _type[kwargs["type_id"]]

    _quality = {
        1: "jantx",
        2: "jantx",
        3: "military",
        4: "commercial",
        5: "commercial",
    }[kwargs["quality_id"]]

    _overstress, _reason = _do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_subcategory][_type][_quality]["current"][environment_id],
    )

    if (
        _subcategory == "diode" and _type in ["schottky,", "regulator", "suppressor"]
    ) or _subcategory == "transistor":
        _ostress, _rsn = _do_check_power_limit(
            kwargs["power_ratio"],
            stress_limits[_subcategory][_type][_quality]["power"][environment_id],
        )
        _overstress = _overstress or _ostress
        _reason += _rsn

    _ostress, _rsn = _do_check_temperature_limit(
        kwargs["temperature_junction"],
        stress_limits[_subcategory][_type][_quality]["temperature"][environment_id],
    )
    _overstress = _overstress or _ostress
    _reason += _rsn

    _ostress, _rsn = _do_check_voltage_limit(
        kwargs["voltage_ratio"],
        stress_limits[_subcategory][_type][_quality]["voltage"][environment_id],
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


def _do_check_power_limit(
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
        f"Power ratio of {power_ratio} exceeds the allowable limit of "
        f"{power_limit}.\n",
    )


def _do_check_temperature_limit(
    junction_temperature: float,
    temperature_limit: float,
) -> Tuple[int, str]:
    """Check if the junction temperature exceeds the limit.

    :param junction_temperature:
    :param temperature_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    if junction_temperature <= temperature_limit:
        return 0, ""

    return (
        1,
        f"Junction temperature of {junction_temperature}C exceeds the allowable "
        f"limit of {temperature_limit}C.\n",
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
