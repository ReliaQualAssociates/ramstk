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
    *,
    application_id: int,
    current_ratio: float,
    power_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for switchs.

    :param environment_id: the index for the environment the switch is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for switches.
    :param application_id: the application ID for the switch being checked for
        overstress.
    :param current_ratio: the operating to rated ratio of current for the switch being
        checked for overstress.
    :param power_ratio: the operating to rated ratio of power for the switch being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid application ID.
    :raises: TypeError when passed a non-numeric value for the current ratio or power
        ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _application = _get_switch_application(application_id)

    try:
        # Check current limit
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_current_limit(
                current_ratio,
                stress_limits[_application]["current"][environment_id],
            ),
        )

        # Check power limit
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_power_limit(
                power_ratio, stress_limits[_application]["power"][environment_id]
            ),
        )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid switch environment ID {environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid switch application ID {application_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid switch current ratio type "
            f"{type(current_ratio)} or power ratio type {type(power_ratio)}.  Both "
            f"should be <type 'float'>."
        )


def _get_switch_application(application_id: int) -> str:
    """Retrieve the application type based on the application ID.

    :param application_id: the application ID for the switch being checked for
        overstress.
    :return: the selected switch application name.
    :rtype: str
    """
    return {
        1: "resistive_load",
        2: "inductive_load",
        3: "lamp_load",
    }.get(application_id, "")
