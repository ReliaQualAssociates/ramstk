# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.semiconductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_power_limit,
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for semiconductors.

    :param environment_id: the index for the environment the semiconductor is operating
        in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the semiconductor to check derating.
    :param stress_limits: the dict containing the stress derating limits for
        semiconductors.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown subcategory ID, quality ID, or type ID are passed.
        :raise: TypeError if a non-numeric value is passed for the current ratio, power
        ratio, junction temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = _get_semiconductor_subcategory(subcategory_id)
    _type = _get_semiconductor_type(subcategory_id, kwargs.get("type_id", 0))
    _quality = _get_semiconductor_quality(kwargs.get("quality_id", 1))

    # Check current limit.
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_current_limit(
            kwargs["current_ratio"],
            stress_limits[_subcategory][_type][_quality]["current"][environment_id],
        ),
    )

    # Check power limit for specific subcategories and types.
    if (
        _subcategory == "diode"
        and _type in ["schottky", "regulator", "suppressor"]
        or _subcategory == "transistor"
    ):
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_power_limit(
                kwargs["power_ratio"],
                stress_limits[_subcategory][_type][_quality]["power"][environment_id],
            ),
        )

        # Check junction temperature limit.
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                kwargs["temperature_junction"],
                stress_limits[_subcategory][_type][_quality]["temperature"][
                    environment_id
                ],
                0.0,
            ),
        )

        # Check voltage limit.
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_voltage_limit(
                kwargs["voltage_ratio"],
                stress_limits[_subcategory][_type][_quality]["voltage"][environment_id],
            ),
        )

    return _overstress, _reason


def _get_semiconductor_subcategory(subcategory_id: int) -> str:
    """Return the semiconductor subcategory based on the subcategory ID."""
    _subcategories = {
        1: "diode",
        3: "transistor",
        4: "transistor",
        6: "transistor",
        7: "transistor",
        8: "transistor",
        9: "transistor",
        10: "thyristor",
    }

    _subcategory = _subcategories.get(subcategory_id)

    if _subcategory is None:
        raise KeyError(f"Unknown subcategory_id: {subcategory_id}")

    return _subcategory


def _get_semiconductor_type(subcategory_id: int, type_id: int) -> str:
    """Return the semiconductor type based on the subcategory ID and type ID."""
    _type_mapping = {
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
    }
    _type = _type_mapping.get(subcategory_id, "")
    return _type.get(type_id, "") if isinstance(_type, dict) else _type


def _get_semiconductor_quality(quality_id: int) -> str:
    """Return the semiconductor quality based on the quality ID."""
    return {
        1: "jantx",
        2: "jantx",
        3: "military",
        4: "commercial",
        5: "commercial",
    }[quality_id]
