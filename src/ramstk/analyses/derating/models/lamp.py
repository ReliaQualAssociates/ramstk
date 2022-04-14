# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.lamp.py is part of the RAMSTK Project
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
    """Check actual stresses against derating criteria for lamps.

    :param environment_id: the index for the environment the lamp
        is operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the lamp to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for
        lamps.
    :return: _overstress, _reason
    :rtype: tuple
    :raise: IndexError if an unknown environment ID is passed.
    :raise: KeyError if an unknown subcategory ID is passed.
    :raise: TypeError if a non-numeric value is passed for the current ratio.
    """
    _subcategory = {
        4: "lamp",
    }[subcategory_id]

    return _do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_subcategory]["current"][environment_id],
    )


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
