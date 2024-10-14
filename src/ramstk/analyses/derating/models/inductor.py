# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
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
    """Check actual stresses against derating criteria for inductors.

    :param environment_id: the index for the environment the inductor is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the indcutor to check derating.
    :param stress_limits: the dict containing the stress derating limits for inductors.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown family ID is passed. :raise: TypeError if a non-numeric
        value is passed for the current ratio, hot spot temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    # Determine the frequency category based on subcategory and family.
    _frequency = {
        1: {
            1: "low_frequency",
            2: "low_frequency",
            3: "low_frequency",
            4: "high_frequency",
        },
        2: "high_frequency",
    }[subcategory_id]

    if isinstance(_frequency, dict):
        _frequency = _frequency[kwargs["family_id"]]

        # Check current limit
        _overstress, _reason = do_check_current_limit(
            kwargs["current_ratio"],
            stress_limits[_frequency]["current"][environment_id],
        )

        # Check temperature limit
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                kwargs["temperature_hot_spot"],
                kwargs["temperature_rated_max"],
                stress_limits[_frequency]["temperature"][environment_id],
            ),
        )

        # Check voltage limit for low-frequency inductors
        if _frequency == "low_frequency":
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_voltage_limit(
                    kwargs["voltage_ratio"],
                    stress_limits[_frequency]["voltage"][environment_id],
                ),
            )

    return _overstress, _reason
