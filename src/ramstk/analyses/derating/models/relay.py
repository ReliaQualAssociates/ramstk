# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_temperature_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for relays.

    :param environment_id: the index for the environment the relay is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for relays.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown type ID is passed. :raise: TypeError if a non-numeric
        value is passed for the current ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _type = {
        1: "resistive_load",
        2: "inductive_load",
        3: "capacitive_load",
    }[kwargs["type_id"]]

    _overstress, _reason = do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_type]["current"][environment_id],
    )

    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_temperature_limit(
            kwargs["temperature_active"],
            kwargs["temperature_rated_max"],
            stress_limits[_type]["temperature"][environment_id],
        ),
    )

    return _overstress, _reason
