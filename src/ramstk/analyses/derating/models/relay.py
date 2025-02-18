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
    *,
    current_ratio: float,
    temperature_active: float,
    temperature_rated_max: float,
    type_id: int,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for relays.

    :param environment_id: the index for the environment the relay is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for relays.
    :param current_ratio: the operating to rated current ratio of the relay being
        checked for overstress.
    :param temperature_active: the ambient operating temperature of the relay being
        checked for overstress.
    :param temperature_rated_max: the maximum rated temperature of the relay being
        checked for overstress.
    :param type_id: the load type ID of the relay being checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid type ID.
    :raises: TypeError when passed a non-numeric value for the current ratio or ambient
        operating temperature.
    """
    _overstress: int = 0
    _reason: str = ""

    try:
        _load_type = {
            1: "resistive_load",
            2: "inductive_load",
            3: "capacitive_load",
        }[type_id]

        _overstress, _reason = do_check_current_limit(
            current_ratio,
            stress_limits[_load_type]["current"][environment_id],
        )

        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                temperature_active,
                temperature_rated_max,
                stress_limits[_load_type]["temperature"][environment_id],
            ),
        )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid relay environment ID {environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid relay load type ID {type_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid relay current ratio type "
            f"{type(current_ratio)} or ambient operating temperature "
            f"{type(temperature_active)}.  Both should be <type 'float'>."
        ) from exc
