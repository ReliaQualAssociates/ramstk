# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for resistors.

    :param environment_id: the index for the environment the resistor
        is operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the resistor to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for
        resistors.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown subcategory ID is passed.
    :raise: TypeError if a non-numeric value is passed for the power ratio, rated power,
        case temperature, knee temperature, rated temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = {
        1: "fixed_composition",
        2: "fixed_film",
        3: "fixed_film_power",
        4: "ixed_film_network",
        5: "fixed_wirewound",
        6: "fixed_wirewound_power",
        7: "fixed_wirewound_chassis",
        8: "thermistor",
        9: "variable_wirewound",
        10: "variable_wirewound_precision",
        11: "variable_wirewound",
        12: "variable_wirewound_power",
        13: "variable_non_wirewound",
        14: "variable_composition",
        15: "variable_film",
    }[subcategory_id]

    _power_limit = _do_get_power_limit(
        _subcategory,
        environment_id,
        kwargs["power_rated"],
        stress_limits,
    )
    _overstress, _reason = _do_check_power_limit(
        kwargs["power_ratio"],
        _power_limit,
    )

    _temperature_limit = _do_get_temperature_limit(
        _subcategory,
        environment_id,
        kwargs["power_rated"],
        stress_limits,
    )
    _ostress, _rsn = _do_check_temperature_limit(
        kwargs["temperature_case"],
        kwargs["temperature_knee"],
        kwargs["temperature_rated_max"],
        _temperature_limit,
    )
    _overstress = _overstress or _ostress
    _reason += _rsn

    if subcategory_id in {2, 4, 5, 6, 7}:
        _voltage_limit = _do_get_voltage_limit(
            _subcategory,
            environment_id,
            kwargs["power_rated"],
            stress_limits,
        )
        _ostress, _rsn = _do_check_voltage_limit(
            kwargs["voltage_ratio"],
            _voltage_limit,
        )
        _overstress = _overstress or _ostress
        _reason += _rsn

    return _overstress, _reason


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
    case_temperature: float,
    knee_temperature: float,
    max_rated_temperature: float,
    temperature_limit: float,
) -> Tuple[int, str]:
    """Check if the case temperature exceeds the limit.

    :param case_temperature:
    :param max_rated_temperature:
    :param temperature_limit:
    :return: _overstress, _reason
    :rtype: tuple
    """
    _max_temperature: float = knee_temperature + temperature_limit * (
        max_rated_temperature - knee_temperature
    )

    if case_temperature <= _max_temperature:
        return 0, ""

    return (
        1,
        f"Case temperature of {case_temperature}C exceeds the derated maximum "
        f"temperature of {_max_temperature}C.\n",
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


def _do_get_power_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float:
    """Retrieve the power limits.

    :param subcategory:
    :param environment_id:
    :param rated_power:
    :param stress_limits:
    :return: _power_limit
    :rtype: float
    """
    if subcategory in {"fixed_composition", "fixed_film", "fixed_wirewound"}:
        return (
            stress_limits[subcategory]["high_power"]["power"][environment_id]
            if rated_power >= 0.5
            else stress_limits[subcategory]["low_power"]["power"][environment_id]
        )

    return stress_limits[subcategory]["power"][environment_id]


def _do_get_temperature_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float:
    """Retrieve the power limits.

    :param subcategory:
    :param environment_id:
    :param rated_power:
    :param stress_limits:
    :return: _temperature_limit
    :rtype: float
    """
    if subcategory in {"fixed_composition", "fixed_film", "fixed_wirewound"}:
        return (
            stress_limits[subcategory]["high_power"]["temperature"][environment_id]
            if rated_power >= 0.5
            else stress_limits[subcategory]["low_power"]["temperature"][environment_id]
        )

    return stress_limits[subcategory]["temperature"][environment_id]


def _do_get_voltage_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
) -> float:
    """Retrieve the power limits.

    :param subcategory:
    :param environment_id:
    :param rated_power:
    :param stress_limits:
    :return: _voltage_limit
    :rtype: float
    """
    if subcategory in {"fixed_composition", "fixed_film", "fixed_wirewound"}:
        return (
            stress_limits[subcategory]["high_power"]["voltage"][environment_id]
            if rated_power >= 0.5
            else stress_limits[subcategory]["low_power"]["voltage"][environment_id]
        )

    return stress_limits[subcategory]["voltage"][environment_id]
