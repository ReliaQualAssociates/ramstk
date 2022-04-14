# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.integratedcircuit.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for integrated circuits.

    :param environment_id: the index for the environment the integrated circuit
        is operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the integrated circuit to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for
        integrated circuits.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown subcategory ID, package ID, or technology ID are
        passed.
    :raise: TypeError if a non-numeric value is passed for the current ratio or junction
        temperature.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = {
        1: "digital",
        2: "linear",
        3: "microprocessor",
        4: "memory",
    }[subcategory_id]
    _technology = {
        1: "bipolar",
        2: "mos",
    }[kwargs["technology_id"]]
    _package = {
        1: "hermetic",
        2: "hermetic",
        3: "hermetic",
        4: "plastic1",
        5: "plastic1",
        6: "plastic1",
        7: "plastic2",
        8: "plastic2",
        9: "plastic2",
    }[kwargs["package_id"]]

    _overstress, _reason = _do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_subcategory][_technology][_package]["current"][environment_id],
    )

    _ostress, _rsn = _do_check_temperature_limit(
        kwargs["temperature_junction"],
        stress_limits[_subcategory][_technology][_package]["temperature"][
            environment_id
        ],
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
