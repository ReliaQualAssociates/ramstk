# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for capacitors.

    :param environment_id: the index for the environment the capacitor
        is operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the capacitor to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for
        capacitors.
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
        1: "paper",
        2: "paper",
        3: "plastic",
        4: "metallized",
        5: "metallized",
        6: "metallized",
        7: "mica",
        8: "mica_button",
        9: "glass",
        10: "ceramic_fixed",
        11: {
            1: "temp_comp_ceramic",
            2: "ceramic_chip",
        },
        12: {
            1: "tantalum_solid",
            2: "tantalum_chip",
        },
        13: "tantalum_wet",
        14: "aluminum",
        15: "aluminum_dry",
        16: "ceramic_variable",
        17: "piston",
        18: "trimmer",
        19: "vacuum",
    }[subcategory_id]
    if isinstance(_subcategory, dict):
        _subcategory = _subcategory[kwargs["specification_id"]]

    _overstress, _reason = _do_check_temperature_limit(
        kwargs["temperature_case"],
        kwargs["temperature_rated_max"],
        stress_limits[_subcategory]["temperature"][environment_id],
    )

    _ostress, _rsn = _do_check_voltage_limit(
        kwargs["voltage_ratio"],
        stress_limits[_subcategory]["voltage"][environment_id],
    )
    _overstress = _overstress or _ostress
    _reason += _rsn

    return _overstress, _reason


def _do_check_temperature_limit(
    case_temperature: float,
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
    if case_temperature <= (max_rated_temperature - temperature_limit):
        return 0, ""

    return (
        1,
        f"Case temperature of {case_temperature}C exceeds the derated maximum "
        f"temperature of {temperature_limit}C less than maximum rated temperature "
        f"of {max_rated_temperature}C.\n",
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
