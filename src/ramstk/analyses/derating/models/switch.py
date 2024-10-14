# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_power_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for switchs.

    :param environment_id: the index for the environment the switch is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for switchs.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown application ID is passed. :raise: TypeError if a non-
        numeric value is passed for the current ratio or power ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _application = _get_switch_application(kwargs["application_id"])

    # Check current limit
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_current_limit(
            kwargs["current_ratio"],
            stress_limits[_application]["current"][environment_id],
        ),
    )

    # Check power limit
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_power_limit(
            kwargs["power_ratio"], stress_limits[_application]["power"][environment_id]
        ),
    )

    return _overstress, _reason


def _get_switch_application(application_id: int) -> str:
    """Return the application type based on the application ID."""
    return {
        1: "resistive_load",
        2: "inductive_load",
        3: "lamp_load",
    }[application_id]
