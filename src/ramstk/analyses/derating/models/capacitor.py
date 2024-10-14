# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Optional, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for capacitors.

    :param environment_id: the index for the environment the capacitor is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the capacitor to check derating.
    :param stress_limits: the dict containing the stress derating limits for capacitors.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown subcategory ID, quality ID, or type ID are passed.
        :raise: TypeError if a non-numeric value is passed for the current ratio, power
        ratio, junction temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = _do_resolve_subcategory(
        subcategory_id, kwargs.get("specification_id")
    )

    # Check temperature limits
    _overstress, _reason = do_check_temperature_limit(
        kwargs["temperature_case"],
        kwargs["temperature_rated_max"],
        stress_limits[_subcategory]["temperature"][environment_id],
    )

    # Check voltage limits
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_voltage_limit(
            kwargs["voltage_ratio"],
            stress_limits[_subcategory]["voltage"][environment_id],
        ),
    )

    return _overstress, _reason


def _do_resolve_subcategory(
    subcategory_id: int, specification_id: Optional[int]
) -> str:
    """Resolve the capacitor subcategory based on subcategory and specification ID."""
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

    if isinstance(_subcategory, dict) and specification_id:
        return _subcategory[specification_id]

    return _subcategory
