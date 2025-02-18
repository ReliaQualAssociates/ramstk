# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.lamp.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import do_check_current_limit


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, List[float]]],
    *,
    current_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for lamps.

    :param environment_id: the index for the environment the lamp is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the lamp being checked for overstress.
    :param stress_limits: the dict containing the stress derating limits for lamps.
    :param current_ratio: the operating to rated current ratio of the lamp being checked
        for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    :raises: TypeError when passed a non-numeric value for the current ratio.
    """
    try:
        _subcategory = {
            4: "lamp",
        }[subcategory_id]

        return do_check_current_limit(
            current_ratio,
            stress_limits[_subcategory]["current"][environment_id],
        )
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid lamp environment ID {environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid lamp subcategory ID {subcategory_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid lamp current ratio type "
            f"{type(current_ratio)}.  Should be <type 'float'>."
        ) from exc
