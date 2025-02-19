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
    *,
    current_ratio: float,
    family_id: int,
    temperature_hot_spot: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for inductors.

    :param environment_id: the index for the environment the inductive device is
        operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the inductive device being checked for
        overstress.
    :param stress_limits: the dict containing the stress derating limits for inductive
        devices.
    :param current_ratio: the operating to rated current ratio of the inductive device
        being checked for overstress.
    :param family_id: the family ID of the inductive device being checked for
        overstress.
    :param temperature_hot_spot: the hot spot temperature of the inductive device being
        checked for overstress.
    :param temperature_rated_max: the maximum rated temperature of the inductive device
        being checked for overstress.
    :param voltage_ratio: the operating to rated voltage ratio of teh inductive device
        being checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid family ID.
    :raises: TypeError when passed a non-numeric value for the current ratio, hot spot
        temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    try:
        # Determine the frequency category based on subcategory and, if needed, family.
        if subcategory_id == 1:
            _frequency: str = {
                1: "low_frequency",
                2: "low_frequency",
                3: "low_frequency",
                4: "high_frequency",
            }[family_id]
        else:
            _frequency = "high_frequency"

        # Check current limit
        _overstress, _reason = do_check_current_limit(
            current_ratio,
            stress_limits[_frequency]["current"][environment_id],
        )

        # Check temperature limit
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                temperature_hot_spot,
                temperature_rated_max,
                stress_limits[_frequency]["temperature"][environment_id],
            ),
        )

        # Check voltage limit for low-frequency inductors
        if _frequency == "low_frequency":
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_voltage_limit(
                    voltage_ratio,
                    stress_limits[_frequency]["voltage"][environment_id],
                ),
            )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid inductive device environment "
            f"ID {environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid inductive device family ID {family_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid inductive device current "
            f"ratio type {type(current_ratio)}, hot spot temperature type"
            f" {type(temperature_hot_spot)}, or voltage ratio type "
            f"{type(voltage_ratio)}.  All should be <type 'float'>."
        ) from exc
